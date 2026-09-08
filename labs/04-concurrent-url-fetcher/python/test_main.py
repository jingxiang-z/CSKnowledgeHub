import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

import requests

import main


class FetcherTests(unittest.TestCase):
    def setUp(self):
        self.started = threading.Event()
        self.release = threading.Event()
        self.paths = []
        self.lock = threading.Lock()
        self.active = 0
        self.peak = 0
        self.two_active = threading.Event()
        test = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                with test.lock:
                    test.paths.append(self.path)
                    test.active += 1
                    test.peak = max(test.peak, test.active)
                    if test.active == 2:
                        test.two_active.set()
                try:
                    if self.path.startswith('/blocked'):
                        test.started.set()
                        test.release.wait(3)
                    body = 'héllo'.encode()
                    self.send_response(404 if self.path == '/missing' else 200)
                    self.send_header('Content-Length', str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                except (BrokenPipeError, ConnectionResetError):
                    pass
                finally:
                    with test.lock:
                        test.active -= 1

            def log_message(self, *args):
                pass

        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()
        self.base = f'http://127.0.0.1:{self.server.server_port}'

    def tearDown(self):
        self.release.set()
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def test_order_duplicates_partial_failure_and_http_errors(self):
        urls = [self.base + '/ok', 'invalid-url', self.base + '/missing', self.base + '/ok']
        with main.URLFetcher() as fetcher:
            results = fetcher.fetch_all(urls)
        self.assertEqual([r['url'] for r in results], urls)
        self.assertEqual(results[0]['content_size'], len('héllo'.encode()))
        self.assertIsNone(results[0]['error'])
        self.assertIsNotNone(results[1]['error'])
        self.assertEqual(results[2]['status_code'], 404)
        self.assertEqual(results[2]['content_size'], len('héllo'.encode()))
        self.assertIsNotNone(results[2]['error'])
        self.assertEqual(results[3], results[0])

    def test_cancellation_leaves_active_request_running(self):
        urls = [self.base + '/blocked', self.base + '/queued']
        with main.URLFetcher(max_workers=1) as fetcher, ThreadPoolExecutor(1) as caller:
            future = caller.submit(fetcher.fetch_all, urls)
            try:
                self.assertTrue(self.started.wait(1))
                fetcher.cancel()
                self.assertFalse(future.done())
            finally:
                self.release.set()
            results = future.result(timeout=2)
        self.assertEqual(results[0]['status_code'], 200)
        self.assertIsNone(results[0]['error'])
        self.assertEqual(results[1]['error'], 'Fetch cancelled')
        self.assertEqual(self.paths, ['/blocked'])

    def test_pre_cancelled_and_empty_inputs(self):
        with main.URLFetcher() as fetcher:
            self.assertEqual(fetcher.fetch_all([]), [])
            fetcher.cancel_event.set()
            results = fetcher.fetch_all([self.base + '/ok'])
            self.assertEqual(results[0]['error'], 'Fetch cancelled')
        self.assertEqual(self.paths, [])

    def test_concurrency_and_out_of_order_completion(self):
        urls = [self.base + '/blocked-first', self.base + '/blocked-second', self.base + '/last']
        with main.URLFetcher(max_workers=2) as fetcher, ThreadPoolExecutor(1) as caller:
            future = caller.submit(fetcher.fetch_all, urls)
            try:
                self.assertTrue(self.two_active.wait(1))
                self.assertEqual(len(self.paths), 2)
            finally:
                self.release.set()
            results = future.result(timeout=2)
        self.assertEqual([r['url'] for r in results], urls)
        self.assertTrue(all(r['error'] is None for r in results))
        self.assertLessEqual(self.peak, 2)

    def test_timeout(self):
        with main.URLFetcher() as fetcher:
            result = fetcher.fetch_one(self.base + '/blocked', timeout=0.05)
        self.assertIsNotNone(result['error'])
        self.assertIsNone(result['status_code'])

    def test_response_closed_on_success_and_http_error(self):
        original_get = requests.get
        responses = []

        def tracked_get(*args, **kwargs):
            response = original_get(*args, **kwargs)
            response.close = unittest.mock.Mock(wraps=response.close)
            responses.append(response)
            return response

        with patch.object(main.requests, 'get', side_effect=tracked_get):
            with main.URLFetcher() as fetcher:
                fetcher.fetch_all([self.base + '/ok', self.base + '/missing'])
        self.assertEqual(len(responses), 2)
        for response in responses:
            response.close.assert_called_once()

    def test_shutdown_on_success_and_unexpected_failure(self):
        with main.URLFetcher() as fetcher:
            fetcher.fetch_all([self.base + '/ok'])
        self.assertTrue(all(not t.is_alive() for t in fetcher.executors._threads))
        with self.assertRaisesRegex(RuntimeError, 'bug'):
            with main.URLFetcher() as fetcher:
                with patch.object(fetcher, 'fetch_one', side_effect=RuntimeError('bug')):
                    fetcher.fetch_all([self.base + '/ok'])
        self.assertTrue(all(not t.is_alive() for t in fetcher.executors._threads))

    def test_input_limits(self):
        with main.URLFetcher() as fetcher:
            with self.assertRaises(ValueError):
                fetcher.fetch_all(['url'] * 101)
        with self.assertRaises(ValueError):
            main.URLFetcher(max_workers=0)


if __name__ == '__main__':
    unittest.main()
