package cli

import (
	"errors"

	"github.com/spf13/cobra"
	"gpuinfo/internal/gpu"
	"gpuinfo/internal/render"
)

func newShowCommand(open gpu.Opener) *cobra.Command {
	var selectorFlags deviceSelectorFlags

	command := &cobra.Command{
		Use:   "show [index]",
		Short: "Show information and metrics for one GPU",
		Args:  cobra.MaximumNArgs(1),
		RunE: func(cmd *cobra.Command, args []string) (err error) {
			selector, err := selectorFlags.resolve(cmd, args)
			if err != nil {
				return err
			}

			if err := cmd.Context().Err(); err != nil {
				return err
			}

			session, err := open()
			if err != nil {
				return err
			}
			defer func() { err = errors.Join(err, session.Close()) }()

			snapshot, err := session.DeviceSnapshot(cmd.Context(), selector)
			if err != nil {
				return err
			}
			var renderErr error
			if jsonOutput(cmd) {
				renderErr = render.SnapshotJSON(cmd.OutOrStdout(), snapshot)
			} else {
				renderErr = render.SnapshotTable(cmd.OutOrStdout(), snapshot)
			}
			return errors.Join(renderErr, snapshot.Error())
		},
	}
	selectorFlags.bind(command)
	return command
}
