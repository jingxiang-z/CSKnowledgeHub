import unittest
import threading
from concurrent.futures import ThreadPoolExecutor

from main import TTLCache


class FakeClock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


class TestTTLCache(unittest.TestCase):
    def setUp(self):
        self.clock = FakeClock()
        self.cache = TTLCache(clock=self.clock, cleanup_interval=None)

    def tearDown(self):
        self.cache.close()

    def test_cache_hit(self):
        self.cache.set("key1", "value1", 10)
        self.assertEqual(self.cache.get("key1"), ("value1", True))

    def test_cache_miss(self):
        self.assertEqual(self.cache.get("key1"), (None, False))

    def test_cached_none_is_distinct_from_cache_miss(self):
        self.cache.set("key1", None, 10)
        self.assertEqual(self.cache.get("key1"), (None, True))
        self.assertEqual(self.cache.get("missing"), (None, False))

    def test_cache_expiry(self):
        self.cache.set("key1", "value1", 1)
        self.assertEqual(self.cache.get("key1"), ("value1", True))
        self.clock.advance(1)
        self.assertEqual(self.cache.get("key1"), (None, False))

    def test_cache_update(self):
        self.cache.set("key1", "value1", 10)
        self.assertEqual(self.cache.get("key1"), ("value1", True))
        self.cache.set("key1", "value2", 10)
        self.assertEqual(self.cache.get("key1"), ("value2", True))

    def test_cache_delete(self):
        self.cache.set("key1", "value1", 10)
        self.assertEqual(self.cache.get("key1"), ("value1", True))
        self.cache.delete("key1")
        self.assertEqual(self.cache.get("key1"), (None, False))

    def test_cache_len(self):
        self.cache.set("key1", "value1", 10)
        self.cache.set("key2", "value2", 10)
        self.assertEqual(self.cache.len(), 2)

    def test_cache_len_excludes_expired_entries(self):
        self.cache.set("key1", "value1", 1)
        self.clock.advance(1)
        self.assertEqual(self.cache.len(), 0)

    def test_rejects_non_positive_ttl(self):
        for ttl in (0, -1):
            with self.subTest(ttl=ttl):
                with self.assertRaises(ValueError):
                    self.cache.set("key1", "value1", ttl)

    def test_explicit_cleanup(self):
        self.cache.set("key1", "value1", 1)
        self.clock.advance(1)
        self.assertEqual(self.cache.cleanup(), 1)
        self.assertEqual(self.cache.get("key1"), (None, False))

    def test_close_interrupts_cleanup_worker(self):
        cache = TTLCache(clock=self.clock, cleanup_interval=60)
        cache.close()
        self.assertFalse(cache._worker.is_alive())

    def test_cache_concurrent_read(self):
        self.cache.set("key1", "value1", 10)

        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(lambda _: self.cache.get("key1"), range(10)))

        self.assertEqual(results, [("value1", True)] * 10)

    def test_cache_concurrent_write(self):
        entries = [(f"key{i}", f"value{i}") for i in range(10)]

        def write_cache(entry):
            key, value = entry
            self.cache.set(key, value, 10)

        with ThreadPoolExecutor(max_workers=10) as executor:
            list(executor.map(write_cache, entries))

        self.assertEqual(self.cache.len(), len(entries))
        for key, value in entries:
            self.assertEqual(self.cache.get(key), (value, True))

    def test_cache_concurrent_read_and_write(self):
        self.cache.set("key1", "value1", 10)
        barrier = threading.Barrier(10)
        written_values = {f"value{i}" for i in range(5)}
        valid_values = {"value1"} | written_values

        def read_cache():
            barrier.wait()
            return [self.cache.get("key1") for _ in range(100)]

        def write_cache(value):
            barrier.wait()
            self.cache.set("key1", value, 10)

        with ThreadPoolExecutor(max_workers=10) as executor:
            read_futures = [executor.submit(read_cache) for _ in range(5)]
            write_futures = [
                executor.submit(write_cache, value) for value in written_values
            ]
            observed_results = [
                result
                for future in read_futures
                for result in future.result()
            ]
            for future in write_futures:
                future.result()

        self.assertTrue(
            all(found and value in valid_values for value, found in observed_results)
        )
        value, found = self.cache.get("key1")
        self.assertTrue(found)
        self.assertIn(value, written_values)


if __name__ == "__main__":
    unittest.main()
