"""NVML adapter: binding handles and exceptions stay inside this module."""

from collections.abc import Callable, Generator
from contextlib import contextmanager
from dataclasses import replace
from typing import Any, TypeVar

from .errors import FatalQueryError, GPUError, QueryError, combine
from .gpu import (
    Device,
    DeviceResult,
    DeviceSelector,
    DeviceSnapshot,
    Memory,
    Metric,
    MetricState,
    Process,
    ProcessList,
    SelectorKind,
    SystemInfo,
)

T = TypeVar("T")


def _text(value: str | bytes) -> str:
    return (
        value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value
    )


class NVMLProvider:
    def __init__(self, binding: Any):
        self._binding = binding

    def _call(self, operation: str, fn: Callable[[], T]) -> T:
        try:
            value = fn()
        except self._binding.NVMLError as error:
            fatal_codes = (
                self._binding.NVML_ERROR_GPU_IS_LOST,
                self._binding.NVML_ERROR_UNINITIALIZED,
                self._binding.NVML_ERROR_LIBRARY_NOT_FOUND,
            )
            error_type = FatalQueryError if error.value in fatal_codes else QueryError
            raise error_type(f"{operation}: {error}") from error
        return value

    def _metric(self, operation: str, fn: Callable[[], T]) -> Metric[T]:
        try:
            return Metric(MetricState.AVAILABLE, self._call(operation, fn))
        except FatalQueryError:
            raise
        except QueryError as error:
            state = (
                MetricState.UNSUPPORTED
                if error.__cause__.value == self._binding.NVML_ERROR_NOT_SUPPORTED
                else MetricState.FAILED
            )
            return Metric(state, error=error)

    def system_info(self) -> SystemInfo:
        b = self._binding
        values: dict[str, Any] = {}
        errors = []
        for name, fn in (
            ("driver_version", lambda: _text(b.nvmlSystemGetDriverVersion())),
            ("cuda_driver_version", b.nvmlSystemGetCudaDriverVersion_v2),
            ("nvml_version", lambda: _text(b.nvmlSystemGetNVMLVersion())),
            ("device_count", b.nvmlDeviceGetCount),
        ):
            try:
                values[name] = self._call(f"get {name}", fn)
            except FatalQueryError:
                raise
            except QueryError as error:
                errors.append(error)
        return SystemInfo(**values, error=combine(*errors))

    def _device(self, handle: Any, index: int) -> DeviceResult:
        b = self._binding
        values: dict[str, Any] = {"index": index}
        errors = []
        for name, fn in (
            ("name", lambda: _text(b.nvmlDeviceGetName(handle))),
            ("uuid", lambda: _text(b.nvmlDeviceGetUUID(handle))),
            ("pci_bus_id", lambda: _text(b.nvmlDeviceGetPciInfo(handle).busId)),
        ):
            try:
                values[name] = self._call(f"get device {index} {name}", fn)
            except FatalQueryError:
                raise
            except QueryError as error:
                errors.append(error)
        return DeviceResult(Device(**values), combine(*errors))

    def list_devices(self) -> list[DeviceResult]:
        b = self._binding
        count = self._call("get device count", b.nvmlDeviceGetCount)
        results = []
        for index in range(count):
            try:
                handle = self._call(
                    f"get device {index}",
                    lambda index=index: b.nvmlDeviceGetHandleByIndex(index),
                )
                results.append(self._device(handle, index))
            except FatalQueryError:
                raise
            except QueryError as error:
                results.append(DeviceResult(Device(index), error))
        return results

    def _handle(self, selector: DeviceSelector) -> Any:
        b = self._binding
        lookup = {
            SelectorKind.INDEX: b.nvmlDeviceGetHandleByIndex,
            SelectorKind.UUID: b.nvmlDeviceGetHandleByUUID,
            SelectorKind.PCI_BUS_ID: b.nvmlDeviceGetHandleByPciBusId,
        }
        if selector.kind not in lookup:
            raise GPUError("invalid device selector")
        return self._call(
            f"resolve device by {selector.kind.value} {selector.value}",
            lambda: lookup[selector.kind](selector.value),
        )

    def device_snapshot(self, selector: DeviceSelector) -> DeviceSnapshot:
        b = self._binding
        handle = self._handle(selector)
        index = self._call("get device index", lambda: b.nvmlDeviceGetIndex(handle))
        identity = self._device(handle, index)
        prefix = f"get device {index}"
        temperature = self._metric(
            f"{prefix} temperature",
            lambda: b.nvmlDeviceGetTemperature(handle, b.NVML_TEMPERATURE_GPU),
        )
        utilization = self._metric(
            f"{prefix} utilization",
            lambda: b.nvmlDeviceGetUtilizationRates(handle),
        )
        gpu_util = (
            replace(utilization, value=utilization.value.gpu)
            if utilization.value is not None
            else utilization
        )
        memory_util = (
            replace(utilization, value=utilization.value.memory)
            if utilization.value is not None
            else utilization
        )
        memory = self._metric(
            f"{prefix} memory", lambda: b.nvmlDeviceGetMemoryInfo(handle)
        )
        if memory.value is not None:
            memory = replace(
                memory,
                value=Memory(memory.value.total, memory.value.used, memory.value.free),
            )
        return DeviceSnapshot(
            device=identity.device,
            device_error=identity.error,
            temperature_celsius=temperature,
            gpu_utilization_percent=gpu_util,
            memory_utilization_percent=memory_util,
            memory=memory,
            power_usage_milliwatts=self._metric(
                f"{prefix} power usage",
                lambda: b.nvmlDeviceGetPowerUsage(handle),
            ),
            power_limit_milliwatts=self._metric(
                f"{prefix} enforced power limit",
                lambda: b.nvmlDeviceGetEnforcedPowerLimit(handle),
            ),
            fan_speed_percent=self._metric(
                f"{prefix} fan speed", lambda: b.nvmlDeviceGetFanSpeed(handle)
            ),
        )

    def compute_processes(self, selector: DeviceSelector) -> ProcessList:
        b = self._binding
        handle = self._handle(selector)
        index = self._call("get device index", lambda: b.nvmlDeviceGetIndex(handle))
        infos = self._call(
            f"get device {index} compute processes",
            lambda: b.nvmlDeviceGetComputeRunningProcesses(handle),
        )
        processes = []
        for info in infos:
            value = info.usedGpuMemory
            unavailable = value is None or value == (1 << 64) - 1
            memory = (
                Metric(MetricState.UNSUPPORTED)
                if unavailable
                else Metric(MetricState.AVAILABLE, value)
            )
            processes.append(Process(info.pid, memory))
        return ProcessList(index, sorted(processes, key=lambda process: process.pid))


@contextmanager
def open_session(binding: Any = None) -> Generator[NVMLProvider, None, None]:
    """Own initialization and shutdown for the lifetime of a with block."""
    if binding is None:
        try:
            import pynvml as binding
        except ImportError as error:
            raise GPUError(
                "install the NVML binding with: pip install nvidia-ml-py"
            ) from error
    try:
        binding.nvmlInit()
    except binding.NVMLError as error:
        raise GPUError(f"initialize NVML: {error}") from error
    try:
        yield NVMLProvider(binding)
    finally:
        try:
            binding.nvmlShutdown()
        except binding.NVMLError as error:
            raise GPUError(f"shut down NVML: {error}") from error
