package main

import (
	"context"
	"errors"
	"sync"
)

// runPipeline sends numItems from each producer to the consumer workers.
// Context cancellation stops remaining work; consumer callbacks must not fail.
func runPipeline(ctx context.Context, numProducers, numConsumers, bufferSize, numItems int, consume func(int)) error {
	if ctx == nil {
		return errors.New("context must not be nil")
	}
	if numProducers <= 0 || numConsumers <= 0 || bufferSize <= 0 || numItems < 0 {
		return errors.New("producer count, consumer count, and buffer size must be positive; item count must be non-negative")
	}
	if consume == nil {
		return errors.New("consumer function must not be nil")
	}

	jobs := make(chan int, bufferSize)
	var producers, consumers sync.WaitGroup

	for range numProducers {
		producers.Add(1)
		go func() {
			defer producers.Done()
			for j := range numItems {
				select {
				case <-ctx.Done():
					return
				case jobs <- j:
				}
			}
		}()
	}

	for range numConsumers {
		consumers.Add(1)
		go func() {
			defer consumers.Done()
			for {
				select {
				case <-ctx.Done():
					return
				case job, ok := <-jobs:
					if !ok {
						return
					}
					consume(job)
				}
			}
		}()
	}

	producers.Wait()
	close(jobs)
	consumers.Wait()

	return ctx.Err()
}
