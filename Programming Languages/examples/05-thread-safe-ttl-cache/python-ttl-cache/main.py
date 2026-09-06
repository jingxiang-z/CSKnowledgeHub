import threading
import time


class TTLCache:
    def __init__(self, clock=None, cleanup_interval=1.0):
        self.cache = {}
        self.ttl = {}
        self.lock = threading.Lock()
        self._clock = time.monotonic if clock is None else clock
        self._cleanup_interval = cleanup_interval
        self._stop_event = threading.Event()
        self._worker = None

        if cleanup_interval is not None:
            if cleanup_interval <= 0:
                raise ValueError("cleanup_interval must be positive")
            self._worker = threading.Thread(target=self._run_cleanup)
            self._worker.start()

    def get(self, key):
        with self.lock:
            if key in self.cache and self.ttl[key] > self._clock():
                return self.cache[key], True
            if key in self.cache:
                del self.cache[key]
                del self.ttl[key]
            return None, False

    def set(self, key, value, ttl):
        if ttl <= 0:
            raise ValueError("ttl must be positive")

        with self.lock:
            self.cache[key] = value
            self.ttl[key] = self._clock() + ttl

    def delete(self, key):
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                del self.ttl[key]

    def len(self):
        with self.lock:
            self._delete_expired(self._clock())
            return len(self.cache)

    def _delete_expired(self, now):
        removed = 0
        for key in list(self.cache.keys()):
            if self.ttl[key] <= now:
                del self.cache[key]
                del self.ttl[key]
                removed += 1
        return removed

    def cleanup(self):
        with self.lock:
            return self._delete_expired(self._clock())

    def _run_cleanup(self):
        while not self._stop_event.wait(self._cleanup_interval):
            self.cleanup()

    def close(self):
        self._stop_event.set()
        if self._worker is not None:
            self._worker.join()
