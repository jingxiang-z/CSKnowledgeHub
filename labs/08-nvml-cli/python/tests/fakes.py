from gpuinfo.gpu import (
    Device,
    DeviceSnapshot,
    Memory,
    Metric,
    MetricState,
    ProcessList,
    SystemInfo,
)


def snapshot():
    return DeviceSnapshot(
        Device(0, "Example GPU", "GPU-0", "0000:01:00.0"),
        Metric(MetricState.AVAILABLE, 42),
        Metric(MetricState.AVAILABLE, 75),
        Metric(MetricState.AVAILABLE, 50),
        Metric(
            MetricState.AVAILABLE, Memory(16_000_000_000, 4_000_000_000, 12_000_000_000)
        ),
        Metric(MetricState.AVAILABLE, 125_000),
        Metric(MetricState.AVAILABLE, 250_000),
        Metric(MetricState.AVAILABLE, 0),
    )


class FakeSession:
    def __init__(self):
        self.info = SystemInfo("driver", 12040, "12", 1)
        self.devices = []
        self.snapshot = snapshot()
        self.processes = ProcessList(0)
        self.close_calls = 0
        self.query_calls = 0
        self.query_error = None
        self.close_error = None
        self.selector = None
        self.on_snapshot = None

    def _query(self):
        self.query_calls += 1
        if self.query_error:
            raise self.query_error

    def system_info(self):
        self._query()
        return self.info

    def list_devices(self):
        self._query()
        return self.devices

    def device_snapshot(self, selector):
        self._query()
        self.selector = selector
        return self.on_snapshot(selector) if self.on_snapshot else self.snapshot

    def compute_processes(self, selector):
        self._query()
        self.selector = selector
        return self.processes

    def close(self):
        self.close_calls += 1
        if self.close_error:
            raise self.close_error

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
