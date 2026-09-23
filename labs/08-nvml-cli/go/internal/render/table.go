package render

import (
	"fmt"
	"io"
	"strconv"
	"text/tabwriter"

	"gpuinfo/internal/gpu"
)

func DeviceTable(dst io.Writer, results []gpu.DeviceResult) error {
	out := tabwriter.NewWriter(dst, 0, 0, 2, ' ', 0)
	fmt.Fprintln(out, "INDEX\tNAME\tUUID\tPCI BUS ID")
	for _, result := range results {
		device := result.Device
		fmt.Fprintf(out, "%d\t%s\t%s\t%s\n", device.Index, device.Name, device.UUID, device.PciBusID)
	}
	return out.Flush()
}

func SystemTable(dst io.Writer, info gpu.SystemInfo) error {
	out := tabwriter.NewWriter(dst, 0, 0, 2, ' ', 0)
	fmt.Fprintf(out, "DRIVER VERSION\t%s\n", info.DriverVersion)
	fmt.Fprintf(out, "CUDA DRIVER VERSION\t%s\n", cudaDriverVersion(info.CUDADriverVersion))
	fmt.Fprintf(out, "NVML VERSION\t%s\n", info.NVMLVersion)
	fmt.Fprintf(out, "DEVICE COUNT\t%d\n", info.DeviceCount)
	return out.Flush()
}

func SnapshotTable(dst io.Writer, snapshot gpu.DeviceSnapshot) error {
	out := tabwriter.NewWriter(dst, 0, 0, 2, ' ', 0)
	fmt.Fprintf(out, "INDEX\t%d\n", snapshot.Device.Index)
	fmt.Fprintf(out, "NAME\t%s\n", snapshot.Device.Name)
	fmt.Fprintf(out, "UUID\t%s\n", snapshot.Device.UUID)
	fmt.Fprintf(out, "PCI BUS ID\t%s\n", snapshot.Device.PciBusID)
	fmt.Fprintf(out, "TEMPERATURE (C)\t%s\n", uint32Metric(snapshot.TemperatureCelsius))
	fmt.Fprintf(out, "GPU UTILIZATION (%%)\t%s\n", uint32Metric(snapshot.GPUUtilizationPercent))
	fmt.Fprintf(out, "MEMORY UTILIZATION (%%)\t%s\n", uint32Metric(snapshot.MemoryUtilizationPercent))
	fmt.Fprintf(out, "MEMORY TOTAL (BYTES)\t%s\n", memoryMetric(snapshot.Memory, func(memory gpu.Memory) uint64 { return memory.TotalBytes }))
	fmt.Fprintf(out, "MEMORY USED (BYTES)\t%s\n", memoryMetric(snapshot.Memory, func(memory gpu.Memory) uint64 { return memory.UsedBytes }))
	fmt.Fprintf(out, "MEMORY FREE (BYTES)\t%s\n", memoryMetric(snapshot.Memory, func(memory gpu.Memory) uint64 { return memory.FreeBytes }))
	fmt.Fprintf(out, "POWER USAGE (mW)\t%s\n", uint32Metric(snapshot.PowerUsageMilliwatts))
	fmt.Fprintf(out, "POWER LIMIT (mW)\t%s\n", uint32Metric(snapshot.PowerLimitMilliwatts))
	fmt.Fprintf(out, "FAN SPEED (%%)\t%s\n", uint32Metric(snapshot.FanSpeedPercent))
	return out.Flush()
}

func uint32Metric(metric gpu.Metric[uint32]) string {
	if metric.State != gpu.MetricAvailable {
		return string(metric.State)
	}
	return strconv.FormatUint(uint64(metric.Value), 10)
}

func memoryMetric(metric gpu.Metric[gpu.Memory], value func(gpu.Memory) uint64) string {
	if metric.State != gpu.MetricAvailable {
		return string(metric.State)
	}
	return strconv.FormatUint(value(metric.Value), 10)
}

func cudaDriverVersion(version int) string {
	if version <= 0 {
		return "unknown"
	}
	return fmt.Sprintf("%d.%d", version/1000, (version%1000)/10)
}

func ProcessTable(dst io.Writer, result gpu.ProcessList) error {
	out := tabwriter.NewWriter(dst, 0, 0, 2, ' ', 0)
	fmt.Fprintf(out, "GPU INDEX\t%d\n", result.DeviceIndex)
	if len(result.Processes) == 0 {
		fmt.Fprintln(out, "No active compute processes")
		return out.Flush()
	}
	fmt.Fprintln(out, "PID\tGPU MEMORY (BYTES)")
	for _, process := range result.Processes {
		memory := "unsupported"
		if process.UsedGPUMemoryBytes.State == gpu.MetricAvailable {
			memory = strconv.FormatUint(process.UsedGPUMemoryBytes.Value, 10)
		}
		fmt.Fprintf(out, "%d\t%s\n", process.PID, memory)
	}
	return out.Flush()
}
