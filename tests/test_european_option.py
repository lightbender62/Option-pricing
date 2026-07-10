"""
Tests for option_pricing.european.EuropeanOption
"""
import pytest

from option_pricing import EuropeanOption


# --- Correctness ---

@pytest.mark.parametrize("model", ["black_scholes", "binomial", "montecarlo"])
def test_call_and_put_positive_across_models(atm_european, model):
    assert atm_european.call(model=model) > 0
    assert atm_european.put(model=model) > 0


def test_models_roughly_agree():
    opt = EuropeanOption(S=100, K=100, T=1, r=0.05, sigma=0.2)
    bs_call = opt.call(model="black_scholes")
    bin_call = opt.call(model="binomial", steps=500)
    mc_call = opt.call(model="montecarlo", steps=100, paths=100000)
    assert bin_call == pytest.approx(bs_call, abs=0.1)
    assert mc_call == pytest.approx(bs_call, abs=0.2)


def test_greeks_dict_has_all_keys(atm_european):
    g = atm_european.greeks()
    expected_keys = {
        "delta_call", "delta_put", "gamma", "theta_call",
        "theta_put", "vega", "rho_call", "rho_put",
    }
    assert set(g.keys()) == expected_keys


def test_implied_vol_round_trip(atm_european):
    call = atm_european.call(model="black_scholes")
    put = atm_european.put(model="black_scholes")
    iv_call, iv_put = atm_european.implied_vol(call_price=call, put_price=put)
    assert iv_call == pytest.approx(0.2, abs=1e-4)
    assert iv_put == pytest.approx(0.2, abs=1e-4)


def test_implied_vol_single_sided(atm_european):
    call = atm_european.call(model="black_scholes")
    iv_call = atm_european.implied_vol(call_price=call)
    assert iv_call == pytest.approx(0.2, abs=1e-4)

    put = atm_european.put(model="black_scholes")
    iv_put = atm_european.implied_vol(put_price=put)
    assert iv_put == pytest.approx(0.2, abs=1e-4)


# --- Edge cases ---

def test_unknown_model_raises(atm_european):
    with pytest.raises(ValueError):
        atm_european.call(model="quantum")


def test_implied_vol_no_args_raises(atm_european):
    with pytest.raises(ValueError):
        atm_european.implied_vol()


def test_negative_S_raises():
    with pytest.raises(ValueError):
        EuropeanOption(S=-100, K=100, T=1, r=0.05, sigma=0.2).call()