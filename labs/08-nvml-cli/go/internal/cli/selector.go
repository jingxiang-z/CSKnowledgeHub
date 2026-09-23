package cli

import (
	"fmt"
	"strconv"

	"github.com/spf13/cobra"
	"gpuinfo/internal/gpu"
)

type deviceSelectorFlags struct {
	uuid     string
	pciBusID string
}

func (s *deviceSelectorFlags) bind(cmd *cobra.Command) {
	cmd.Flags().StringVar(&s.uuid, "uuid", "", "select a GPU by UUID")
	cmd.Flags().StringVar(&s.pciBusID, "pci-bus-id", "", "select a GPU by PCI bus ID")
}

func (s *deviceSelectorFlags) resolve(cmd *cobra.Command, args []string) (gpu.DeviceSelector, error) {
	selectorCount := len(args)
	if cmd.Flags().Changed("uuid") {
		selectorCount++
	}
	if cmd.Flags().Changed("pci-bus-id") {
		selectorCount++
	}
	if selectorCount != 1 {
		return gpu.DeviceSelector{}, fmt.Errorf("provide exactly one device selector: index, --uuid, or --pci-bus-id")
	}

	if len(args) == 1 {
		index, err := strconv.Atoi(args[0])
		if err != nil || index < 0 {
			return gpu.DeviceSelector{}, fmt.Errorf("invalid GPU index %q: must be a nonnegative integer", args[0])
		}
		return gpu.IndexSelector(index), nil
	}
	if cmd.Flags().Changed("uuid") {
		if s.uuid == "" {
			return gpu.DeviceSelector{}, fmt.Errorf("--uuid cannot be empty")
		}
		return gpu.UUIDSelector(s.uuid), nil
	}
	if s.pciBusID == "" {
		return gpu.DeviceSelector{}, fmt.Errorf("--pci-bus-id cannot be empty")
	}
	return gpu.PCIBusIDSelector(s.pciBusID), nil
}
