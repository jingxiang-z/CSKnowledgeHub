package main

import (
	"context"
	"encoding/json"
	"errors"
	"io"
	"log"
	"net/http"
	"os/signal"
	"sync"
	"syscall"
	"time"
)

type Store struct {
	mu   sync.RWMutex
	data map[string]json.RawMessage
}

type PutRequest struct {
	Value json.RawMessage `json:"value"`
}

type KVResponse struct {
	Key   string          `json:"key"`
	Value json.RawMessage `json:"value"`
}

type statusWriter struct {
	http.ResponseWriter
	status int
}

func (w *statusWriter) WriteHeader(status int) {
	if w.status != 0 {
		return
	}
	w.status = status
	w.ResponseWriter.WriteHeader(status)
}

func (w *statusWriter) Write(body []byte) (int, error) {
	if w.status == 0 {
		w.WriteHeader(http.StatusOK)
	}
	return w.ResponseWriter.Write(body)
}

func logAndRecover(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		writer := &statusWriter{ResponseWriter: w}
		defer func() {
			if recovered := recover(); recovered != nil {
				log.Printf("unexpected error during %s %s: %v", r.Method, r.URL.Path, recovered)
				if writer.status == 0 {
					http.Error(writer, "Internal server error", http.StatusInternalServerError)
				}
			}
			log.Printf("%s %s %d", r.Method, r.URL.Path, writer.status)
		}()
		next.ServeHTTP(writer, r)
	})
}

func validKey(key string) bool {
	if len(key) == 0 || len(key) > 128 {
		return false
	}
	for i := 0; i < len(key); i++ {
		c := key[i]
		if !((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') ||
			(c >= '0' && c <= '9') || c == '_' || c == '-') {
			return false
		}
	}
	return true
}

func writeJSON(w http.ResponseWriter, status int, data any) {
	body, err := json.Marshal(data)
	if err != nil {
		log.Printf("encode response: %v", err)
		http.Error(w, "Internal server error", http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_, _ = w.Write(append(body, '\n'))
}

func newHandler(store *Store) http.Handler {
	mux := http.NewServeMux()

	mux.HandleFunc("GET /health", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
	})

	mux.HandleFunc("GET /keys/{key}", func(w http.ResponseWriter, r *http.Request) {
		key := r.PathValue("key")
		if !validKey(key) {
			http.Error(w, "Invalid key", http.StatusBadRequest)
			return
		}

		store.mu.RLock()
		value, exists := store.data[key]
		store.mu.RUnlock()
		if !exists {
			http.Error(w, "Key not found", http.StatusNotFound)
			return
		}
		writeJSON(w, http.StatusOK, KVResponse{Key: key, Value: value})
	})

	mux.HandleFunc("PUT /keys/{key}", func(w http.ResponseWriter, r *http.Request) {
		key := r.PathValue("key")
		if !validKey(key) {
			http.Error(w, "Invalid key", http.StatusBadRequest)
			return
		}

		var req PutRequest
		decoder := json.NewDecoder(r.Body)
		if err := decoder.Decode(&req); err != nil {
			http.Error(w, "Invalid request body: "+err.Error(), http.StatusBadRequest)
			return
		}
		if len(req.Value) == 0 {
			http.Error(w, "Missing value", http.StatusBadRequest)
			return
		}
		var extra any
		if err := decoder.Decode(&extra); err != io.EOF {
			http.Error(w, "Request body must contain one JSON object", http.StatusBadRequest)
			return
		}

		store.mu.Lock()
		store.data[key] = req.Value
		store.mu.Unlock()
		writeJSON(w, http.StatusOK, KVResponse{Key: key, Value: req.Value})
	})

	mux.HandleFunc("DELETE /keys/{key}", func(w http.ResponseWriter, r *http.Request) {
		key := r.PathValue("key")
		if !validKey(key) {
			http.Error(w, "Invalid key", http.StatusBadRequest)
			return
		}

		store.mu.Lock()
		_, exists := store.data[key]
		if exists {
			delete(store.data, key)
		}
		store.mu.Unlock()
		if !exists {
			http.Error(w, "Key not found", http.StatusNotFound)
			return
		}
		w.WriteHeader(http.StatusNoContent)
	})

	return logAndRecover(mux)
}

func main() {
	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer stop()

	server := &http.Server{
		Addr:    ":8080",
		Handler: newHandler(&Store{data: make(map[string]json.RawMessage)}),
	}
	go func() {
		if err := server.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
			log.Fatalf("serve: %v", err)
		}
	}()
	<-ctx.Done()

	shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := server.Shutdown(shutdownCtx); err != nil {
		log.Printf("shutdown: %v", err)
	}
}
