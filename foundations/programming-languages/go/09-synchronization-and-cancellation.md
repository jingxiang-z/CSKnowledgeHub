# 09 Synchronization and Cancellation

Shared mutable state needs synchronization. Background work also needs a stopping condition and a way for callers to wait for its completion.

## Protect Shared State and Join Work

```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	var mu sync.Mutex
	var wg sync.WaitGroup
	total := 0
	for _, pages := range []int{120, 240, 310} {
		wg.Add(1)
		go func(count int) {
			defer wg.Done()
			mu.Lock()
			total += count
			mu.Unlock()
		}(pages)
	}
	wg.Wait()
	fmt.Println("Total pages:", total)
}
```

Call `Add` before launching the work; `Done` records completion and `Wait` blocks until all registered work finishes. The mutex protects concurrent updates. A wait group alone does not prevent races between workers. Do not copy a mutex or wait group after first use.

## Cancel Work Cooperatively

This separate program lets a caller stop a producer and wait for it to exit:

```go
package main

import (
	"context"
	"fmt"
)

func produce(ctx context.Context, out chan<- int, done chan<- struct{}) {
	defer close(done)
	defer close(out)
	for n := 1; ; n++ {
		select {
		case <-ctx.Done():
			return
		case out <- n:
		}
	}
}

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	values := make(chan int)
	done := make(chan struct{})
	go produce(ctx, values, done)
	fmt.Println(<-values)
	cancel()
	<-done
}
```

Cancellation signals intent; it does not forcibly stop a goroutine. The producer observes `ctx.Done()` even if nobody receives another value. The separate `done` signal lets the caller wait for cleanup. Call cancellation functions to release associated resources; `WithTimeout` and `WithDeadline` also support bounded work.

Pass a context explicitly, conventionally as the first parameter. `time.Sleep` is not a completion signal. Choose a mutex for shared state or a channel for communication based on the data flow, and test exercised concurrent paths with the race detector.

[Next: Tests and Tooling](10-tests-and-tooling.md)

## References

- [Tour: sync.Mutex](https://go.dev/tour/concurrency/9)
- [Standard library: sync](https://pkg.go.dev/sync)
- [Standard library: context](https://pkg.go.dev/context)
- [Go memory model](https://go.dev/ref/mem)
