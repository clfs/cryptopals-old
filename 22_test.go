package main

import (
	"math/rand"
	"testing"
	"time"
)

func getTimeSeedAndOutput() (seed uint32, output uint32) {
	time.Sleep(time.Duration(40+rand.Intn(1000-40)) * time.Millisecond)
	seed = uint32(time.Now().UnixNano() / 1e6)
	output = newMt19937(seed).rand()
	time.Sleep(time.Duration(40+rand.Intn(1000-40)) * time.Millisecond)
	return
}

func recoverTimeSeed(output uint32) (seed uint32) {
	seed = uint32(time.Now().UnixNano() / 1e6)
	for {
		seed--
		if output == newMt19937(seed).rand() {
			return
		}
	}
}

func TestChallenge22(t *testing.T) {
	seed, output := getTimeSeedAndOutput()
	if res := recoverTimeSeed(output); res != seed {
		t.Fatalf("expected %d, got %d", seed, res)
	}
}
