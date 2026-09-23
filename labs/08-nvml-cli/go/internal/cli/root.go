package cli

import (
	"fmt"

	"github.com/spf13/cobra"
	"gpuinfo/internal/gpu"
)

func NewRootCommand(open gpu.Opener) *cobra.Command {
	root := &cobra.Command{
		Use:           "gpuinfo",
		Short:         "Inspect NVIDIA GPUs",
		SilenceUsage:  true,
		SilenceErrors: true,
		PersistentPreRunE: func(cmd *cobra.Command, _ []string) error {
			output, err := cmd.Flags().GetString("output")
			if err != nil {
				return err
			}
			if output != "table" && output != "json" {
				return fmt.Errorf("invalid --output %q: expected table or json", output)
			}
			return nil
		},
	}
	root.PersistentFlags().String("output", "table", "output format: table or json")
	root.AddCommand(
		newSystemCommand(open),
		newListCommand(open),
		newShowCommand(open),
		newProcessCommand(open),
		newWatchCommand(open),
	)
	return root
}

func jsonOutput(cmd *cobra.Command) bool {
	return cmd.Flag("output").Value.String() == "json"
}
