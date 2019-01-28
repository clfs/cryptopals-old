package main

import "testing"

type Mt19937 struct {
	index int
	state [624]uint32
}

func newMt19937(seed uint32) *Mt19937 {
	m := &Mt19937{index: 624}
	for i := range m.state {
		if i == 0 {
			m.state[0] = seed
		} else {
			m.state[i] = 1812433253*(m.state[i-1]^m.state[i-1]>>30) + uint32(i)
		}
	}
	return m
}

func (m *Mt19937) rand() uint32 {
	if m.index >= 624 {
		m.twist()
	}
	y := m.state[m.index]
	y ^= y >> 11
	y ^= y << 7 & 0x9d2c5680
	y ^= y << 15 & 0xefc60000
	y ^= y >> 18
	m.index++
	return y
}

func (m *Mt19937) twist() {
	for i := range m.state {
		y := (m.state[i] & 0x80000000) + (m.state[(i+1)%624] & 0x7fffffff)
		m.state[i] = m.state[(i+397)%624] ^ y>>1
		if y%2 == 1 {
			m.state[i] ^= 0x9908b0df
		}
	}
	m.index = 0
}

func TestChallenge21(t *testing.T) {
	// Some seed/number pairs I found on Google.
	tables := []struct {
		s uint32
		n uint32
	}{
		{0, 2357136044},
		{1, 1791095845},
		{10, 3312796937},
		{5489, 3499211612},
	}
	for _, table := range tables {
		m := newMt19937(table.s)
		if res := m.rand(); res != table.n {
			t.Fatalf("expected %d, got %d", table.n, res)
		}
	}
}
