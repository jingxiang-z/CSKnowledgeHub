from collections import deque
from threading import Thread, Condition


def run(producer_count=1, consumer_count=1, queue_size=5, items_to_produce=10):
    if producer_count <= 0 or consumer_count <= 0 or queue_size <= 0:
        raise ValueError("producer_count, consumer_count, and queue_size must be positive")
    if items_to_produce < 0:
        raise ValueError("items_to_produce must be non-negative")

    queue = deque()
    condition = Condition()
    producer_done = False

    def producer():
        for item in range(items_to_produce):
            with condition:
                while len(queue) == queue_size:
                    condition.wait()
                queue.append(item)
                condition.notify_all()

    def consumer(consumer_id):
        while True:
            with condition:
                while not queue and not producer_done:
                    condition.wait()
                if not queue:
                    return
                item = queue.popleft()
                condition.notify_all()
            print(f"Consumer {consumer_id} consumed item: {item}")

    producers = [Thread(target=producer) for _ in range(producer_count)]
    consumers = [Thread(target=consumer, args=(i,)) for i in range(consumer_count)]
    for p in producers:
        p.start()
    for c in consumers:
        c.start()
    for p in producers:
        p.join()
    # Signal consumers to stop after all producers are done
    with condition:
        producer_done = True
        condition.notify_all()
    for c in consumers:
        c.join()
