package nvml

import (
	"context"
	"errors"
	"gpuinfo/internal/gpu"
	"testing"
)

func TestCanceledContextStopsDeviceSnapshotBeforeNVMLCalls(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	session := &Session{}
	if _, err := session.DeviceSnapshot(ctx, gpu.IndexSelector(0)); !errors.Is(err, context.Canceled) {
		t.Fatalf("DeviceSnapshot error = %v", err)
	}
}
