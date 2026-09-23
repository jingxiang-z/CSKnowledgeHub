package nvml

import (
	"context"
	"errors"
	"fmt"

	binding "github.com/NVIDIA/go-nvml/pkg/nvml"
	"gpuinfo/internal/gpu"
)

func (s *Session) SystemInfo(ctx context.Context) (gpu.SystemInfo, error) {
	var info gpu.SystemInfo
	var queryErr error

	if err := ctx.Err(); err != nil {
		return info, err
	}
	driverVersion, ret := binding.SystemGetDriverVersion()
	if ret == binding.SUCCESS {
		info.DriverVersion = driverVersion
	} else {
		queryErr = errors.Join(queryErr, fmt.Errorf("get NVIDIA driver version: %w", ret))
	}

	if err := ctx.Err(); err != nil {
		return info, errors.Join(queryErr, err)
	}
	cudaDriverVersion, ret := binding.SystemGetCudaDriverVersion_v2()
	if ret == binding.SUCCESS {
		info.CUDADriverVersion = cudaDriverVersion
	} else {
		queryErr = errors.Join(queryErr, fmt.Errorf("get CUDA driver version: %w", ret))
	}

	if err := ctx.Err(); err != nil {
		return info, errors.Join(queryErr, err)
	}
	nvmlVersion, ret := binding.SystemGetNVMLVersion()
	if ret == binding.SUCCESS {
		info.NVMLVersion = nvmlVersion
	} else {
		queryErr = errors.Join(queryErr, fmt.Errorf("get NVML version: %w", ret))
	}

	if err := ctx.Err(); err != nil {
		return info, errors.Join(queryErr, err)
	}
	deviceCount, ret := binding.DeviceGetCount()
	if ret == binding.SUCCESS {
		info.DeviceCount = deviceCount
	} else {
		queryErr = errors.Join(queryErr, fmt.Errorf("get device count: %w", ret))
	}

	return info, errors.Join(queryErr, ctx.Err())
}
