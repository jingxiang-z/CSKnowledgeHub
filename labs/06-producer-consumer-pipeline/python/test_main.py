from collections import Counter
from threading import Event, Lock, Thread, enumerate as live_threads
import unittest
from unittest.mock import patch

import main


class ProducerConsumerTests(unittest.TestCase):
    def start_run(self, **kwargs):
        """Run in a daemon thread so a deadlock fails the test promptly."""
        outcome = []

        def target():
            try:
                main.run(**kwargs)
            except Exception as exception:
                outcome.append(exception)
            else:
                outcome.append(None)

        thread = Thread(target=target, daemon=True)
        thread.start()
        return thread, outcome

    def finish_run(self, thread, outcome):
        thread.join(timeout=2)
        self.assertFalse(thread.is_alive(), "run() did not shut down")
        self.assertEqual(len(outcome), 1)
        return outcome[0]

    def test_empty_input_stops_all_workers(self):
        before = {thread.ident for thread in live_threads()}
        with patch.object(main, "print", create=True) as output:
            thread, outcome = self.start_run(
                producer_count=2, consumer_count=3,
                queue_size=1, items_to_produce=0,
            )
            self.assertIsNone(self.finish_run(thread, outcome))
            output.assert_not_called()
        self.assertEqual({thread.ident for thread in live_threads()}, before)

    def test_every_item_is_consumed_with_multiple_workers(self):
        messages = []
        lock = Lock()

        def record(message):
            with lock:
                messages.append(message)

        with patch.object(main, "print", create=True, side_effect=record):
            thread, outcome = self.start_run(
                producer_count=3, consumer_count=4,
                queue_size=1, items_to_produce=10,
            )
            self.assertIsNone(self.finish_run(thread, outcome))

        values = [int(message.rsplit(": ", 1)[1]) for message in messages]
        self.assertEqual(Counter(values), Counter({item: 3 for item in range(10)}))

    def test_slow_consumer_eventually_releases_producer(self):
        consuming = Event()
        release = Event()
        self.addCleanup(release.set)
        messages = []

        def slow_consume(message):
            consuming.set()
            if not release.wait(timeout=2):
                raise TimeoutError("test did not release the consumer")
            messages.append(message)

        with patch.object(main, "print", create=True, side_effect=slow_consume):
            thread, outcome = self.start_run(queue_size=1, items_to_produce=3)
            self.assertTrue(consuming.wait(timeout=1))
            self.assertTrue(thread.is_alive())
            release.set()
            self.assertIsNone(self.finish_run(thread, outcome))

        self.assertEqual(len(messages), 3)

    def test_invalid_configuration(self):
        for kwargs in (
            {"producer_count": 0},
            {"consumer_count": 0},
            {"queue_size": 0},
            {"items_to_produce": -1},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                main.run(**kwargs)


if __name__ == "__main__":
    unittest.main()
