package cli

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"github.com/spf13/cobra"
	"gpuinfo/internal/gpu"
	"strconv"
	"strings"
	"testing"
	"time"
)

func watchCommandForTest(ctx context.Context, output string, count int, stdout, stderr *bytes.Buffer) *cobra.Command {
	cmd := &cobra.Command{}
	cmd.Flags().String("output", output, "")
	cmd.Flags().Int("count", 0, "")
	if count > 0 {
		_ = cmd.Flags().Set("count", strconv.Itoa(count))
	}
	cmd.SetContext(ctx)
	cmd.SetOut(stdout)
	cmd.SetErr(stderr)
	return cmd
}

func TestInvalidWatchArgumentsFailBeforeOpeningSession(t *testing.T) {
	assertInvalidArgumentsFailBeforeOpeningSession(t, [][]string{
		{"watch", "0", "--count", "0"},
		{"watch", "0", "--interval", "0s"},
	})
}

func TestWatchBoundedJSONWithoutSleeping(t *testing.T) {
	var stdout, stderr bytes.Buffer
	cmd := watchCommandForTest(context.Background(), "json", 3, &stdout, &stderr)
	snapshotCalls, waitCalls, openCalls := 0, 0, 0
	metricErr := errors.New("GPU utilization failed")
	session := &fakeSession{snapshot: func(context.Context, gpu.DeviceSelector) (gpu.DeviceSnapshot, error) {
		snapshotCalls++
		snapshot := availableSnapshot()
		if snapshotCalls == 1 {
			snapshot.GPUUtilizationPercent = gpu.Metric[uint32]{State: gpu.MetricFailed, Err: metricErr}
		}
		return snapshot, nil
	}}
	open := func() (gpu.Session, error) { openCalls++; return session, nil }
	wait := func(ctx context.Context, interval time.Duration) error {
		waitCalls++
		if interval != 2*time.Second {
			t.Errorf("interval = %v", interval)
		}
		return ctx.Err()
	}
	err := runWatch(cmd, []string{"0"}, open, &deviceSelectorFlags{}, 2*time.Second, 3, wait)
	if err != nil || snapshotCalls != 3 || waitCalls != 2 || openCalls != 1 || session.closeCalls != 1 {
		t.Fatalf("watch: err=%v samples=%d waits=%d opens=%d closes=%d", err, snapshotCalls, waitCalls, openCalls, session.closeCalls)
	}
	if !strings.Contains(stderr.String(), metricErr.Error()) {
		t.Fatalf("missing partial metric warning: %q", stderr.String())
	}
	lines := strings.Split(strings.TrimSpace(stdout.String()), "\n")
	if len(lines) != 3 {
		t.Fatalf("JSON Lines count = %d, want 3: %q", len(lines), stdout.String())
	}
	for i, line := range lines {
		var got struct {
			Sample int `json:"sample"`
		}
		if err := json.Unmarshal([]byte(line), &got); err != nil || got.Sample != i+1 {
			t.Fatalf("sample %d: decoded=%+v err=%v", i+1, got, err)
		}
	}
}

func TestWatchCancellationClosesSession(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	var stdout, stderr bytes.Buffer
	cmd := watchCommandForTest(ctx, "json", 0, &stdout, &stderr)
	session := &fakeSession{snapshot: func(context.Context, gpu.DeviceSelector) (gpu.DeviceSnapshot, error) {
		return availableSnapshot(), nil
	}}
	waitCalls := 0
	wait := func(ctx context.Context, _ time.Duration) error {
		waitCalls++
		cancel()
		return ctx.Err()
	}
	err := runWatch(cmd, []string{"0"}, func() (gpu.Session, error) { return session, nil }, &deviceSelectorFlags{}, time.Second, 0, wait)
	if !errors.Is(err, context.Canceled) || waitCalls != 1 || session.closeCalls != 1 || len(strings.Split(strings.TrimSpace(stdout.String()), "\n")) != 1 {
		t.Fatalf("cancellation: err=%v waits=%d closes=%d stdout=%q", err, waitCalls, session.closeCalls, stdout.String())
	}
}

func TestWatchLostDeviceStopsAfterCompletedSample(t *testing.T) {
	var stdout, stderr bytes.Buffer
	cmd := watchCommandForTest(context.Background(), "json", 3, &stdout, &stderr)
	lost := errors.New("device lost")
	calls := 0
	session := &fakeSession{snapshot: func(context.Context, gpu.DeviceSelector) (gpu.DeviceSnapshot, error) {
		calls++
		if calls == 2 {
			return gpu.DeviceSnapshot{}, lost
		}
		return availableSnapshot(), nil
	}}
	waits := 0
	err := runWatch(cmd, []string{"0"}, func() (gpu.Session, error) { return session, nil }, &deviceSelectorFlags{}, time.Second, 3, func(context.Context, time.Duration) error { waits++; return nil })
	if !errors.Is(err, lost) || calls != 2 || waits != 1 || session.closeCalls != 1 {
		t.Fatalf("lost device: err=%v samples=%d waits=%d closes=%d", err, calls, waits, session.closeCalls)
	}
	if strings.Count(stdout.String(), "\n") != 1 || !strings.Contains(stdout.String(), `"sample":1`) {
		t.Fatalf("expected only successful sample: %q", stdout.String())
	}
}

func TestWatchCommandOneSampleJSON(t *testing.T) {
	session := &fakeSession{snapshot: func(context.Context, gpu.DeviceSelector) (gpu.DeviceSnapshot, error) {
		return availableSnapshot(), nil
	}}
	stdout, _, err, opens := executeFake(context.Background(), session, "watch", "0", "--count", "1", "--output", "json")
	if err != nil || opens != 1 || session.closeCalls != 1 {
		t.Fatalf("watch: err=%v opens=%d closes=%d", err, opens, session.closeCalls)
	}
	if !strings.HasPrefix(stdout, `{"sample":1,"snapshot":`) || strings.Count(stdout, "\n") != 1 {
		t.Fatalf("watch JSON line = %q", stdout)
	}
}

func TestCancellationDuringWatchQueryClosesSession(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	var stdout, stderr bytes.Buffer
	cmd := watchCommandForTest(ctx, "json", 1, &stdout, &stderr)
	session := &fakeSession{snapshot: func(queryCtx context.Context, _ gpu.DeviceSelector) (gpu.DeviceSnapshot, error) {
		if queryCtx != ctx {
			t.Error("watch did not pass command context to provider")
		}
		cancel()
		return availableSnapshot(), nil
	}}
	err := runWatch(cmd, []string{"0"}, func() (gpu.Session, error) { return session, nil }, &deviceSelectorFlags{}, time.Second, 1, func(context.Context, time.Duration) error {
		t.Fatal("watch waited after cancellation")
		return nil
	})
	if !errors.Is(err, context.Canceled) || session.closeCalls != 1 || stdout.Len() != 0 {
		t.Fatalf("canceled query: err=%v closes=%d stdout=%q", err, session.closeCalls, stdout.String())
	}
}

func TestWatchWaitHonorsExpiredDeadline(t *testing.T) {
	ctx, cancel := context.WithDeadline(context.Background(), time.Now().Add(-time.Second))
	defer cancel()
	if err := waitInterval(ctx, time.Hour); !errors.Is(err, context.DeadlineExceeded) {
		t.Fatalf("wait error = %v, want deadline exceeded", err)
	}
}
