from concurrent.futures import ThreadPoolExecutor
import threading

import requests


class URLFetcher:
    """Use as a context manager to guarantee worker shutdown.

    cancel() (or cancel_event.set()) skips requests that have not started.
    Active requests finish normally. Cancellation stays set for this instance.
    """

    def __init__(self, max_workers=10):
        self.max_workers = max_workers
        self.executors = ThreadPoolExecutor(max_workers=self.max_workers)
        self.cancel_event = threading.Event()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.cancel()
        self.shutdown()

    def fetch_one(self, url, timeout=10):
        result = {"url": url, "status_code": None, "content_size": 0, "error": None}
        if self.cancel_event.is_set():
            result["error"] = "Fetch cancelled"
            return result
        try:
            with requests.get(url, timeout=timeout) as response:
                result["status_code"] = response.status_code
                result["content_size"] = len(response.content)
                response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            result["error"] = str(exc)
        return result

    def fetch_all(self, urls, timeout=10):
        """Return one record per input URL, preserving order and duplicates."""
        urls = list(urls)
        if len(urls) > 100:
            raise ValueError("Number of URLs exceeds 100")
        futures = [
            self.executors.submit(self.fetch_one, url, timeout=timeout)
            for url in urls
        ]
        # Requests run concurrently; collecting in submission order keeps duplicates.
        return [future.result() for future in futures]

    def cancel(self):
        """Skip queued/unsubmitted requests; allow active requests to finish."""
        self.cancel_event.set()

    def shutdown(self):
        self.executors.shutdown(wait=True)
