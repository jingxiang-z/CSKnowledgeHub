import io
import json
import unittest
from dataclasses import replace

from gpuinfo.cli import run
from gpuinfo.errors import GPUError
from gpuinfo.gpu import Metric, MetricState
from tests.fakes import FakeSession, snapshot


class WatchTests(unittest.TestCase):
    def setUp(self):
        self.session = FakeSession()
        self.out, self.err = io.StringIO(), io.StringIO()
        self.waits = []

    def wait(self, seconds):
        self.waits.append(seconds)

    def execute(self, *extra, wait=None):
        return run(
            ["watch", "0", "--output", "json", *extra],
            opener=lambda: self.session,
            sleep=self.wait if wait is None else wait,
            stdout=self.out,
            stderr=self.err,
        )

    def test_bounded_samples_and_intervals(self):
        self.assertEqual(self.execute("--count", "3", "--interval", "0.5"), 0)
        values = [json.loads(line) for line in self.out.getvalue().splitlines()]
        self.assertEqual([v["sample"] for v in values], [1, 2, 3])
        self.assertEqual(self.waits, [0.5, 0.5])
        self.assertEqual(self.session.query_calls, 3)
        self.assertEqual(self.session.close_calls, 1)

    def test_one_sample_does_not_wait(self):
        self.assertEqual(self.execute("--count", "1"), 0)
        self.assertEqual(self.waits, [])
        self.assertEqual(len(self.out.getvalue().splitlines()), 1)

    def test_partial_failure_does_not_stop(self):
        self.session.snapshot = replace(
            snapshot(),
            fan_speed_percent=Metric(MetricState.FAILED, error=GPUError("fan failed")),
        )
        self.assertEqual(self.execute("--count", "2"), 0)
        self.assertEqual(self.session.query_calls, 2)
        self.assertIn("sample 1: fan failed", self.err.getvalue())
        self.assertIn("sample 2: fan failed", self.err.getvalue())

    def test_keyboard_interrupt_while_sleeping(self):
        def interrupt(seconds):
            raise KeyboardInterrupt

        self.assertEqual(self.execute(wait=interrupt), 130)
        self.assertEqual(self.session.close_calls, 1)
        self.assertEqual(len(self.out.getvalue().splitlines()), 1)
        self.assertEqual(self.err.getvalue(), "")

    def test_keyboard_interrupt_during_query(self):
        def interrupt(selector):
            raise KeyboardInterrupt

        self.session.on_snapshot = interrupt
        self.assertEqual(self.execute("--count", "1"), 130)
        self.assertEqual(self.session.close_calls, 1)
        self.assertEqual(self.out.getvalue(), "")
        self.assertEqual(self.waits, [])

    def test_sigterm_style_exit_closes_session(self):
        def terminate(seconds):
            raise SystemExit(143)

        with self.assertRaises(SystemExit) as stopped:
            self.execute(wait=terminate)
        self.assertEqual(stopped.exception.code, 143)
        self.assertEqual(self.session.close_calls, 1)

    def test_fatal_query_stops_after_completed_sample(self):
        def query(selector):
            if self.session.query_calls == 2:
                raise GPUError("device lost")
            return snapshot()

        self.session.on_snapshot = query
        self.assertEqual(self.execute("--count", "3"), 1)
        self.assertEqual(self.session.query_calls, 2)
        self.assertEqual(self.waits, [2.0])
        self.assertEqual(self.session.close_calls, 1)
        self.assertEqual(len(self.out.getvalue().splitlines()), 1)

    def test_table_watch(self):
        self.assertEqual(
            run(
                ["watch", "0", "--count", "2"],
                opener=lambda: self.session,
                sleep=self.wait,
                stdout=self.out,
                stderr=self.err,
            ),
            0,
        )
        self.assertIn("SAMPLE 1", self.out.getvalue())
        self.assertIn("SAMPLE 2", self.out.getvalue())
        self.assertIn("MEMORY USED (BYTES)", self.out.getvalue())
