package gpu

import "context"

type Provider interface {
	SystemInfo(context.Context) (SystemInfo, error)
	ListDevices(context.Context) ([]DeviceResult, error)
	DeviceSnapshot(context.Context, DeviceSelector) (DeviceSnapshot, error)
	ComputeProcesses(context.Context, DeviceSelector) (ProcessList, error)
}

// Session is a provider whose native resources must be closed after a command.
type Session interface {
	Provider
	Close() error
}

type Opener func() (Session, error)
