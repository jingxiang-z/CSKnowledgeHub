package nvml

import (
	"context"
	"fmt"

	binding "github.com/NVIDIA/go-nvml/pkg/nvml"
	"gpuinfo/internal/gpu"
)

func (s *Session) DeviceSnapshot(ctx context.Context, selector gpu.DeviceSelector) (gpu.DeviceSnapshot, error) {
	handle, err := deviceHandle(ctx, selector)
	if err != nil {
		return gpu.DeviceSnapshot{}, err
	}

	index, ret := handle.GetIndex()
	if err := ctx.Err(); err != nil {
		return gpu.DeviceSnapshot{}, err
	}
	if ret != binding.SUCCESS {
		return gpu.DeviceSnapshot{}, fmt.Errorf("get device index for %s: %w", selector, ret)
	}

	identity, err := readDeviceFields(ctx, handle, index)
	if err != nil {
		return gpu.DeviceSnapshot{}, err
	}
	snapshot := gpu.DeviceSnapshot{
		Device:    identity.Device,
		DeviceErr: identity.Err,
	}

	if err := ctx.Err(); err != nil {
		return gpu.DeviceSnapshot{}, err
	}
	temperature, ret := handle.GetTemperature(binding.TEMPERATURE_GPU)
	snapshot.TemperatureCelsius = metric(temperature, ret, fmt.Sprintf("get device %d temperature", index))

	if err := ctx.Err(); err != nil {
		return gpu.DeviceSnapshot{}, err
	}
	utilization, ret := handle.GetUtilizationRates()
	snapshot.GPUUtilizationPercent = metric(utilization.Gpu, ret, fmt.Sprintf("get device %d GPU utilization", index))
	snapshot.MemoryUtilizationPercent = metric(utilization.Memory, ret, fmt.Sprintf("get device %d memory utilization", index))

	if err := ctx.Err(); err != nil {
		return gpu.DeviceSnapshot{}, err
	}
	memory, ret := handle.GetMemoryInfo()
	snapshot.Memory = metric(gpu.Memory{
		TotalBytes: memory.Total,
		UsedBytes:  memory.Used,
		FreeBytes:  memory.Free,
	}, ret, fmt.Sprintf("get device %d memory information", index))

	if err := ctx.Err(); err != nil {
		return gpu.DeviceSnapshot{}, err
	}
	powerUsage, ret := handle.GetPowerUsage()
	snapshot.PowerUsageMilliwatts = metric(powerUsage, ret, fmt.Sprintf("get device %d power usage", index))

	if err := ctx.Err(); err != nil {
		return gpu.DeviceSnapshot{}, err
	}
	powerLimit, ret := handle.GetEnforcedPowerLimit()
	snapshot.PowerLimitMilliwatts = metric(powerLimit, ret, fmt.Sprintf("get device %d enforced power limit", index))

	if err := ctx.Err(); err != nil {
		return gpu.DeviceSnapshot{}, err
	}
	fanSpeed, ret := handle.GetFanSpeed()
	snapshot.FanSpeedPercent = metric(fanSpeed, ret, fmt.Sprintf("get device %d fan speed", index))

	if err := ctx.Err(); err != nil {
		return gpu.DeviceSnapshot{}, err
	}
	return snapshot, nil
}

func deviceHandle(ctx context.Context, selector gpu.DeviceSelector) (binding.Device, error) {
	if err := ctx.Err(); err != nil {
		return nil, err
	}
	var handle binding.Device
	var ret binding.Return

	switch selector.Kind {
	case gpu.SelectorByIndex:
		handle, ret = binding.DeviceGetHandleByIndex(selector.Index)
	case gpu.SelectorByUUID:
		handle, ret = binding.DeviceGetHandleByUUID(selector.Value)
	case gpu.SelectorByPCIBusID:
		handle, ret = binding.DeviceGetHandleByPciBusId(selector.Value)
	default:
		return nil, fmt.Errorf("invalid device selector")
	}
	if err := ctx.Err(); err != nil {
		return nil, err
	}
	if ret != binding.SUCCESS {
		return nil, fmt.Errorf("resolve device by %s: %w", selector, ret)
	}
	return handle, nil
}

func metric[T any](value T, ret binding.Return, operation string) gpu.Metric[T] {
	if ret == binding.SUCCESS {
		return gpu.Metric[T]{Value: value, State: gpu.MetricAvailable}
	}
	err := fmt.Errorf("%s: %w", operation, ret)
	if ret == binding.ERROR_NOT_SUPPORTED {
		return gpu.Metric[T]{State: gpu.MetricUnsupported, Err: err}
	}
	return gpu.Metric[T]{State: gpu.MetricFailed, Err: err}
}
