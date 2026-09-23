package cli

import (
	"context"
	"encoding/json"
	"errors"
	"gpuinfo/internal/gpu"
	"testing"
)

func TestShowJSONPreservesUnitsAndMetricStates(t *testing.T) {
	snapshot := availableSnapshot()
	snapshot.TemperatureCelsius = gpu.Metric[uint32]{State: gpu.MetricUnsupported, Err: errors.New("temperature unsupported")}
	metricErr := errors.New("utilization query failed")
	snapshot.GPUUtilizationPercent = gpu.Metric[uint32]{State: gpu.MetricFailed, Err: metricErr}
	session := &fakeSession{snapshot: func(context.Context, gpu.DeviceSelector) (gpu.DeviceSnapshot, error) { return snapshot, nil }}
	stdout, _, err, _ := executeFake(context.Background(), session, "show", "0", "--output", "json")
	if !errors.Is(err, metricErr) || session.closeCalls != 1 {
		t.Fatalf("expected failed metric and session cleanup: err=%v closes=%d", err, session.closeCalls)
	}
	var got map[string]any
	if err := json.Unmarshal([]byte(stdout), &got); err != nil {
		t.Fatal(err)
	}
	memory := got["memory"].(map[string]any)["value"].(map[string]any)
	if memory["total_bytes"] != float64(16_000_000_000) || memory["used_bytes"] != float64(4_000_000_000) {
		t.Fatalf("memory raw bytes = %+v", memory)
	}
	unsupported := got["temperature_celsius"].(map[string]any)
	if unsupported["state"] != "unsupported" || unsupported["error"] != "temperature unsupported" || unsupported["value"] != nil {
		t.Fatalf("unsupported metric = %+v", unsupported)
	}
	failed := got["gpu_utilization_percent"].(map[string]any)
	if failed["state"] != "failed" || failed["error"] != metricErr.Error() || failed["value"] != nil {
		t.Fatalf("failed metric = %+v", failed)
	}
	fan := got["fan_speed_percent"].(map[string]any)
	if fan["state"] != "available" || fan["value"] != float64(0) {
		t.Fatalf("available zero metric = %+v", fan)
	}
	if got["power_usage_milliwatts"].(map[string]any)["value"] != float64(125_000) {
		t.Fatalf("power unit changed: %+v", got["power_usage_milliwatts"])
	}
}
