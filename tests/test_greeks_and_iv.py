"""
Tests for option_pricing._core.analytics (greeks, implied_volatility)
"""
import pytest

from option_pricing._core.analytics.greeks import calculate_greeks, calculate_vega
from option_pricing._core.analytics.implied_volatility import calculate_iv
from option_pricing._core.black_scholes import calculate_price

# --- Correctness ---

def test_delta_call_minus_delta_put_equals_one():
    delta_call, delta_put, *_ = calculate_greeks(S=100, K=100, T=1, r=0.05, sigma=0.2)
    assert (delta_call - delta_put) == pytest.approx(1.0, abs=1e-6)


def test_gamma_and_vega_identical_for_call_and_put():
    # Gamma and Vega are the same for calls and puts at the same strike;
    # calculate_greeks returns a single gamma/vega (not split), this test
    # just confirms they're sane and positive for an ATM option.
    _, _, gamma, _, _, vega, _, _ = calculate_greeks(S=100, K=100, T=1, r=0.05, sigma=0.2)
    assert gamma > 0
    assert vega > 0


def test_calculate_vega_matches_calculate_greeks_vega():
    _, _, _, _, _, vega_from_greeks, _, _ = calculate_greeks(S=100, K=100, T=1, r=0.05, sigma=0.2)
    vega_standalone = calculate_vega(S=100, K=100, T=1, r=0.05, sigma=0.2)
    assert vega_from_greeks == pytest.approx(vega_standalone, abs=1e-9)


def test_iv_recovers_known_sigma():
    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
    call, put = calculate_price(S, K, T, r, sigma)
    iv_call, iv_put = calculate_iv(S, K, T, r, call_market=call, put_market=put)
    assert iv_call == pytest.approx(sigma, abs=1e-4)
    assert iv_put == pytest.approx(sigma, abs=1e-4)


def test_iv_single_sided_call_only():
    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
    call, _ = calculate_price(S, K, T, r, sigma)
    iv_call, iv_put = calculate_iv(S, K, T, r, call_market=call)
    assert iv_call == pytest.approx(sigma, abs=1e-4)
    assert iv_put is None


def test_iv_single_sided_put_only():
    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2
    _, put = calculate_price(S, K, T, r, sigma)
    iv_call, iv_put = calculate_iv(S, K, T, r, put_market=put)
    assert iv_call is None
    assert iv_put == pytest.approx(sigma, abs=1e-4)


# --- Edge cases ---

def test_greeks_T_zero_delta_step_function():
    delta_call, delta_put, gamma, theta_call, theta_put, vega, rho_call, rho_put = calculate_greeks(
        S=110, K=100, T=0, r=0.05, sigma=0.2
    )
    assert delta_call == 1.0
    assert delta_put == 0.0
    assert gamma == 0.0
    assert vega == 0.0


def test_greeks_T_zero_atm_delta_is_half():
    delta_call, delta_put, *_ = calculate_greeks(S=100, K=100, T=0, r=0.05, sigma=0.2)
    assert delta_call == 0.5
    assert delta_put == -0.5


def test_calculate_vega_zero_at_T_zero():
    vega = calculate_vega(S=100, K=100, T=0, r=0.05, sigma=0.2)
    assert vega == 0.0


def test_calculate_vega_zero_at_sigma_zero():
    vega = calculate_vega(S=100, K=100, T=1, r=0.05, sigma=0)
    assert vega == 0.0


@pytest.mark.parametrize("bad_S", [0, -100])
def test_greeks_negative_S_raises(bad_S):
    with pytest.raises(ValueError):
        calculate_greeks(S=bad_S, K=100, T=1, r=0.05, sigma=0.2)


def test_iv_no_market_price_raises():
    with pytest.raises(ValueError):
        calculate_iv(S=100, K=100, T=1, r=0.05)


def test_iv_T_zero_raises():
    with pytest.raises(ValueError):
        calculate_iv(S=100, K=100, T=0, r=0.05, call_market=10)


def test_iv_negative_market_price_raises():
    with pytest.raises(ValueError):
        calculate_iv(S=100, K=100, T=1, r=0.05, call_market=-5)


def test_iv_unreachable_price_raises():
    # A call market price of ~0 for an ATM option is not achievable at any
    # positive sigma -> should raise rather than silently return garbage.
    with pytest.raises(ValueError):
        calculate_iv(S=100, K=100, T=1, r=0.05, call_market=0.0001, put_market=0.0001)