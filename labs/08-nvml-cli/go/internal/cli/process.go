package cli

import (
	"errors"

	"github.com/spf13/cobra"
	"gpuinfo/internal/gpu"
	"gpuinfo/internal/render"
)

func newProcessCommand(open gpu.Opener) *cobra.Command {
	var selectorFlags deviceSelectorFlags

	command := &cobra.Command{
		Use:     "process [index]",
		Aliases: []string{"processes"},
		Short:   "Show active compute processes on one GPU",
		Args:    cobra.MaximumNArgs(1),
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

			processes, err := session.ComputeProcesses(cmd.Context(), selector)
			if err != nil {
				return err
			}
			if jsonOutput(cmd) {
				return render.ProcessesJSON(cmd.OutOrStdout(), processes)
			}
			return render.ProcessTable(cmd.OutOrStdout(), processes)
		},
	}
	selectorFlags.bind(command)
	return command
}
