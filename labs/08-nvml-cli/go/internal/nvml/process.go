package nvml

import (
	"context"
	"fmt"
	"sort"

	binding "github.com/NVIDIA/go-nvml/pkg/nvml"
	"gpuinfo/internal/gpu"
)

func (s *Session) ComputeProcesses(ctx context.Context, selector gpu.DeviceSelector) (gpu.ProcessList, error) {
	handle, err := deviceHandle(ctx, selector)
	if err != nil {
		return gpu.ProcessList{}, err
	}

	index, ret := handle.GetIndex()
	if err := ctx.Err(); err != nil {
		return gpu.ProcessList{}, err
	}
	if ret != binding.SUCCESS {
		return gpu.ProcessList{}, fmt.Errorf("get device index for %s: %w", selector, ret)
	}

	if err := ctx.Err(); err != nil {
		return gpu.ProcessList{}, err
	}
	infos, ret := handle.GetComputeRunningProcesses()
	if err := ctx.Err(); err != nil {
		return gpu.ProcessList{}, err
	}
	if ret != binding.SUCCESS {
		return gpu.ProcessList{}, fmt.Errorf("get device %d compute processes: %w", index, ret)
	}

	result := gpu.ProcessList{DeviceIndex: index, Processes: make([]gpu.Process, 0, len(infos))}
	for _, info := range infos {
		if err := ctx.Err(); err != nil {
			return gpu.ProcessList{}, err
		}
		process := gpu.Process{PID: info.Pid}
		if info.UsedGpuMemory == ^uint64(0) {
			// NVML_VALUE_NOT_AVAILABLE is an all-ones unsigned memory value.
			process.UsedGPUMemoryBytes.State = gpu.MetricUnsupported
		} else {
			process.UsedGPUMemoryBytes = gpu.Metric[uint64]{
				Value: info.UsedGpuMemory,
				State: gpu.MetricAvailable,
			}
		}
		result.Processes = append(result.Processes, process)
	}
	sort.Slice(result.Processes, func(i, j int) bool {
		return result.Processes[i].PID < result.Processes[j].PID
	})
	return result, nil
}
