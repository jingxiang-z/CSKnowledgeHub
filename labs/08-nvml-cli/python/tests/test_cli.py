import io
import json
import unittest
from dataclasses import replace

from gpuinfo.cli import run
from gpuinfo.errors import GPUError
from gpuinfo.gpu import (
    Device,
    DeviceResult,
    Metric,
    MetricState,
    Process,
    ProcessList,
    SelectorKind,
)
from tests.fakes import FakeSession, snapshot


class CLITests(unittest.TestCase):
    def setUp(self):
        self.session = FakeSession()
        self.opens = 0
        self.out, self.err = io.StringIO(), io.StringIO()

    def open(self):
        self.opens += 1
        return self.session

    def execute(self, args, **kwargs):
        return run(args, opener=self.open, stdout=self.out, stderr=self.err, **kwargs)

    def test_selectors(self):
        for args, kind, value in (
            (["show", "0"], SelectorKind.INDEX, 0),
            (["show", "--uuid", "GPU-0"], SelectorKind.UUID, "GPU-0"),
            (
                ["show", "--pci-bus-id", "0000:01:00.0"],
                SelectorKind.PCI_BUS_ID,
                "0000:01:00.0",
            ),
        ):
            with self.subTest(args=args):
                self.assertEqual(self.execute(args), 0)
                self.assertEqual(self.session.selector.kind, kind)
                self.assertEqual(self.session.selector.value, value)
        self.assertEqual(self.opens, 3)
        self.assertEqual(self.session.close_calls, 3)

    def test_validation_precedes_init(self):
        for args in (
            [],
            ["show"],
            ["show", "-1"],
            ["show", "abc"],
            ["show", "--uuid", ""],
            ["show", "0", "--uuid", "GPU-0"],
            ["show", "--uuid", "GPU-0", "--pci-bus-id", "x"],
            ["watch", "0", "--interval", "0"],
            ["watch", "0", "--interval", "-2"],
            ["watch", "0", "--interval", "bad"],
            ["watch", "0", "--count", "0"],
            ["watch", "0", "--count", "1.5"],
            ["list", "--output", "xml"],
        ):
            with self.subTest(args=args):
                self.assertEqual(self.execute(args), 2)
        self.assertEqual(self.opens, 0)
        self.assertEqual(self.session.close_calls, 0)
        self.assertEqual(self.out.getvalue(), "")

    def test_help_without_native_dependency(self):
        self.assertEqual(self.execute(["watch", "--help"]), 0)
        self.assertIn("--interval", self.out.getvalue())
        self.assertEqual(self.opens, 0)

    def test_list_zero_one_multiple_order_and_partial_failure(self):
        for count in (0, 1, 3):
            with self.subTest(count=count):
                self.out.seek(0)
                self.out.truncate()
                self.session.devices = [
                    DeviceResult(Device(index, f"GPU {index}"))
                    for index in range(count)
                ]
                if count == 3:
                    self.session.devices[1] = DeviceResult(
                        Device(1), GPUError("device 1 UUID unavailable")
                    )
                self.assertEqual(
                    self.execute(["list", "--output", "json"]), 1 if count == 3 else 0
                )
                values = json.loads(self.out.getvalue())
                self.assertEqual(
                    [v["device"]["index"] for v in values], list(range(count))
                )
                if count == 3:
                    self.assertEqual(values[1]["error"], "device 1 UUID unavailable")
                    self.assertEqual(values[2]["device"]["name"], "GPU 2")
        self.assertEqual(self.session.close_calls, 3)

    def test_root_output_flag_and_system_json(self):
        self.assertEqual(self.execute(["--output", "json", "system"]), 0)
        self.assertEqual(
            json.loads(self.out.getvalue()),
            {
                "driver_version": "driver",
                "cuda_driver_version": "12.4",
                "nvml_version": "12",
                "device_count": 1,
            },
        )

    def test_snapshot_partial_metrics_and_raw_units(self):
        self.session.snapshot = replace(
            snapshot(),
            temperature_celsius=Metric(
                MetricState.UNSUPPORTED, error=GPUError("temperature unsupported")
            ),
            gpu_utilization_percent=Metric(
                MetricState.FAILED, error=GPUError("GPU utilization failed")
            ),
        )
        self.assertEqual(self.execute(["show", "0", "--output", "json"]), 1)
        value = json.loads(self.out.getvalue())
        self.assertEqual(
            value["memory"]["value"],
            {
                "total_bytes": 16_000_000_000,
                "used_bytes": 4_000_000_000,
                "free_bytes": 12_000_000_000,
            },
        )
        self.assertEqual(value["power_usage_milliwatts"]["value"], 125_000)
        self.assertEqual(value["fan_speed_percent"], {"state": "available", "value": 0})
        self.assertEqual(
            value["temperature_celsius"],
            {"state": "unsupported", "error": "temperature unsupported"},
        )
        self.assertEqual(
            value["gpu_utilization_percent"],
            {"state": "failed", "error": "GPU utilization failed"},
        )
        self.assertNotIn("device_error", value)
        self.assertIn("GPU utilization failed", self.err.getvalue())

    def test_unsupported_is_successful(self):
        self.session.snapshot = replace(
            snapshot(), fan_speed_percent=Metric(MetricState.UNSUPPORTED)
        )
        self.assertEqual(self.execute(["show", "0"]), 0)
        self.assertIn("unsupported", self.out.getvalue())
        self.assertEqual(self.err.getvalue(), "")

    def test_process_alias_json(self):
        self.session.processes = ProcessList(
            0, [Process(123, Metric(MetricState.UNSUPPORTED))]
        )
        self.assertEqual(self.execute(["processes", "0", "--output", "json"]), 0)
        self.assertEqual(
            json.loads(self.out.getvalue()),
            {
                "device_index": 0,
                "processes": [
                    {"pid": 123, "used_gpu_memory_bytes": {"state": "unsupported"}}
                ],
            },
        )

    def test_empty_process_table(self):
        self.assertEqual(self.execute(["process", "0"]), 0)
        self.assertIn("No active compute processes", self.out.getvalue())

    def test_init_failure_no_shutdown_or_stdout(self):
        def fail():
            raise GPUError("initialize NVML failed")

        self.assertEqual(
            run(
                ["list", "--output", "json"],
                opener=fail,
                stdout=self.out,
                stderr=self.err,
            ),
            1,
        )
        self.assertEqual(self.session.close_calls, 0)
        self.assertEqual(self.out.getvalue(), "")
        self.assertIn("initialize NVML failed", self.err.getvalue())

    def test_shutdown_failure_reported(self):
        self.session.query_error = GPUError("query failed")
        self.session.close_error = GPUError("shutdown failed")
        self.assertEqual(self.execute(["system", "--output", "json"]), 1)
        self.assertIn("shutdown failed", self.err.getvalue())
        self.assertEqual(self.session.close_calls, 1)
        self.assertEqual(self.out.getvalue(), "")

    def test_system_partial_error_rendered(self):
        self.session.info = replace(
            self.session.info, error=GPUError("driver unavailable")
        )
        self.assertEqual(self.execute(["system", "--output", "json"]), 1)
        self.assertEqual(json.loads(self.out.getvalue())["error"], "driver unavailable")
        self.assertEqual(self.session.close_calls, 1)

    def test_keyboard_interrupt_closes_session(self):
        self.session.query_error = KeyboardInterrupt()
        self.assertEqual(self.execute(["list"]), 130)
        self.assertEqual(self.session.close_calls, 1)
        self.assertEqual(self.out.getvalue(), "")
        self.assertEqual(self.err.getvalue(), "")


class EntryPointTests(unittest.TestCase):
    def test_sigterm_exits_and_handler_is_restored(self):
        import signal
        from unittest.mock import patch

        from gpuinfo.cli import main

        installed = {}
        old = object()

        def install(signum, handler):
            installed[signum] = handler
            return old

        def execute():
            installed[signal.SIGTERM](signal.SIGTERM, None)

        with (
            patch("gpuinfo.cli.signal.signal", side_effect=install),
            patch("gpuinfo.cli.run", side_effect=execute),
            self.assertRaises(SystemExit) as stopped,
        ):
            main()
        self.assertEqual(stopped.exception.code, 143)
        self.assertIs(installed[signal.SIGTERM], old)

    def test_module_exit_code_and_stderr(self):
        import subprocess
        import sys

        result = subprocess.run(
            [sys.executable, "-m", "gpuinfo", "list", "--output", "xml"],
            capture_output=True,
            check=False,
            text=True,
            timeout=5,
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("invalid choice", result.stderr)


if __name__ == "__main__":
    unittest.main()
