package nvml

import (
	"context"
	"errors"
	"gpuinfo/internal/gpu"
	"testing"
)

func TestCanceledContextStopsComputeProcessesBeforeNVMLCalls(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	session := &Session{}
	if _, err := session.ComputeProcesses(ctx, gpu.IndexSelector(0)); !errors.Is(err, context.Canceled) {
		t.Fatalf("ComputeProcesses error = %v", err)
	}
}
