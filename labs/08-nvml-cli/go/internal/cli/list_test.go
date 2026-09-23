package cli

import (
	"context"
	"encoding/json"
	"errors"
	"gpuinfo/internal/gpu"
	"strings"
	"testing"
)

func TestListJSONZeroOneAndPartialMultiple(t *testing.T) {
	cases := []struct {
		name    string
		devices []gpu.DeviceResult
		want    string
		wantErr bool
	}{
		{"zero", []gpu.DeviceResult{}, "[]\n", false},
		{"one", []gpu.DeviceResult{{Device: gpu.Device{Index: 0, Name: "GPU 0"}}}, "[{\"device\":{\"index\":0,\"name\":\"GPU 0\",\"uuid\":\"\",\"pci_bus_id\":\"\"}}]\n", false},
		{"partial multiple", []gpu.DeviceResult{
			{Device: gpu.Device{Index: 0, Name: "GPU 0"}},
			{Device: gpu.Device{Index: 1, Name: "GPU 1"}, Err: errors.New("device 1 UUID unavailable")},
		}, "", true},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			session := &fakeSession{devices: tc.devices}
			stdout, _, err, opens := executeFake(context.Background(), session, "list", "--output", "json")
			if (err != nil) != tc.wantErr || opens != 1 || session.closeCalls != 1 {
				t.Fatalf("execute: err=%v opens=%d closes=%d", err, opens, session.closeCalls)
			}
			if tc.want != "" && stdout != tc.want {
				t.Fatalf("JSON = %q, want %q", stdout, tc.want)
			}
			if tc.wantErr {
				if !strings.Contains(err.Error(), "device 1 UUID unavailable") {
					t.Fatalf("error = %v", err)
				}
				var got []struct {
					Device struct {
						Index int `json:"index"`
					} `json:"device"`
					Error string `json:"error"`
				}
				if decodeErr := json.Unmarshal([]byte(stdout), &got); decodeErr != nil {
					t.Fatal(decodeErr)
				}
				if len(got) != 2 || got[0].Device.Index != 0 || got[1].Device.Index != 1 || got[1].Error != "device 1 UUID unavailable" {
					t.Fatalf("unexpected ordered partial results: %+v", got)
				}
			}
		})
	}
}
