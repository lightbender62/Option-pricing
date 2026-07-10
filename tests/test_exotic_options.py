"""
Tests for option_pricing.exotic: AsianOption, BarrierOption, LookbackOption
"""
import pytest

from option_pricing import AsianOption, BarrierOption, LookbackOption, EuropeanOption


# --- Asian ---

def test_asian_arithmetic_and_geometric_positive(atm_asian):
    assert atm_asian.call(average="arithmetic") > 0
    assert atm_asian.call(average="geometric") > 0


def test_asian_unknown_average_raises(atm_asian):
    with pytest.raises(ValueError):
        atm_asian.call(average="banana")


def test_asian_negative_K_raises():
    with pytest.raises(ValueError):
        AsianOption(S=100, K=-100, T=1, r=0.05, sigma=0.2).call()


# --- Barrier ---

def test_barrier_in_out_parity_roughly_matches_vanilla(
    down_and_out_barrier, down_and_in_barrier
):
    vanilla = EuropeanOption(S=100, K=100, T=1, r=0.05, sigma=0.2)
    combined = down_and_out_barrier.call() + down_and_in_barrier.call()
    assert combined == pytest.approx(vanilla.call(model="montecarlo"), abs=1.0)


@pytest.mark.parametrize("barrier_type", ["down-and-out", "down-and-in", "up-and-out", "up-and-in"])
def test_all_barrier_types_run(barrier_type):
    H = 90 if "down" in barrier_type else 110
    opt = BarrierOption(S=100, K=100, T=1, r=0.05, sigma=0.2, H=H, barrier_type=barrier_type)
    assert opt.call() >= 0
    assert opt.put() >= 0


def test_barrier_invalid_H_direction_raises():
    with pytest.raises(ValueError):
        BarrierOption(S=100, K=100, T=1, r=0.05, sigma=0.2, H=150, barrier_type="down-and-out").call()


def test_barrier_unknown_type_raises():
    with pytest.raises(ValueError):
        BarrierOption(S=100, K=100, T=1, r=0.05, sigma=0.2, H=90, barrier_type="sideways").call()


# --- Lookback ---

def test_lookback_floating_and_fixed_positive(atm_lookback):
    assert atm_lookback.call(strike_type="floating") >= 0
    assert atm_lookback.call(strike_type="fixed") >= 0


def test_lookback_unknown_strike_type_raises(atm_lookback):
    with pytest.raises(ValueError):
        atm_lookback.call(strike_type="banana")


def test_lookback_call_gte_vanilla_call(atm_lookback):
    # Lookback call (best possible exercise) should be worth at least as
    # much as an equivalent vanilla call.
    vanilla = EuropeanOption(S=100, K=100, T=1, r=0.05, sigma=0.2)
    assert atm_lookback.call(strike_type="fixed") >= vanilla.call(model="montecarlo") - 1.0