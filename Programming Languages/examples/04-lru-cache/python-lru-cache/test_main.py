import unittest

from main import LRUCache


class TestLRUCache(unittest.TestCase):
    def assert_order(self, cache, expected):
        actual = []
        node = cache.head.next
        while node is not cache.tail:
            actual.append(node.key)
            node = node.next
        self.assertEqual(actual, expected)

    def test_insert_and_get(self):
        cache = LRUCache(2)
        cache.Put(1, 10)
        self.assertEqual(cache.Get(1), (10, True))
        self.assertEqual(cache.Len(), 1)

    def test_lru_get_promotion(self):
        cache = LRUCache(2)
        cache.Put(1, 1)
        cache.Put(2, 2)
        cache.Get(1)
        self.assert_order(cache, [1, 2])
        cache.Put(3, 3)
        self.assertEqual(cache.Get(2), (0, False))
        self.assert_order(cache, [3, 1])

    def test_lru_put_promotion(self):
        cache = LRUCache(2)
        cache.Put(1, 1)
        cache.Put(2, 2)
        cache.Put(1, 10)
        self.assert_order(cache, [1, 2])
        cache.Put(3, 3)
        self.assertEqual(cache.Get(2), (0, False))
        self.assertEqual(cache.Get(1), (10, True))

    def test_capacity_eviction(self):
        cache = LRUCache(2)
        cache.Put(1, 1)
        cache.Put(2, 2)
        cache.Put(3, 3)
        self.assertEqual(cache.Get(1), (0, False))
        self.assertEqual(cache.Len(), 2)
        self.assertEqual(cache.Capacity(), 2)

    def test_delete(self):
        cache = LRUCache(2)
        cache.Put(1, 1)
        cache.Put(2, 2)
        cache.Delete(1)
        self.assertEqual(cache.Get(1), (0, False))
        self.assertEqual(cache.Len(), 1)
        self.assert_order(cache, [2])

    def test_non_positive_capacity(self):
        for capacity in (0, -1):
            with self.subTest(capacity=capacity):
                with self.assertRaises(ValueError):
                    LRUCache(capacity)

    def test_repeated_operations_on_one_key(self):
        cache = LRUCache(1)
        for value in range(5):
            cache.Put(1, value)
            self.assertEqual(cache.Get(1), (value, True))
            self.assertEqual(cache.Len(), 1)
        cache.Delete(1)
        cache.Delete(1)
        self.assertEqual(cache.Len(), 0)

    def test_stored_negative_one_is_found(self):
        cache = LRUCache(1)
        cache.Put(1, -1)
        self.assertEqual(cache.Get(1), (-1, True))


if __name__ == "__main__":
    unittest.main()
