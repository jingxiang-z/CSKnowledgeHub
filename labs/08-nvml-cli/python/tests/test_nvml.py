import unittest
from types import SimpleNamespace

from gpuinfo.errors import FatalQueryError, GPUError
from gpuinfo.gpu import DeviceSelector, MetricState, SelectorKind
from gpuinfo.nvml import NVMLProvider, open_session


class BindingError(Exception):
    def __init__(self, value):
        self.value = value
        super().__init__(f"NVML error {value}")


class FakeBinding:
    NVMLError = BindingError
    NVML_ERROR_NOT_SUPPORTED = 3
    NVML_ERROR_GPU_IS_LOST = 15
    NVML_ERROR_UNINITIALIZED = 1
    NVML_ERROR_LIBRARY_NOT_FOUND = 12
    NVML_TEMPERATURE_GPU = 0

    def __init__(self):
        self.calls = []
        self.failures = {}
        self.after_call = None
        self.count = 3

    def __getattr__(self, name):
        if not name.startswith("nvml"):
            raise AttributeError(name)

        def call(*args):
            self.calls.append((name, args))
            failure = self.failures.get((name, args), self.failures.get(name))
            if failure is not None:
                raise BindingError(failure)
            values = {
                "nvmlSystemGetDriverVersion": b"driver",
                "nvmlSystemGetCudaDriverVersion_v2": 12040,
                "nvmlSystemGetNVMLVersion": "12",
                "nvmlDeviceGetCount": self.count,
                "nvmlDeviceGetHandleByIndex": args[0] if args else None,
                "nvmlDeviceGetHandleByUUID": 0,
                "nvmlDeviceGetHandleByPciBusId": 0,
                "nvmlDeviceGetIndex": args[0] if args else None,
                "nvmlDeviceGetName": b"Example GPU",
                "nvmlDeviceGetUUID": "GPU-0",
                "nvmlDeviceGetPciInfo": SimpleNamespace(busId=b"0000:01:00.0"),
                "nvmlDeviceGetTemperature": 42,
                "nvmlDeviceGetUtilizationRates": SimpleNamespace(gpu=75, memory=50),
                "nvmlDeviceGetMemoryInfo": SimpleNamespace(
                    total=16000, used=4000, free=12000
                ),
                "nvmlDeviceGetPowerUsage": 125000,
                "nvmlDeviceGetEnforcedPowerLimit": 250000,
                "nvmlDeviceGetFanSpeed": 0,
                "nvmlDeviceGetComputeRunningProcesses": [
                    SimpleNamespace(pid=30, usedGpuMemory=None),
                    SimpleNamespace(pid=10, usedGpuMemory=123456),
                    SimpleNamespace(pid=20, usedGpuMemory=(1 << 64) - 1),
                ],
            }
            if self.after_call:
                self.after_call(name)
            return values.get(name)

        return call


class NVMLTests(unittest.TestCase):
    def setUp(self):
        self.binding = FakeBinding()
        self.session = NVMLProvider(self.binding)
        self.selector = DeviceSelector(SelectorKind.INDEX, 0)

    def test_init_shutdown_exactly_once(self):
        with open_session(self.binding) as provider:
            provider.list_devices()
            self.assertNotIn("nvmlShutdown", [name for name, _ in self.binding.calls])
        names = [name for name, _ in self.binding.calls]
        self.assertEqual(names.count("nvmlInit"), 1)
        self.assertEqual(names.count("nvmlShutdown"), 1)

    def test_init_failure_does_not_shutdown(self):
        self.binding.failures["nvmlInit"] = 12
        with (
            self.assertRaisesRegex(GPUError, "initialize NVML"),
            open_session(self.binding),
        ):
            self.fail("block must not run after failed initialization")
        self.assertEqual([name for name, _ in self.binding.calls], ["nvmlInit"])

    def test_shutdown_failure(self):
        self.binding.failures["nvmlShutdown"] = 3
        with (
            self.assertRaisesRegex(GPUError, "shut down NVML"),
            open_session(self.binding),
        ):
            pass
        self.assertEqual(
            sum(name == "nvmlShutdown" for name, _ in self.binding.calls), 1
        )

    def test_keyboard_interrupt_stops_native_calls_and_shuts_down(self):
        def interrupt(name):
            if name == "nvmlDeviceGetTemperature":
                raise KeyboardInterrupt

        self.binding.after_call = interrupt
        with (
            self.assertRaises(KeyboardInterrupt),
            open_session(self.binding) as provider,
        ):
            provider.device_snapshot(self.selector)
        names = [name for name, _ in self.binding.calls]
        self.assertEqual(names[-2:], ["nvmlDeviceGetTemperature", "nvmlShutdown"])
        self.assertNotIn("nvmlDeviceGetUtilizationRates", names)

    def test_query_failure_shuts_down(self):
        self.binding.failures["nvmlDeviceGetCount"] = 15
        with self.assertRaises(FatalQueryError), open_session(self.binding) as provider:
            provider.list_devices()
        self.assertEqual(self.binding.calls[-1][0], "nvmlShutdown")

    def test_unexpected_exception_shuts_down(self):
        with (
            self.assertRaisesRegex(ValueError, "unexpected"),
            open_session(self.binding),
        ):
            raise ValueError("unexpected")
        self.assertEqual(self.binding.calls[-1][0], "nvmlShutdown")

    def test_device_listing_order_and_partial_failure(self):
        self.binding.failures[("nvmlDeviceGetUUID", (1,))] = 3
        result = self.session.list_devices()
        self.assertEqual([item.device.index for item in result], [0, 1, 2])
        self.assertIsNone(result[0].error)
        self.assertIn("device 1 uuid", str(result[1].error))
        self.assertEqual(result[1].device.pci_bus_id, "0000:01:00.0")
        self.assertIsNone(result[2].error)

    def test_failed_device_handle_keeps_other_devices(self):
        self.binding.failures[("nvmlDeviceGetHandleByIndex", (1,))] = 6
        result = self.session.list_devices()
        self.assertEqual(len(result), 3)
        self.assertIn("get device 1", str(result[1].error))
        self.assertEqual(result[2].device.name, "Example GPU")

    def test_system_partial_failure(self):
        self.binding.failures["nvmlSystemGetDriverVersion"] = 3
        result = self.session.system_info()
        self.assertEqual(result.driver_version, "")
        self.assertEqual(result.cuda_driver_version, 12040)
        self.assertEqual(result.device_count, 3)
        self.assertIn("driver_version", str(result.error))

    def test_snapshot_unsupported_failed_and_valid_metrics(self):
        self.binding.failures["nvmlDeviceGetTemperature"] = 3
        self.binding.failures["nvmlDeviceGetPowerUsage"] = 6
        result = self.session.device_snapshot(self.selector)
        self.assertEqual(result.temperature_celsius.state, MetricState.UNSUPPORTED)
        self.assertEqual(result.power_usage_milliwatts.state, MetricState.FAILED)
        self.assertEqual(result.memory.value.used_bytes, 4000)
        self.assertEqual(result.gpu_utilization_percent.value, 75)
        self.assertEqual(result.memory_utilization_percent.value, 50)
        self.assertEqual(result.fan_speed_percent.value, 0)
        self.assertIn("power usage", str(result.error()))

    def test_lost_device_is_fatal_even_for_metric(self):
        self.binding.failures["nvmlDeviceGetTemperature"] = 15
        with self.assertRaises(FatalQueryError):
            self.session.device_snapshot(self.selector)
        self.assertEqual(self.binding.calls[-1][0], "nvmlDeviceGetTemperature")

    def test_selector_lookup(self):
        for kind, value, fn in (
            (SelectorKind.INDEX, 0, "nvmlDeviceGetHandleByIndex"),
            (SelectorKind.UUID, "GPU-0", "nvmlDeviceGetHandleByUUID"),
            (SelectorKind.PCI_BUS_ID, "0000:01:00.0", "nvmlDeviceGetHandleByPciBusId"),
        ):
            with self.subTest(kind=kind):
                self.binding.calls.clear()
                self.session.device_snapshot(DeviceSelector(kind, value))
                self.assertEqual(self.binding.calls[0], (fn, (value,)))

    def test_process_unavailable_memory_and_pid_order(self):
        result = self.session.compute_processes(self.selector)
        self.assertEqual([process.pid for process in result.processes], [10, 20, 30])
        self.assertEqual(result.processes[0].used_gpu_memory_bytes.value, 123456)
        self.assertEqual(
            result.processes[1].used_gpu_memory_bytes.state, MetricState.UNSUPPORTED
        )
        self.assertEqual(
            result.processes[2].used_gpu_memory_bytes.state, MetricState.UNSUPPORTED
        )
