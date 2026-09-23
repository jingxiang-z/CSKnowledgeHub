package cli

import (
	"context"
	"errors"
	"gpuinfo/internal/gpu"
	"strings"
	"testing"
)

func TestSystemErrorsAndCloseErrorPropagate(t *testing.T) {
	queryErr := errors.New("driver query failed")
	closeErr := errors.New("shutdown failed")
	session := &fakeSession{
		info:    gpu.SystemInfo{DriverVersion: "", CUDADriverVersion: 12040, NVMLVersion: "12", DeviceCount: 1},
		infoErr: queryErr, closeErr: closeErr,
	}
	stdout, _, err, opens := executeFake(context.Background(), session, "system", "--output", "json")
	if !errors.Is(err, queryErr) || !errors.Is(err, closeErr) || opens != 1 || session.closeCalls != 1 {
		t.Fatalf("execute: err=%v opens=%d closes=%d", err, opens, session.closeCalls)
	}
	if !strings.Contains(stdout, `"cuda_driver_version":"12.4"`) || !strings.Contains(stdout, `"error":"driver query failed"`) {
		t.Fatalf("partial system JSON = %q", stdout)
	}
}
