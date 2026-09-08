class Node:
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    """An LRU cache backed by a dictionary and an owned recency list.

    ``cache`` owns all entry nodes. The head and tail sentinels belong to the
    cache itself, bound the list, and are never placed in the dictionary.
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.cache = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove_node(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = None
        node.next = None

    def _add_to_head(self, node: Node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def Get(self, key: int) -> tuple[int, bool]:
        if key in self.cache:
            node = self.cache[key]
            self._remove_node(node)
            self._add_to_head(node)
            return node.value, True
        return 0, False

    def Put(self, key: int, value: int):
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove_node(node)
            self._add_to_head(node)
        else:
            new_node = Node(key, value)
            self._add_to_head(new_node)
            self.cache[key] = new_node
            if len(self.cache) > self.capacity:
                tail_prev = self.tail.prev
                self._remove_node(tail_prev)
                del self.cache[tail_prev.key]

    def Delete(self, key: int):
        if key in self.cache:
            node = self.cache[key]
            self._remove_node(node)
            del self.cache[key]

    def Len(self) -> int:
        return len(self.cache)

    def Capacity(self) -> int:
        return self.capacity
