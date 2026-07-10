"""
Tests for option_pricing._core.binomial_model
"""
import pytest

from option_pricing._core.binomial_model import binomial_price, american_price
from option_pricing._core.black_scholes import calculate_price


# --- Correctness ---

def test_binomial_converges_to_black_scholes():
    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
    bs_call, bs_put = calculate_price(S, K, T, r, sigma)
    bin_call, bin_put = binomial_price(S, K, T, r, sigma, N=1000)
    assert bin_call == pytest.approx(bs_call, abs=0.05)
    assert bin_put == pytest.approx(bs_put, abs=0.05)


def test_american_put_gte_european_put():
    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
    _, euro_put = binomial_price(S, K, T, r, sigma, N=500)
    _, amer_put = american_price(S, K, T, r, sigma, N=500)
    assert amer_put >= euro_put - 1e-6


def test_american_call_approx_european_call_no_dividends():
    # No dividends -> American call should never be worth exercising early
    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
    euro_call, _ = binomial_price(S, K, T, r, sigma, N=500)
    amer_call, _ = american_price(S, K, T, r, sigma, N=500)
    assert amer_call == pytest.approx(euro_call, abs=0.05)


# --- Edge cases ---

def test_N_equals_one_does_not_crash():
    call, put = binomial_price(S0=100, K=100, T=1, r=0.05, sigma=0.2, N=1)
    assert call >= 0
    assert put >= 0


@pytest.mark.parametrize("N", [0, -1])
def test_N_less_than_one_raises(N):
    with pytest.raises(ValueError):
        binomial_price(S0=100, K=100, T=1, r=0.05, sigma=0.2, N=N)


def test_sigma_zero_does_not_crash_binomial():
    # This used to divide by zero (u == d == 1); should now return
    # discounted forward-intrinsic value instead.
    call, put = binomial_price(S0=100, K=100, T=1, r=0.05, sigma=0, N=50)
    forward = 100 * (2.718281828 ** 0.05)
    assert call == pytest.approx(max(forward - 100, 0) * (2.718281828 ** -0.05), rel=1e-3)


def test_american_sigma_zero_optimal_stopping():
    # American put with deterministic path should pick best exercise time,
    # not just terminal payoff.
    call, put = american_price(S0=90, K=100, T=1, r=0.05, sigma=0, N=50)
    assert put >= 10.0 - 1e-6  # deep ITM put, intrinsic value at t=0 is 10


def test_T_zero_binomial_returns_intrinsic():
    call, put = binomial_price(S0=110, K=100, T=0, r=0.05, sigma=0.2, N=50)
    assert call == pytest.approx(10.0)
    assert put == pytest.approx(0.0)


@pytest.mark.parametrize("bad_S0", [0, -100])
def test_negative_S0_raises(bad_S0):
    with pytest.raises(ValueError):
        binomial_price(S0=bad_S0, K=100, T=1, r=0.05, sigma=0.2, N=50)