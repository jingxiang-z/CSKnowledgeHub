package cli

import (
	"errors"

	"github.com/spf13/cobra"
	"gpuinfo/internal/gpu"
	"gpuinfo/internal/render"
)

func newSystemCommand(open gpu.Opener) *cobra.Command {
	return &cobra.Command{
		Use:   "system",
		Short: "Show NVIDIA system information",
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

			info, queryErr := session.SystemInfo(cmd.Context())
			var renderErr error
			if jsonOutput(cmd) {
				renderErr = render.SystemJSON(cmd.OutOrStdout(), info, queryErr)
			} else {
				renderErr = render.SystemTable(cmd.OutOrStdout(), info)
			}
			return errors.Join(queryErr, renderErr)
		},
	}
}
