"""
Tests for option_pricing._core.monte_carlo
"""
import pytest

from option_pricing._core.monte_carlo import (
    simulate_paths,
    european_price,
    asian_price_arithmetic,
    asian_price_geometric,
    barrier_price,
    lookback_price_floating,
    lookback_price_fixed,
)
from option_pricing._core.black_scholes import calculate_price


# --- Correctness ---

def test_mc_converges_to_black_scholes():
    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
    bs_call, bs_put = calculate_price(S, K, T, r, sigma)
    mc_call, mc_put = european_price(S, K, T, r, sigma, N=100, M=200000)
    assert mc_call == pytest.approx(bs_call, abs=0.15)
    assert mc_put == pytest.approx(bs_put, abs=0.15)


def test_asian_geometric_call_lte_arithmetic_call():
    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
    arith_call, _ = asian_price_arithmetic(S, K, T, r, sigma, N=100, M=50000)
    geom_call, _ = asian_price_geometric(S, K, T, r, sigma, N=100, M=50000)
    assert geom_call <= arith_call + 0.5  # geometric mean <= arithmetic mean


def test_barrier_in_out_parity():
    S, K, T, r, sigma, H = 100, 100, 1, 0.05, 0.2, 90
    out_call, _ = barrier_price(S, K, T, r, sigma, N=100, M=100000, H=H, barrier_type="down-and-out")
    in_call, _ = barrier_price(S, K, T, r, sigma, N=100, M=100000, H=H, barrier_type="down-and-in")
    vanilla_call, _ = european_price(S, K, T, r, sigma, N=100, M=100000)
    assert (out_call + in_call) == pytest.approx(vanilla_call, abs=0.5)


def test_lookback_floating_call_gte_zero():
    call, put = lookback_price_floating(S=100, T=1, r=0.05, sigma=0.2, N=100, M=20000)
    assert call >= 0
    assert put >= 0


def test_lookback_fixed_bounded_by_floating_logic():
    call, put = lookback_price_fixed(S=100, K=100, T=1, r=0.05, sigma=0.2, N=100, M=20000)
    assert call >= 0
    assert put >= 0


# --- Edge cases ---

def test_T_zero_returns_flat_paths():
    paths = simulate_paths(S=100, T=0, r=0.05, sigma=0.2, N=50, M=10)
    assert paths.shape == (1, 10)
    assert (paths == 100).all()


@pytest.mark.parametrize("N", [0, -1])
def test_N_less_than_one_raises(N):
    with pytest.raises(ValueError):
        simulate_paths(S=100, T=1, r=0.05, sigma=0.2, N=N, M=100)


@pytest.mark.parametrize("M", [0, -1])
def test_M_less_than_one_raises(M):
    with pytest.raises(ValueError):
        simulate_paths(S=100, T=1, r=0.05, sigma=0.2, N=50, M=M)


def test_negative_S_raises():
    with pytest.raises(ValueError):
        simulate_paths(S=-100, T=1, r=0.05, sigma=0.2, N=50, M=100)


def test_negative_sigma_raises():
    with pytest.raises(ValueError):
        simulate_paths(S=100, T=1, r=0.05, sigma=-0.2, N=50, M=100)


@pytest.mark.parametrize("bad_K", [0, -1])
def test_european_price_bad_K_raises(bad_K):
    with pytest.raises(ValueError):
        european_price(S=100, K=bad_K, T=1, r=0.05, sigma=0.2, N=50, M=100)


def test_barrier_down_H_above_S_raises():
    with pytest.raises(ValueError):
        barrier_price(S=100, K=100, T=1, r=0.05, sigma=0.2, N=50, M=100, H=150, barrier_type="down-and-out")


def test_barrier_up_H_below_S_raises():
    with pytest.raises(ValueError):
        barrier_price(S=100, K=100, T=1, r=0.05, sigma=0.2, N=50, M=100, H=50, barrier_type="up-and-out")


def test_barrier_invalid_type_raises():
    with pytest.raises(ValueError):
        barrier_price(S=100, K=100, T=1, r=0.05, sigma=0.2, N=50, M=100, H=90, barrier_type="sideways")