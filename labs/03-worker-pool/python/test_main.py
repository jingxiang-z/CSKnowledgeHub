import threading
import unittest
from concurrent.futures import ThreadPoolExecutor, TimeoutError

from main import WorkerPool


class WorkerPoolTests(unittest.TestCase):
    def make_pool(self, workers=1, queue_size=2):
        pool = WorkerPool(workers, queue_size)
        self.addCleanup(pool.shutdown)
        return pool

    def blocked_task(self, pool):
        """Keep one worker busy until the test releases it."""
        started = threading.Event()
        release = threading.Event()
        self.addCleanup(release.set)

        def task():
            started.set()
            if not release.wait(3):
                raise TimeoutError("test did not release worker")
            return 42

        future = pool.submit_task(task)
        self.assertTrue(started.wait(1))
        return release, future

    def test_empty_input(self):
        self.assertEqual(self.make_pool().get_results(), {
            "completed": [], "failed": [], "cancelled": [],
        })

    def test_one_worker(self):
        pool = self.make_pool()
        executed = []

        def task(number):
            executed.append(number)
            return number * number

        for number in range(3):
            pool.submit_task(task, number)
        self.assertEqual(pool.get_results()["completed"], [0, 1, 4])
        self.assertEqual(executed, [0, 1, 2])

    def test_fewer_jobs_than_workers(self):
        pool = self.make_pool(workers=4)
        release, first = self.blocked_task(pool)
        second = pool.submit_task(lambda: 99)
        self.assertEqual(second.result(timeout=1), 99)
        self.assertFalse(first.done())  # Jobs can finish out of order.
        release.set()
        self.assertEqual(pool.get_results()["completed"], [42, 99])

    def test_bounded_queue(self):
        pool = self.make_pool(queue_size=1)
        release, _ = self.blocked_task(pool)
        pool.submit_task(lambda: 99)  # Fill the waiting slot.

        with ThreadPoolExecutor(max_workers=1) as producer:
            entered = threading.Event()

            def submit():
                entered.set()
                return pool.submit_task(lambda: 100)

            submission = producer.submit(submit)
            try:
                self.assertTrue(entered.wait(1))
                with self.assertRaises(TimeoutError):
                    submission.result(timeout=0.05)
            finally:
                release.set()
            submission.result(timeout=1)

        self.assertEqual(pool.get_results()["completed"], [42, 99, 100])

    def test_job_failure(self):
        pool = self.make_pool()

        def fail():
            raise ValueError("boom")

        failed = pool.submit_task(fail)
        with self.assertRaises(ValueError):
            failed.result(timeout=1)
        pool.submit_task(lambda: 99)  # Failure must not close the pool.
        self.assertEqual(pool.get_results(), {
            "completed": [99], "failed": [failed], "cancelled": [],
        })

    def test_cancellation(self):
        pool = self.make_pool()
        release, running = self.blocked_task(pool)
        queued = pool.submit_task(lambda: 99)
        pool.cancel()
        self.assertTrue(queued.cancelled())
        self.assertFalse(running.done())
        with self.assertRaises(RuntimeError):
            pool.submit_task(lambda: None)
        release.set()
        self.assertEqual(pool.get_results(), {
            "completed": [42], "failed": [], "cancelled": [queued],
        })

    def test_clean_shutdown(self):
        pool = self.make_pool()
        release, running = self.blocked_task(pool)
        worker = pool.submit_task(threading.current_thread)
        release.set()
        pool.shutdown()
        self.assertTrue(running.done())
        self.assertFalse(worker.result(timeout=1).is_alive())
        with self.assertRaises(RuntimeError):
            pool.submit_task(lambda: None)


if __name__ == "__main__":
    unittest.main()
