"""
Tests for option_pricing._core.black_scholes
"""
import pytest

from option_pricing._core.black_scholes import calculate_price, asian_price_geometric


# --- Correctness ---

def test_known_atm_call_put():
    # Textbook reference values for S=K=100, T=1, r=0.05, sigma=0.2
    call, put = calculate_price(S=100, K=100, T=1, r=0.05, sigma=0.2)
    assert call == pytest.approx(10.4506, abs=0.01)
    assert put == pytest.approx(5.5735, abs=0.01)


def test_put_call_parity():
    # C - P == S - K*exp(-rT)
    S, K, T, r, sigma = 105, 100, 0.5, 0.03, 0.25
    call, put = calculate_price(S, K, T, r, sigma)
    lhs = call - put
    rhs = S - K * (2.718281828 ** (-r * T))
    assert lhs == pytest.approx(rhs, abs=1e-6)


def test_deep_itm_call_converges_to_intrinsic_forward():
    call, _ = calculate_price(S=1000, K=100, T=1, r=0.05, sigma=0.2)
    assert call > 900  # deep ITM call should be close to S - K*disc


def test_deep_otm_call_near_zero():
    call, _ = calculate_price(S=50, K=1000, T=0.1, r=0.05, sigma=0.2)
    assert call < 0.01


# --- Edge cases ---

def test_T_zero_returns_intrinsic_value():
    call, put = calculate_price(S=110, K=100, T=0, r=0.05, sigma=0.2)
    assert call == pytest.approx(10.0)
    assert put == pytest.approx(0.0)


def test_sigma_zero_deterministic():
    call, put = calculate_price(S=100, K=100, T=1, r=0.05, sigma=0)
    forward = 100 * (2.718281828 ** 0.05)
    assert call == pytest.approx(max(forward - 100, 0) * (2.718281828 ** -0.05), rel=1e-3)
    assert put == pytest.approx(0.0)


@pytest.mark.parametrize("bad_S", [0, -1, -100])
def test_negative_or_zero_S_raises(bad_S):
    with pytest.raises(ValueError):
        calculate_price(S=bad_S, K=100, T=1, r=0.05, sigma=0.2)


@pytest.mark.parametrize("bad_K", [0, -1, -100])
def test_negative_or_zero_K_raises(bad_K):
    with pytest.raises(ValueError):
        calculate_price(S=100, K=bad_K, T=1, r=0.05, sigma=0.2)


def test_negative_T_raises():
    with pytest.raises(ValueError):
        calculate_price(S=100, K=100, T=-1, r=0.05, sigma=0.2)


def test_negative_sigma_raises():
    with pytest.raises(ValueError):
        calculate_price(S=100, K=100, T=1, r=0.05, sigma=-0.2)


# --- Asian geometric-average closed form ---

def test_asian_geometric_T_zero_reduces_to_spot():
    call, put = asian_price_geometric(S=110, K=100, T=0, r=0.05, sigma=0.2)
    assert call == pytest.approx(10.0)
    assert put == pytest.approx(0.0)


def test_asian_geometric_matches_general_formula_as_sigma_shrinks():
    S, K, T, r = 100, 100, 1, 0.05
    tiny_sigma_price, _ = asian_price_geometric(S, K, T, r, sigma=1e-6)
    zero_sigma_price, _ = asian_price_geometric(S, K, T, r, sigma=0)
    assert tiny_sigma_price == pytest.approx(zero_sigma_price, abs=1e-4)