package main

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"gpuinfo/internal/cli"
	"gpuinfo/internal/nvml"
)

func main() {
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()
	if err := cli.NewRootCommand(nvml.Open).ExecuteContext(ctx); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
