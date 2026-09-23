package nvml

import (
	"context"
	"errors"
	"testing"
)

func TestCanceledContextStopsListDevicesBeforeNVMLCalls(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	session := &Session{}
	if _, err := session.ListDevices(ctx); !errors.Is(err, context.Canceled) {
		t.Fatalf("ListDevices error = %v", err)
	}
}
