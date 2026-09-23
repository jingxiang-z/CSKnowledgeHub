package nvml

import (
	"fmt"

	binding "github.com/NVIDIA/go-nvml/pkg/nvml"
	"gpuinfo/internal/gpu"
)

type Session struct{}

func Open() (gpu.Session, error) {
	if ret := binding.Init(); ret != binding.SUCCESS {
		return nil, fmt.Errorf("initialize NVML: %w", ret)
	}
	return &Session{}, nil
}

func (s *Session) Close() error {
	if ret := binding.Shutdown(); ret != binding.SUCCESS {
		return fmt.Errorf("shut down NVML: %w", ret)
	}
	return nil
}
