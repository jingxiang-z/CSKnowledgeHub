package cli

import (
	"errors"

	"github.com/spf13/cobra"
	"gpuinfo/internal/gpu"
	"gpuinfo/internal/render"
)

func newListCommand(open gpu.Opener) *cobra.Command {
	return &cobra.Command{
		Use:   "list",
		Short: "List detected GPUs",
		Args:  cobra.NoArgs,
		RunE: func(cmd *cobra.Command, _ []string) (err error) {
			if err := cmd.Context().Err(); err != nil {
				return err
			}

			session, err := open()
			if err != nil {
				return err
			}
			defer func() { err = errors.Join(err, session.Close()) }()

			results, listErr := session.ListDevices(cmd.Context())
			err = listErr
			if results != nil {
				if jsonOutput(cmd) {
					err = errors.Join(err, render.DevicesJSON(cmd.OutOrStdout(), results))
				} else {
					err = errors.Join(err, render.DeviceTable(cmd.OutOrStdout(), results))
				}
			}
			for _, result := range results {
				err = errors.Join(err, result.Err)
			}
			return err
		},
	}
}
