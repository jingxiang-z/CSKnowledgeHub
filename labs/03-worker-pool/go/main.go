package main

import (
	"context"
	"errors"
	"fmt"
	"sync"
)

type Job func(ctx context.Context) (any, error)

type Result struct {
	Value     any
	Err       error
	Cancelled bool
}

type WorkerPool struct {
	MaxWorkers int
	QueueSize  int
	Results    []Result
	tasks      chan Job
	wg         sync.WaitGroup
	mu         sync.Mutex
	closed     bool
	ctx        context.Context
	cancel     context.CancelFunc
}

func NewWorkerPool(maxWorkers, queueSize int) (*WorkerPool, error) {
	if maxWorkers <= 0 {
		return nil, fmt.Errorf("maxWorkers must be positive")
	}
	if queueSize < 0 {
		return nil, fmt.Errorf("queueSize must be non-negative")
	}
	ctx, cancel := context.WithCancel(context.Background())
	pool := &WorkerPool{
		MaxWorkers: maxWorkers,
		QueueSize:  queueSize,
		tasks:      make(chan Job, queueSize),
		Results:    make([]Result, 0, queueSize),
		ctx:        ctx,
		cancel:     cancel,
	}
	for i := 0; i < pool.MaxWorkers; i++ {
		pool.wg.Add(1)
		go func() {
			defer pool.wg.Done()
			for task := range pool.tasks {
				var result Result
				if err := pool.ctx.Err(); err != nil {
					result = Result{Err: err, Cancelled: true}
				} else {
					value, err := task(pool.ctx)
					result = Result{Value: value, Err: err, Cancelled: errors.Is(err, context.Canceled)}
				}
				pool.mu.Lock()
				pool.Results = append(pool.Results, result)
				pool.mu.Unlock()
			}
		}()
	}
	return pool, nil
}

func (pool *WorkerPool) Submit(task Job) error {
	pool.mu.Lock()
	defer pool.mu.Unlock()
	if pool.closed {
		return fmt.Errorf("worker pool is closed")
	}
	select {
	case pool.tasks <- task:
	default:
		return fmt.Errorf("task queue is full")
	}
	return nil
}

func (pool *WorkerPool) Cancel() {
	pool.cancel()
	pool.Close()
}

func (pool *WorkerPool) Close() {
	pool.mu.Lock()
	if !pool.closed {
		pool.closed = true
		close(pool.tasks)
	}
	pool.mu.Unlock()
	pool.wg.Wait()
	pool.cancel()
}
