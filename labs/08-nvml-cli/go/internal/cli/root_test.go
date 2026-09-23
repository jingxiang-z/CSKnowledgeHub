package cli

import (
	"bytes"
	"context"
	"errors"
	"gpuinfo/internal/gpu"
	"strings"
	"testing"
	"time"
)

type fakeSession struct {
	info       gpu.SystemInfo
	infoErr    error
	devices    []gpu.DeviceResult
	listErr    error
	snapshot   func(context.Context, gpu.DeviceSelector) (gpu.DeviceSnapshot, error)
	processes  gpu.ProcessList
	processErr error
	closeErr   error
	closeCalls int
}

func (f *fakeSession) SystemInfo(context.Context) (gpu.SystemInfo, error) { return f.info, f.infoErr }
func (f *fakeSession) ListDevices(context.Context) ([]gpu.DeviceResult, error) {
	return f.devices, f.listErr
}
func (f *fakeSession) DeviceSnapshot(ctx context.Context, selector gpu.DeviceSelector) (gpu.DeviceSnapshot, error) {
	return f.snapshot(ctx, selector)
}
func (f *fakeSession) ComputeProcesses(context.Context, gpu.DeviceSelector) (gpu.ProcessList, error) {
	return f.processes, f.processErr
}
func (f *fakeSession) Close() error {
	f.closeCalls++
	return f.closeErr
}

func executeFake(ctx context.Context, session *fakeSession, args ...string) (string, string, error, int) {
	var stdout, stderr bytes.Buffer
	openCalls := 0
	root := NewRootCommand(func() (gpu.Session, error) {
		openCalls++
		return session, nil
	})
	root.SetArgs(args)
	root.SetOut(&stdout)
	root.SetErr(&stderr)
	err := root.ExecuteContext(ctx)
	return stdout.String(), stderr.String(), err, openCalls
}

func availableSnapshot() gpu.DeviceSnapshot {
	return gpu.DeviceSnapshot{
		Device:                   gpu.Device{Index: 0, Name: "Example GPU", UUID: "GPU-0", PciBusID: "0000:01:00.0"},
		TemperatureCelsius:       gpu.Metric[uint32]{Value: 42, State: gpu.MetricAvailable},
		GPUUtilizationPercent:    gpu.Metric[uint32]{Value: 75, State: gpu.MetricAvailable},
		MemoryUtilizationPercent: gpu.Metric[uint32]{Value: 50, State: gpu.MetricAvailable},
		Memory: gpu.Metric[gpu.Memory]{Value: gpu.Memory{
			TotalBytes: 16_000_000_000,
			UsedBytes:  4_000_000_000,
			FreeBytes:  12_000_000_000,
		}, State: gpu.MetricAvailable},
		PowerUsageMilliwatts: gpu.Metric[uint32]{Value: 125_000, State: gpu.MetricAvailable},
		PowerLimitMilliwatts: gpu.Metric[uint32]{Value: 250_000, State: gpu.MetricAvailable},
		FanSpeedPercent:      gpu.Metric[uint32]{Value: 0, State: gpu.MetricAvailable},
	}
}

func assertInvalidArgumentsFailBeforeOpeningSession(t *testing.T, cases [][]string) {
	t.Helper()
	for _, args := range cases {
		t.Run(strings.Join(args, " "), func(t *testing.T) {
			session := &fakeSession{}
			_, _, err, opens := executeFake(context.Background(), session, args...)
			if err == nil || opens != 0 || session.closeCalls != 0 {
				t.Fatalf("expected validation error before open: err=%v opens=%d closes=%d", err, opens, session.closeCalls)
			}
		})
	}
}

func TestInvalidOutputFailsBeforeOpeningSession(t *testing.T) {
	assertInvalidArgumentsFailBeforeOpeningSession(t, [][]string{{"list", "--output", "xml"}})
}

func TestOpenFailureReturnsErrorWithoutJSON(t *testing.T) {
	openErr := errors.New("initialize NVML failed")
	var stdout, stderr bytes.Buffer
	root := NewRootCommand(func() (gpu.Session, error) { return nil, openErr })
	root.SetArgs([]string{"list", "--output", "json"})
	root.SetOut(&stdout)
	root.SetErr(&stderr)
	err := root.ExecuteContext(context.Background())
	if !errors.Is(err, openErr) || stdout.Len() != 0 {
		t.Fatalf("open failure: err=%v stdout=%q", err, stdout.String())
	}
}

func TestExpiredDeadlineStopsCommandsBeforeOpeningSession(t *testing.T) {
	ctx, cancel := context.WithDeadline(context.Background(), time.Now().Add(-time.Second))
	defer cancel()
	for _, args := range [][]string{
		{"system"}, {"list"}, {"show", "0"}, {"process", "0"}, {"watch", "0", "--count", "1"},
	} {
		t.Run(strings.Join(args, " "), func(t *testing.T) {
			session := &fakeSession{}
			stdout, _, err, opens := executeFake(ctx, session, args...)
			if !errors.Is(err, context.DeadlineExceeded) || opens != 0 || session.closeCalls != 0 || stdout != "" {
				t.Fatalf("expired deadline: err=%v opens=%d closes=%d stdout=%q", err, opens, session.closeCalls, stdout)
			}
		})
	}
}
