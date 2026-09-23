package cli

import (
	"context"
	"gpuinfo/internal/gpu"
	"testing"
)

func TestShowSelectors(t *testing.T) {
	cases := []struct {
		name string
		args []string
		want gpu.DeviceSelector
	}{
		{"index", []string{"show", "0"}, gpu.IndexSelector(0)},
		{"UUID", []string{"show", "--uuid", "GPU-0"}, gpu.UUIDSelector("GPU-0")},
		{"PCI bus ID", []string{"show", "--pci-bus-id", "0000:01:00.0"}, gpu.PCIBusIDSelector("0000:01:00.0")},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			var got gpu.DeviceSelector
			session := &fakeSession{snapshot: func(_ context.Context, selector gpu.DeviceSelector) (gpu.DeviceSnapshot, error) {
				got = selector
				return availableSnapshot(), nil
			}}
			_, _, err, opens := executeFake(context.Background(), session, tc.args...)
			if err != nil || opens != 1 || session.closeCalls != 1 {
				t.Fatalf("execute: err=%v opens=%d closes=%d", err, opens, session.closeCalls)
			}
			if got != tc.want {
				t.Fatalf("selector = %+v, want %+v", got, tc.want)
			}
		})
	}
}

func TestInvalidSelectorArgumentsFailBeforeOpeningSession(t *testing.T) {
	assertInvalidArgumentsFailBeforeOpeningSession(t, [][]string{
		{"show"},
		{"show", "-1"},
		{"show", "0", "--uuid", "GPU-0"},
		{"show", "--uuid", "GPU-0", "--pci-bus-id", "0000:01:00.0"},
	})
}
