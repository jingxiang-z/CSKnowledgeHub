package gpu

type Device struct {
	Index    int
	Name     string
	UUID     string
	PciBusID string
}

// DeviceResult keeps available fields alongside errors from this device.
type DeviceResult struct {
	Device Device
	Err    error
}
