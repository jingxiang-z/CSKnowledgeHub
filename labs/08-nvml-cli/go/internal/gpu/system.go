package gpu

type SystemInfo struct {
	DriverVersion     string
	CUDADriverVersion int
	NVMLVersion       string
	DeviceCount       int
}
