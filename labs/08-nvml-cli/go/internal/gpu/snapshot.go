package gpu

import (
	"errors"
	"fmt"
)

type SelectorKind uint8

const (
	SelectorByIndex SelectorKind = iota
	SelectorByUUID
	SelectorByPCIBusID
)

type DeviceSelector struct {
	Kind  SelectorKind
	Index int
	Value string
}

func IndexSelector(index int) DeviceSelector {
	return DeviceSelector{Kind: SelectorByIndex, Index: index}
}

func UUIDSelector(uuid string) DeviceSelector {
	return DeviceSelector{Kind: SelectorByUUID, Value: uuid}
}

func PCIBusIDSelector(busID string) DeviceSelector {
	return DeviceSelector{Kind: SelectorByPCIBusID, Value: busID}
}

func (s DeviceSelector) String() string {
	switch s.Kind {
	case SelectorByIndex:
		return fmt.Sprintf("index %d", s.Index)
	case SelectorByUUID:
		return fmt.Sprintf("UUID %q", s.Value)
	case SelectorByPCIBusID:
		return fmt.Sprintf("PCI bus ID %q", s.Value)
	default:
		return "unknown selector"
	}
}

type MetricState string

const (
	MetricAvailable   MetricState = "available"
	MetricUnsupported MetricState = "unsupported"
	MetricFailed      MetricState = "failed"
)

type Metric[T any] struct {
	Value T
	State MetricState
	Err   error
}

type Memory struct {
	TotalBytes uint64
	UsedBytes  uint64
	FreeBytes  uint64
}

type DeviceSnapshot struct {
	Device                   Device
	DeviceErr                error
	TemperatureCelsius       Metric[uint32]
	GPUUtilizationPercent    Metric[uint32]
	MemoryUtilizationPercent Metric[uint32]
	Memory                   Metric[Memory]
	PowerUsageMilliwatts     Metric[uint32]
	PowerLimitMilliwatts     Metric[uint32]
	FanSpeedPercent          Metric[uint32]
}

func (s DeviceSnapshot) Error() error {
	err := s.DeviceErr
	for _, metricErr := range []error{
		failedMetricError(s.TemperatureCelsius),
		failedMetricError(s.GPUUtilizationPercent),
		failedMetricError(s.MemoryUtilizationPercent),
		failedMetricError(s.Memory),
		failedMetricError(s.PowerUsageMilliwatts),
		failedMetricError(s.PowerLimitMilliwatts),
		failedMetricError(s.FanSpeedPercent),
	} {
		err = errors.Join(err, metricErr)
	}
	return err
}

func failedMetricError[T any](metric Metric[T]) error {
	if metric.State == MetricFailed {
		return metric.Err
	}
	return nil
}
