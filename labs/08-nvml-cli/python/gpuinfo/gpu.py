"""Domain values and the provider contract; no NVML or CLI dependencies."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Generic, Protocol, TypeVar

from .errors import combine

T = TypeVar("T")


class MetricState(str, Enum):
    AVAILABLE = "available"
    UNSUPPORTED = "unsupported"
    FAILED = "failed"


@dataclass(frozen=True)
class Metric(Generic[T]):
    state: MetricState
    value: T | None = None
    error: Exception | None = None


class SelectorKind(str, Enum):
    INDEX = "index"
    UUID = "uuid"
    PCI_BUS_ID = "pci_bus_id"


@dataclass(frozen=True)
class DeviceSelector:
    kind: SelectorKind
    value: int | str


@dataclass(frozen=True)
class Device:
    index: int
    name: str = ""
    uuid: str = ""
    pci_bus_id: str = ""


@dataclass(frozen=True)
class DeviceResult:
    device: Device
    error: Exception | None = None


@dataclass(frozen=True)
class SystemInfo:
    driver_version: str = ""
    cuda_driver_version: int = 0
    nvml_version: str = ""
    device_count: int = 0
    error: Exception | None = None


@dataclass(frozen=True)
class Memory:
    total_bytes: int
    used_bytes: int
    free_bytes: int


@dataclass(frozen=True)
class DeviceSnapshot:
    device: Device
    temperature_celsius: Metric[int]
    gpu_utilization_percent: Metric[int]
    memory_utilization_percent: Metric[int]
    memory: Metric[Memory]
    power_usage_milliwatts: Metric[int]
    power_limit_milliwatts: Metric[int]
    fan_speed_percent: Metric[int]
    device_error: Exception | None = None

    def error(self) -> Exception | None:
        return combine(
            self.device_error,
            *(
                getattr(self, name).error
                for name in SNAPSHOT_METRICS
                if getattr(self, name).state == MetricState.FAILED
            ),
        )


SNAPSHOT_METRICS = (
    "temperature_celsius",
    "gpu_utilization_percent",
    "memory_utilization_percent",
    "memory",
    "power_usage_milliwatts",
    "power_limit_milliwatts",
    "fan_speed_percent",
)


@dataclass(frozen=True)
class Process:
    pid: int
    used_gpu_memory_bytes: Metric[int]


@dataclass(frozen=True)
class ProcessList:
    device_index: int
    processes: list[Process] = field(default_factory=list)


class Provider(Protocol):
    def system_info(self) -> SystemInfo: ...
    def list_devices(self) -> list[DeviceResult]: ...
    def device_snapshot(self, selector: DeviceSelector) -> DeviceSnapshot: ...
    def compute_processes(self, selector: DeviceSelector) -> ProcessList: ...
