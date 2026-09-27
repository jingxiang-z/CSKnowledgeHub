"""Argument parsing and synchronous command orchestration."""

import argparse
import math
import signal
import sys
import time
from collections.abc import Callable, Sequence
from contextlib import AbstractContextManager, redirect_stderr, redirect_stdout
from typing import TextIO

from . import render
from .errors import GPUError, combine
from .gpu import DeviceSelector, Provider, SelectorKind
from .nvml import open_session

Opener = Callable[[], AbstractContextManager[Provider]]


def positive_seconds(value: str) -> float:
    try:
        seconds = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "interval must be a number of seconds"
        ) from error
    if not math.isfinite(seconds) or seconds <= 0:
        raise argparse.ArgumentTypeError("interval must be positive and finite")
    return seconds


def positive_count(value: str) -> int:
    try:
        count = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("count must be a positive integer") from error
    if count <= 0:
        raise argparse.ArgumentTypeError("count must be a positive integer")
    return count


def build_parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="gpuinfo", description="Inspect NVIDIA GPUs")
    root.add_argument("--output", choices=("table", "json"), default="table")
    commands = root.add_subparsers(dest="command", required=True)
    for name, help_text in (
        ("system", "Show system and driver information"),
        ("list", "List detected GPUs"),
        ("show", "Show one GPU's metrics"),
        ("process", "Show active compute processes"),
        ("watch", "Watch metrics for one GPU"),
    ):
        command = commands.add_parser(
            name, help=help_text, aliases=["processes"] if name == "process" else []
        )
        command.add_argument(
            "--output", choices=("table", "json"), default=argparse.SUPPRESS
        )
        if name in ("show", "process", "watch"):
            command.add_argument(
                "index", nargs="?", help="nonnegative NVML device index"
            )
            command.add_argument("--uuid", help="select a GPU by UUID")
            command.add_argument("--pci-bus-id", help="select a GPU by PCI bus ID")
        if name == "watch":
            command.add_argument(
                "--interval",
                type=positive_seconds,
                default=2.0,
                help="seconds between completed samples (default: 2)",
            )
            command.add_argument(
                "--count",
                type=positive_count,
                help="number of samples; omit to watch until interrupted",
            )
    return root


def resolve_selector(args: argparse.Namespace) -> DeviceSelector:
    if (
        sum(value is not None for value in (args.index, args.uuid, args.pci_bus_id))
        != 1
    ):
        raise GPUError(
            "provide exactly one device selector: index, --uuid, or --pci-bus-id"
        )
    if args.index is not None:
        try:
            index = int(args.index)
        except ValueError as error:
            raise GPUError(
                f"invalid GPU index {args.index!r}: must be a nonnegative integer"
            ) from error
        if index < 0:
            raise GPUError("GPU index must be nonnegative")
        return DeviceSelector(SelectorKind.INDEX, index)
    if args.uuid is not None:
        if not args.uuid:
            raise GPUError("--uuid cannot be empty")
        return DeviceSelector(SelectorKind.UUID, args.uuid)
    if not args.pci_bus_id:
        raise GPUError("--pci-bus-id cannot be empty")
    return DeviceSelector(SelectorKind.PCI_BUS_ID, args.pci_bus_id)


def run_watch(
    args: argparse.Namespace,
    provider: Provider,
    selector: DeviceSelector,
    stdout: TextIO,
    stderr: TextIO,
    sleep: Callable[[float], None],
) -> None:
    sample = 0
    while args.count is None or sample < args.count:
        snapshot = provider.device_snapshot(selector)
        sample += 1
        if args.output == "json":
            render.write_json(stdout, {"sample": sample, "snapshot": snapshot})
        else:
            stdout.write(f"SAMPLE {sample}\n")
            render.snapshot_table(stdout, snapshot)
        if error := snapshot.error():
            stderr.write(
                f"watch {selector.kind.value} {selector.value}, sample {sample}: {error}\n"
            )
        if sample == args.count:
            return
        if args.output == "table":
            stdout.write("\n")
        sleep(args.interval)


def execute(
    args: argparse.Namespace,
    provider: Provider,
    selector: DeviceSelector | None,
    stdout: TextIO,
    stderr: TextIO,
    sleep: Callable[[float], None],
) -> None:
    if args.command == "watch":
        run_watch(args, provider, selector, stdout, stderr, sleep)
        return
    if args.command == "system":
        value = provider.system_info()
        error, table = value.error, render.system_table
    elif args.command == "list":
        value = provider.list_devices()
        error, table = combine(*(item.error for item in value)), render.devices_table
    elif args.command == "show":
        value = provider.device_snapshot(selector)
        error, table = value.error(), render.snapshot_table
    else:
        value = provider.compute_processes(selector)
        error, table = None, render.processes_table
    if args.output == "json":
        render.write_json(stdout, value)
    else:
        table(stdout, value)
    if error is not None:
        raise error


def run(
    argv: Sequence[str] | None = None,
    *,
    opener: Opener = open_session,
    sleep: Callable[[float], None] = time.sleep,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    stdout = sys.stdout if stdout is None else stdout
    stderr = sys.stderr if stderr is None else stderr
    try:
        # Let argparse generate its standard help, usage, and validation errors.
        with redirect_stdout(stdout), redirect_stderr(stderr):
            parser = build_parser()
            try:
                args = parser.parse_args(argv)
                try:
                    selector = (
                        resolve_selector(args)
                        if args.command in ("show", "process", "processes", "watch")
                        else None
                    )
                except GPUError as error:
                    parser.error(str(error))
            except SystemExit as error:
                return error.code
        with opener() as provider:
            execute(args, provider, selector, stdout, stderr, sleep)
    except KeyboardInterrupt:
        return 130
    except (GPUError, OSError) as error:
        stderr.write(f"gpuinfo: {error}\n")
        return 1
    return 0


def _terminate(signum, frame):
    raise SystemExit(128 + signum)


def main() -> int:
    previous = signal.signal(signal.SIGTERM, _terminate)
    try:
        return run()
    finally:
        signal.signal(signal.SIGTERM, previous)
