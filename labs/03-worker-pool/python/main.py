from concurrent.futures import CancelledError, ThreadPoolExecutor
import threading

class WorkerPool:
    def __init__(self, max_workers, queue_size):
        if max_workers <= 0:
            raise ValueError("max_workers must be a positive integer")
        if queue_size <= 0:
            raise ValueError("queue_size must be a positive integer")
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.tasks = []
        self.slots = threading.BoundedSemaphore(max_workers + queue_size)
        self.lock = threading.Lock()
        self.closed = False

    def submit_task(self, task, *args, **kwargs):
        # Poll so a blocked producer can notice cancellation or shutdown.
        while True:
            with self.lock:
                if self.closed:
                    raise RuntimeError("pool is not accepting tasks")
            if self.slots.acquire(timeout=0.05):
                break
        try:
            with self.lock:
                if self.closed:
                    raise RuntimeError("pool is not accepting tasks")
                future = self.executor.submit(task, *args, **kwargs)
                self.tasks.append(future)
        except BaseException:
            self.slots.release()
            raise
        # Register outside the lock: an already finished future calls this now.
        future.add_done_callback(lambda _: self.slots.release())
        return future

    def get_results(self):
        results = {
            "completed": [],
            "failed": [],
            "cancelled": []
        }
        with self.lock:
            tasks = list(self.tasks)
        for future in tasks:
            try:
                value = future.result()
            except CancelledError:
                # A task can also raise CancelledError without being cancelled.
                outcome = "cancelled" if future.cancelled() else "failed"
                results[outcome].append(future)
            except Exception:
                results["failed"].append(future)
            else:
                results["completed"].append(value)
        return results

    def cancel(self):
        """Reject new work and cancel queued tasks; running tasks may finish."""
        with self.lock:
            self.closed = True
            tasks = list(self.tasks)
        # Cancelling invokes callbacks, so do it outside the lock.
        for future in tasks:
            future.cancel()

    def shutdown(self):
        """Call from the owner thread to wait for all workers to exit."""
        with self.lock:
            self.closed = True
        self.executor.shutdown(wait=True)
