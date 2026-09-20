from concurrent.futures import ThreadPoolExecutor
import logging
from threading import Event, Thread
from time import monotonic, sleep
from urllib.request import urlopen
import socket

import pytest
import uvicorn
from fastapi.testclient import TestClient

import main
from main import app, lock, store


@pytest.fixture(autouse=True)
def clear_store():
    with lock:
        store.clear()


def test_crud():
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "healthy"}
        assert client.get("/keys/item").status_code == 404
        assert client.put("/keys/item", json={"value": 1}).status_code == 200
        assert client.get("/keys/item").json() == {"key": "item", "value": 1}
        assert client.delete("/keys/item").status_code == 204
        assert client.get("/keys/item").status_code == 404


def test_json_values_and_errors():
    with TestClient(app) as client:
        for index, value in enumerate((None, True, 3.5, "text", [1], {"a": 1})):
            key = f"item_{index}"
            assert client.put(f"/keys/{key}", json={"value": value}).status_code == 200
            assert client.get(f"/keys/{key}").json()["value"] == value

        assert client.put("/keys/item", json={}).status_code == 422
        assert client.put(
            "/keys/item", content='{"value":',
            headers={"content-type": "application/json"},
        ).status_code == 422
        assert client.get("/keys/bad.key").status_code == 400
        assert client.get("/missing").status_code == 404
        assert client.post("/keys/item").status_code == 405


def test_concurrent_requests():
    with TestClient(app) as client:
        def write(value):
            return client.put("/keys/shared", json={"value": value}).status_code

        with ThreadPoolExecutor(max_workers=12) as pool:
            statuses = list(pool.map(write, range(24)))

        assert statuses == [200] * 24
        assert client.get("/keys/shared").json()["value"] in range(24)


def test_request_logging_and_unexpected_error(caplog, monkeypatch):
    caplog.set_level(logging.INFO, logger="key_value_server")

    class BrokenStore(dict):
        def __getitem__(self, key):
            raise RuntimeError("broken store")

    with TestClient(app, raise_server_exceptions=False) as client:
        assert client.get("/health").status_code == 200
        monkeypatch.setattr(main, "store", BrokenStore(item=1))
        response = client.get("/keys/item")

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}
    assert "GET /health 200" in caplog.text
    assert "GET /keys/item 500" in caplog.text
    assert "broken store" in caplog.text


def test_shutdown_waits_for_active_request(monkeypatch):
    entered = Event()
    release = Event()

    class SlowStore(dict):
        def __getitem__(self, key):
            entered.set()
            assert release.wait(3)
            return super().__getitem__(key)

    monkeypatch.setattr(main, "store", SlowStore(item=42))
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]

    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port,
                                           timeout_graceful_shutdown=2, log_level="error"))
    thread = Thread(target=server.run, daemon=True)
    thread.start()
    try:
        deadline = monotonic() + 3
        while not server.started and monotonic() < deadline:
            sleep(0.01)
        assert server.started

        with ThreadPoolExecutor(max_workers=1) as pool:
            request = pool.submit(lambda: urlopen(f"http://127.0.0.1:{port}/keys/item").read())
            assert entered.wait(2)
            server.should_exit = True
            sleep(0.2)
            assert thread.is_alive()
            release.set()
            assert request.result(timeout=2) == b'{"key":"item","value":42}'

        thread.join(timeout=3)
        assert not thread.is_alive()
    finally:
        release.set()
        server.should_exit = True
        thread.join(timeout=3)
