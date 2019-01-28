package main

import (
	"testing"
	"time"
)

func untemper(y uint32) uint32 {
	// The shift-mask-xor operation is cyclic!
	// It "undoes" itself after a certain number of repetitions.
	y ^= y >> 18
	y ^= y << 15 & 0xefc60000
	for i := 0; i < 7; i++ {
		y ^= y << 7 & 0x9d2c5680
	}
	for i := 0; i < 3; i++ {
		y ^= y >> 11
	}
	return y
}

// Assumes the attacker can only call `m.rand()`, and
// can't read `m.state` directly.
func cloneMt19937(m *Mt19937) *Mt19937 {
	clone := newMt19937(0)
	for i := 0; i < 624; i++ {
		clone.state[i] = untemper(m.rand())
	}
	return clone
}

func TestChallenge23(t *testing.T) {
	m := newMt19937(uint32(time.Now().Unix()))
	clone := cloneMt19937(m)
	for i := 0; i < 100; i++ {
		if a, b := clone.rand(), m.rand(); a != b {
			t.Fatalf("expected %d, got %d", b, a)
		}
	}
}
