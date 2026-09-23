package cli

import (
	"context"
	"errors"
	"fmt"
	"time"

	"github.com/spf13/cobra"
	"gpuinfo/internal/gpu"
	"gpuinfo/internal/render"
)

func newWatchCommand(open gpu.Opener) *cobra.Command {
	var selectorFlags deviceSelectorFlags
	var interval time.Duration
	var count int

	command := &cobra.Command{
		Use:   "watch [index]",
		Short: "Watch metrics for one GPU",
		Args:  cobra.MaximumNArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			return runWatch(cmd, args, open, &selectorFlags, interval, count, waitInterval)
		},
	}
	selectorFlags.bind(command)
	command.Flags().DurationVar(&interval, "interval", 2*time.Second, "time between completed samples")
	command.Flags().IntVar(&count, "count", 0, "number of samples (omit to watch until interrupted)")
	return command
}

func runWatch(cmd *cobra.Command, args []string, open gpu.Opener, selectorFlags *deviceSelectorFlags, interval time.Duration, count int, wait func(context.Context, time.Duration) error) (err error) {
	selector, err := selectorFlags.resolve(cmd, args)
	if err != nil {
		return err
	}
	if interval <= 0 {
		return fmt.Errorf("--interval must be positive")
	}
	if cmd.Flags().Changed("count") && count <= 0 {
		return fmt.Errorf("--count must be a positive integer")
	}

	if err := cmd.Context().Err(); err != nil {
		return err
	}

	session, err := open()
	if err != nil {
		return err
	}
	defer func() { err = errors.Join(err, session.Close()) }()

	for sample := 1; count == 0 || sample <= count; sample++ {
		if err := cmd.Context().Err(); err != nil {
			return err
		}

		snapshot, err := session.DeviceSnapshot(cmd.Context(), selector)
		if err != nil {
			return fmt.Errorf("watch %s, sample %d: %w", selector, sample, err)
		}
		if err := cmd.Context().Err(); err != nil {
			return err
		}
		if jsonOutput(cmd) {
			if err := render.WatchJSON(cmd.OutOrStdout(), sample, snapshot); err != nil {
				return err
			}
		} else {
			if _, err := fmt.Fprintf(cmd.OutOrStdout(), "SAMPLE %d\n", sample); err != nil {
				return err
			}
			if err := render.SnapshotTable(cmd.OutOrStdout(), snapshot); err != nil {
				return err
			}
		}
		if partialErr := snapshot.Error(); partialErr != nil {
			if _, err := fmt.Fprintf(cmd.ErrOrStderr(), "watch %s, sample %d: %v\n", selector, sample, partialErr); err != nil {
				return err
			}
		}
		if count > 0 && sample == count {
			return nil
		}
		if !jsonOutput(cmd) {
			if _, err := fmt.Fprintln(cmd.OutOrStdout()); err != nil {
				return err
			}
		}

		if err := wait(cmd.Context(), interval); err != nil {
			return err
		}
	}
	return nil
}

func waitInterval(ctx context.Context, interval time.Duration) error {
	timer := time.NewTimer(interval)
	defer timer.Stop()
	select {
	case <-ctx.Done():
		return ctx.Err()
	case <-timer.C:
		return nil
	}
}
