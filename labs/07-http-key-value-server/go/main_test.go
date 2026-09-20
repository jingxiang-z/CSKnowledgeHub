package main

import (
	"context"
	"encoding/json"
	"io"
	"net"
	"net/http"
	"net/http/httptest"
	"strings"
	"sync"
	"testing"
	"time"
)

func testHandler() http.Handler {
	return newHandler(&Store{data: make(map[string]json.RawMessage)})
}

func request(t *testing.T, client *http.Client, method, url, body string, want int) []byte {
	t.Helper()
	req, err := http.NewRequest(method, url, strings.NewReader(body))
	if err != nil {
		t.Fatal(err)
	}
	resp, err := client.Do(req)
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()
	result, err := io.ReadAll(resp.Body)
	if err != nil {
		t.Fatal(err)
	}
	if resp.StatusCode != want {
		t.Fatalf("%s %s: status %d, want %d; body %s", method, url, resp.StatusCode, want, result)
	}
	return result
}

func TestCRUDAndJSONValues(t *testing.T) {
	server := httptest.NewServer(testHandler())
	defer server.Close()
	client := server.Client()

	request(t, client, http.MethodGet, server.URL+"/health", "", http.StatusOK)
	request(t, client, http.MethodGet, server.URL+"/keys/item", "", http.StatusNotFound)
	for _, value := range []string{"null", "true", "3.5", `"text"`, `[1,2]`, `{"a":1}`} {
		request(t, client, http.MethodPut, server.URL+"/keys/item", `{"value":`+value+`}`, http.StatusOK)
		got := request(t, client, http.MethodGet, server.URL+"/keys/item", "", http.StatusOK)
		var response KVResponse
		if err := json.Unmarshal(got, &response); err != nil {
			t.Fatal(err)
		}
		if response.Key != "item" || string(response.Value) != value {
			t.Fatalf("got %s, want value %s", got, value)
		}
	}
	request(t, client, http.MethodDelete, server.URL+"/keys/item", "", http.StatusNoContent)
	request(t, client, http.MethodGet, server.URL+"/keys/item", "", http.StatusNotFound)
	request(t, client, http.MethodDelete, server.URL+"/keys/item", "", http.StatusNotFound)
}

func TestValidationAndRouting(t *testing.T) {
	server := httptest.NewServer(testHandler())
	defer server.Close()
	client := server.Client()

	for _, key := range []string{"bad.key", "bad%20key", strings.Repeat("a", 129), "%C3%A9"} {
		for _, method := range []string{http.MethodGet, http.MethodPut, http.MethodDelete} {
			request(t, client, method, server.URL+"/keys/"+key, `{"value":1}`, http.StatusBadRequest)
		}
	}
	request(t, client, http.MethodPut, server.URL+"/keys/"+strings.Repeat("a", 128), `{"value":1}`, http.StatusOK)
	for _, body := range []string{"", "{", "{}", `{"value":`, `{"value":1} {}`} {
		request(t, client, http.MethodPut, server.URL+"/keys/item", body, http.StatusBadRequest)
	}
	request(t, client, http.MethodPost, server.URL+"/keys/item", `{"value":1}`, http.StatusMethodNotAllowed)
	request(t, client, http.MethodGet, server.URL+"/missing", "", http.StatusNotFound)
}

func TestConcurrentRequests(t *testing.T) {
	server := httptest.NewServer(testHandler())
	defer server.Close()
	client := server.Client()
	var workers sync.WaitGroup
	for i := 0; i < 24; i++ {
		workers.Add(1)
		go func() {
			defer workers.Done()
			request(t, client, http.MethodPut, server.URL+"/keys/shared", `{"value":1}`, http.StatusOK)
			request(t, client, http.MethodGet, server.URL+"/keys/shared", "", http.StatusOK)
		}()
	}
	workers.Wait()
}

func TestRecovery(t *testing.T) {
	handler := logAndRecover(http.HandlerFunc(func(http.ResponseWriter, *http.Request) {
		panic("broken store")
	}))
	response := httptest.NewRecorder()
	handler.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "/keys/item", nil))
	if response.Code != http.StatusInternalServerError {
		t.Fatalf("status %d, want 500", response.Code)
	}
}

func TestShutdownWaitsForActiveRequest(t *testing.T) {
	entered := make(chan struct{})
	release := make(chan struct{})
	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		close(entered)
		<-release
		w.WriteHeader(http.StatusOK)
	})
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatal(err)
	}
	server := &http.Server{Handler: handler}
	serveDone := make(chan error, 1)
	go func() { serveDone <- server.Serve(listener) }()
	defer server.Close()

	requestDone := make(chan error, 1)
	go func() {
		resp, err := http.Get("http://" + listener.Addr().String())
		if err == nil {
			resp.Body.Close()
			if resp.StatusCode != http.StatusOK {
				err = io.ErrUnexpectedEOF
			}
		}
		requestDone <- err
	}()
	select {
	case <-entered:
	case <-time.After(2 * time.Second):
		t.Fatal("request did not start")
	}
	shutdownDone := make(chan error, 1)
	go func() {
		ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
		defer cancel()
		shutdownDone <- server.Shutdown(ctx)
	}()
	select {
	case err := <-shutdownDone:
		t.Fatalf("shutdown completed before request finished: %v", err)
	case <-time.After(50 * time.Millisecond):
	}
	close(release)
	if err := <-requestDone; err != nil {
		t.Fatal(err)
	}
	if err := <-shutdownDone; err != nil {
		t.Fatal(err)
	}
	if err := <-serveDone; err != http.ErrServerClosed {
		t.Fatalf("serve returned %v", err)
	}
}
