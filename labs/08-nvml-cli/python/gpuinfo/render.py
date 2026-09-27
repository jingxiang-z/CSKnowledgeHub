"""Domain-to-table and domain-to-JSON translation."""

import json
from dataclasses import fields, is_dataclass
from enum import Enum
from typing import Any, TextIO

from .gpu import (
    DeviceResult,
    DeviceSnapshot,
    Metric,
    MetricState,
    ProcessList,
    SystemInfo,
)


def cuda_version(version: int) -> str:
    return f"{version // 1000}.{version % 1000 // 10}" if version > 0 else "unknown"


def json_value(value: Any) -> Any:
    if isinstance(value, Metric):
        result = {"state": value.state.value}
        if value.state == MetricState.AVAILABLE:
            result["value"] = json_value(value.value)
        if value.error is not None:
            result["error"] = str(value.error)
        return result
    if isinstance(value, Exception):
        return str(value)
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        result = {
            item.name: json_value(getattr(value, item.name))
            for item in fields(value)
            if getattr(value, item.name) is not None
        }
        if isinstance(value, SystemInfo):
            result["cuda_driver_version"] = cuda_version(value.cuda_driver_version)
        return result
    if isinstance(value, list):
        return [json_value(item) for item in value]
    if isinstance(value, dict):
        return {key: json_value(item) for key, item in value.items()}
    return value


def write_json(out: TextIO, value: Any) -> None:
    out.write(
        json.dumps(json_value(value), separators=(",", ":"), ensure_ascii=False) + "\n"
    )
    out.flush()


def _table(out: TextIO, rows: list[list[Any]]) -> None:
    text = [[str(cell) for cell in row] for row in rows]
    widths = [
        max(len(row[column]) if column < len(row) else 0 for row in text)
        for column in range(max(map(len, text), default=0))
    ]
    out.writelines(
        "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)).rstrip() + "\n"
        for row in text
    )
    out.flush()


def _metric(value: Metric, memory_field: str | None = None) -> str:
    if value.state != MetricState.AVAILABLE:
        return value.state.value
    return str(getattr(value.value, memory_field) if memory_field else value.value)


def system_table(out: TextIO, info: SystemInfo) -> None:
    _table(
        out,
        [
            ["DRIVER VERSION", info.driver_version],
            ["CUDA DRIVER VERSION", cuda_version(info.cuda_driver_version)],
            ["NVML VERSION", info.nvml_version],
            ["DEVICE COUNT", info.device_count],
        ],
    )


def devices_table(out: TextIO, results: list[DeviceResult]) -> None:
    _table(
        out,
        [
            ["INDEX", "NAME", "UUID", "PCI BUS ID"],
            *[
                [
                    item.device.index,
                    item.device.name,
                    item.device.uuid,
                    item.device.pci_bus_id,
                ]
                for item in results
            ],
        ],
    )


def snapshot_table(out: TextIO, snapshot: DeviceSnapshot) -> None:
    device = snapshot.device
    rows = [
        ["INDEX", device.index],
        ["NAME", device.name],
        ["UUID", device.uuid],
        ["PCI BUS ID", device.pci_bus_id],
    ]
    for label, name in (
        ("TEMPERATURE (C)", "temperature_celsius"),
        ("GPU UTILIZATION (%)", "gpu_utilization_percent"),
        ("MEMORY UTILIZATION (%)", "memory_utilization_percent"),
    ):
        rows.append([label, _metric(getattr(snapshot, name))])
    for name in ("total_bytes", "used_bytes", "free_bytes"):
        rows.append(
            [
                f"MEMORY {name.split('_')[0].upper()} (BYTES)",
                _metric(snapshot.memory, name),
            ]
        )
    for label, name in (
        ("POWER USAGE (mW)", "power_usage_milliwatts"),
        ("POWER LIMIT (mW)", "power_limit_milliwatts"),
        ("FAN SPEED (%)", "fan_speed_percent"),
    ):
        rows.append([label, _metric(getattr(snapshot, name))])
    _table(out, rows)


def processes_table(out: TextIO, result: ProcessList) -> None:
    rows = [["GPU INDEX", result.device_index]]
    if not result.processes:
        rows.append(["No active compute processes"])
    else:
        rows.append(["PID", "GPU MEMORY (BYTES)"])
        rows.extend(
            [process.pid, _metric(process.used_gpu_memory_bytes)]
            for process in result.processes
        )
    _table(out, rows)
