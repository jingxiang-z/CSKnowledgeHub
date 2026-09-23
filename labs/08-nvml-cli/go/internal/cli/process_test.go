package cli

import (
	"context"
	"gpuinfo/internal/gpu"
	"testing"
)

func TestProcessAliasJSON(t *testing.T) {
	session := &fakeSession{processes: gpu.ProcessList{DeviceIndex: 0, Processes: []gpu.Process{
		{PID: 123, UsedGPUMemoryBytes: gpu.Metric[uint64]{State: gpu.MetricUnsupported}},
	}}}
	stdout, _, err, _ := executeFake(context.Background(), session, "processes", "0", "--output", "json")
	if err != nil || session.closeCalls != 1 {
		t.Fatalf("execute: err=%v closes=%d", err, session.closeCalls)
	}
	if stdout != "{\"device_index\":0,\"processes\":[{\"pid\":123,\"used_gpu_memory_bytes\":{\"state\":\"unsupported\"}}]}\n" {
		t.Fatalf("process JSON = %q", stdout)
	}
}
