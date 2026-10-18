# 08 Goroutines and Channels

A goroutine is a concurrently executing function started with `go`. Channels let goroutines exchange typed values and coordinate progress; starting a goroutine alone does not wait for it to finish.

## Produce and Consume Values

```go
package main

import "fmt"

func pageCounts(out chan<- int) {
	defer close(out)
	for _, pages := range []int{120, 240, 310} {
		out <- pages
	}
}

func main() {
	counts := make(chan int)
	go pageCounts(counts)

	total := 0
	for pages := range counts {
		total += pages
	}
	fmt.Println("Total pages:", total)
}
```

An unbuffered send waits for a matching receiver, and a receive waits for a sender. `chan<- int` restricts the producer to sending; `<-chan int` restricts a consumer to receiving. Direction restrictions help document responsibilities.

The producer closes the channel after its last send. Ranging over the channel receives until it is closed and drained. Here this gives `main` a completion condition; `main` returning would otherwise end the program even if other goroutines were still running.

## Closing and Buffering

`make(chan int, capacity)` creates a buffered channel. Sends block when its buffer is full; receives block when it is empty and still open. Buffering changes when operations block, but does not guarantee that an incorrectly coordinated program will finish.

Only close a channel when no further sends can occur, typically from the sending side. Sending to a closed channel or closing it twice panics. A receive written as `value, ok := <-channel` reports `ok == false` once the channel is closed and drained. Closing is useful as a signal; channels do not need closing solely for garbage collection.

## Select and Blocking

`select` waits for a ready send or receive case; if several are ready, it chooses one pseudo-randomly. A `default` makes the operation nonblocking and can cause a busy loop when used carelessly. Sending or receiving on a nil channel blocks indefinitely; in a `select`, that case is disabled.

Concurrency does not guarantee parallel execution. Use channels for communication and coordination, and give every goroutine a clear path to completion. Chapter 9 adds cancellation when a consumer may stop early.

[Next: Synchronization and Cancellation](09-synchronization-and-cancellation.md)

## References

- [Tour: Goroutines](https://go.dev/tour/concurrency/1)
- [Tour: Channels](https://go.dev/tour/concurrency/2)
- [Tour: Select](https://go.dev/tour/concurrency/5)
