package nvml

import (
	"context"
	"errors"
	"fmt"

	binding "github.com/NVIDIA/go-nvml/pkg/nvml"
	"gpuinfo/internal/gpu"
)

func (s *Session) ListDevices(ctx context.Context) ([]gpu.DeviceResult, error) {
	if err := ctx.Err(); err != nil {
		return nil, err
	}
	count, ret := binding.DeviceGetCount()
	if ret != binding.SUCCESS {
		return nil, fmt.Errorf("get device count: %w", ret)
	}
	devices := make([]gpu.DeviceResult, 0, count)
	for i := 0; i < count; i++ {
		if err := ctx.Err(); err != nil {
			return devices, err
		}
		result, err := s.readDevice(ctx, i)
		if err != nil {
			return devices, err
		}
		devices = append(devices, result)
	}
	if err := ctx.Err(); err != nil {
		return devices, err
	}
	return devices, nil
}

func (s *Session) readDevice(ctx context.Context, i int) (gpu.DeviceResult, error) {
	if err := ctx.Err(); err != nil {
		return gpu.DeviceResult{}, err
	}
	handle, ret := binding.DeviceGetHandleByIndex(i)
	if err := ctx.Err(); err != nil {
		return gpu.DeviceResult{}, err
	}
	if ret != binding.SUCCESS {
		return gpu.DeviceResult{
			Device: gpu.Device{Index: i},
			Err:    fmt.Errorf("get device %d: %w", i, ret),
		}, nil
	}
	return readDeviceFields(ctx, handle, i)
}

func readDeviceFields(ctx context.Context, handle binding.Device, index int) (gpu.DeviceResult, error) {
	result := gpu.DeviceResult{Device: gpu.Device{Index: index}}
	if err := ctx.Err(); err != nil {
		return result, err
	}
	name, ret := handle.GetName()
	if ret == binding.SUCCESS {
		result.Device.Name = name
	} else {
		result.Err = errors.Join(result.Err, fmt.Errorf("get device %d name: %w", index, ret))
	}

	if err := ctx.Err(); err != nil {
		return result, err
	}
	uuid, ret := handle.GetUUID()
	if ret == binding.SUCCESS {
		result.Device.UUID = uuid
	} else {
		result.Err = errors.Join(result.Err, fmt.Errorf("get device %d UUID: %w", index, ret))
	}

	if err := ctx.Err(); err != nil {
		return result, err
	}
	pci, ret := handle.GetPciInfo()
	if ret == binding.SUCCESS {
		result.Device.PciBusID = cString(pci.BusId[:])
	} else {
		result.Err = errors.Join(result.Err, fmt.Errorf("get device %d PCI info: %w", index, ret))
	}
	return result, ctx.Err()
}

func cString(value []int8) string {
	result := make([]byte, 0, len(value))
	for _, b := range value {
		if b == 0 {
			break
		}
		result = append(result, byte(b))
	}
	return string(result)
}
