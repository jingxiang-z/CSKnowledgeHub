package nvml

import (
	"context"
	"errors"
	"testing"
)

func TestCanceledContextStopsSystemInfoBeforeNVMLCalls(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	session := &Session{}
	if _, err := session.SystemInfo(ctx); !errors.Is(err, context.Canceled) {
		t.Fatalf("SystemInfo error = %v", err)
	}
}
