package render

import (
	"encoding/json"
	"io"

	"gpuinfo/internal/gpu"
)

type jsonDevice struct {
	Index    int    `json:"index"`
	Name     string `json:"name"`
	UUID     string `json:"uuid"`
	PCIBusID string `json:"pci_bus_id"`
}

type jsonDeviceResult struct {
	Device jsonDevice `json:"device"`
	Error  string     `json:"error,omitempty"`
}

type jsonMetric[T any] struct {
	State gpu.MetricState `json:"state"`
	Value *T              `json:"value,omitempty"`
	Error string          `json:"error,omitempty"`
}

type jsonMemory struct {
	TotalBytes uint64 `json:"total_bytes"`
	UsedBytes  uint64 `json:"used_bytes"`
	FreeBytes  uint64 `json:"free_bytes"`
}

type jsonSnapshot struct {
	Device                   jsonDevice             `json:"device"`
	DeviceError              string                 `json:"device_error,omitempty"`
	TemperatureCelsius       jsonMetric[uint32]     `json:"temperature_celsius"`
	GPUUtilizationPercent    jsonMetric[uint32]     `json:"gpu_utilization_percent"`
	MemoryUtilizationPercent jsonMetric[uint32]     `json:"memory_utilization_percent"`
	Memory                   jsonMetric[jsonMemory] `json:"memory"`
	PowerUsageMilliwatts     jsonMetric[uint32]     `json:"power_usage_milliwatts"`
	PowerLimitMilliwatts     jsonMetric[uint32]     `json:"power_limit_milliwatts"`
	FanSpeedPercent          jsonMetric[uint32]     `json:"fan_speed_percent"`
}

func SystemJSON(dst io.Writer, info gpu.SystemInfo, queryErr error) error {
	return writeJSON(dst, struct {
		DriverVersion     string `json:"driver_version"`
		CUDADriverVersion string `json:"cuda_driver_version"`
		NVMLVersion       string `json:"nvml_version"`
		DeviceCount       int    `json:"device_count"`
		Error             string `json:"error,omitempty"`
	}{
		DriverVersion:     info.DriverVersion,
		CUDADriverVersion: cudaDriverVersion(info.CUDADriverVersion),
		NVMLVersion:       info.NVMLVersion,
		DeviceCount:       info.DeviceCount,
		Error:             errorText(queryErr),
	})
}

func DevicesJSON(dst io.Writer, results []gpu.DeviceResult) error {
	devices := make([]jsonDeviceResult, 0, len(results))
	for _, result := range results {
		devices = append(devices, jsonDeviceResult{
			Device: jsonDeviceOf(result.Device),
			Error:  errorText(result.Err),
		})
	}
	return writeJSON(dst, devices)
}

func SnapshotJSON(dst io.Writer, snapshot gpu.DeviceSnapshot) error {
	return writeJSON(dst, jsonSnapshotOf(snapshot))
}

// WatchJSON writes one complete JSON object per sample (JSON Lines).
func WatchJSON(dst io.Writer, sample int, snapshot gpu.DeviceSnapshot) error {
	return writeJSON(dst, struct {
		Sample   int          `json:"sample"`
		Snapshot jsonSnapshot `json:"snapshot"`
	}{Sample: sample, Snapshot: jsonSnapshotOf(snapshot)})
}

func ProcessesJSON(dst io.Writer, result gpu.ProcessList) error {
	type jsonProcess struct {
		PID                uint32             `json:"pid"`
		UsedGPUMemoryBytes jsonMetric[uint64] `json:"used_gpu_memory_bytes"`
	}
	processes := make([]jsonProcess, 0, len(result.Processes))
	for _, process := range result.Processes {
		processes = append(processes, jsonProcess{
			PID:                process.PID,
			UsedGPUMemoryBytes: jsonMetricOf(process.UsedGPUMemoryBytes),
		})
	}
	return writeJSON(dst, struct {
		DeviceIndex int           `json:"device_index"`
		Processes   []jsonProcess `json:"processes"`
	}{DeviceIndex: result.DeviceIndex, Processes: processes})
}

func jsonDeviceOf(device gpu.Device) jsonDevice {
	return jsonDevice{
		Index:    device.Index,
		Name:     device.Name,
		UUID:     device.UUID,
		PCIBusID: device.PciBusID,
	}
}

func jsonSnapshotOf(snapshot gpu.DeviceSnapshot) jsonSnapshot {
	memory := jsonMetric[jsonMemory]{State: snapshot.Memory.State, Error: errorText(snapshot.Memory.Err)}
	if snapshot.Memory.State == gpu.MetricAvailable {
		memory.Value = &jsonMemory{
			TotalBytes: snapshot.Memory.Value.TotalBytes,
			UsedBytes:  snapshot.Memory.Value.UsedBytes,
			FreeBytes:  snapshot.Memory.Value.FreeBytes,
		}
	}
	return jsonSnapshot{
		Device:                   jsonDeviceOf(snapshot.Device),
		DeviceError:              errorText(snapshot.DeviceErr),
		TemperatureCelsius:       jsonMetricOf(snapshot.TemperatureCelsius),
		GPUUtilizationPercent:    jsonMetricOf(snapshot.GPUUtilizationPercent),
		MemoryUtilizationPercent: jsonMetricOf(snapshot.MemoryUtilizationPercent),
		Memory:                   memory,
		PowerUsageMilliwatts:     jsonMetricOf(snapshot.PowerUsageMilliwatts),
		PowerLimitMilliwatts:     jsonMetricOf(snapshot.PowerLimitMilliwatts),
		FanSpeedPercent:          jsonMetricOf(snapshot.FanSpeedPercent),
	}
}

func jsonMetricOf[T any](metric gpu.Metric[T]) jsonMetric[T] {
	result := jsonMetric[T]{State: metric.State, Error: errorText(metric.Err)}
	if metric.State == gpu.MetricAvailable {
		result.Value = &metric.Value
	}
	return result
}

func errorText(err error) string {
	if err == nil {
		return ""
	}
	return err.Error()
}

func writeJSON(dst io.Writer, value any) error {
	return json.NewEncoder(dst).Encode(value)
}
