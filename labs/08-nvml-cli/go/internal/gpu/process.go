package gpu

// Process is one active compute process on a GPU.
type Process struct {
	PID                uint32
	UsedGPUMemoryBytes Metric[uint64]
}

type ProcessList struct {
	DeviceIndex int
	Processes   []Process
}
