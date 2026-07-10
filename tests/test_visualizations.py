"""
Smoke tests for option_pricing.visualization.

These don't check pixel output, just that each .plot()-equivalent call
runs without raising, and that bad inputs correctly raise ValueError.
Uses the Agg backend so no windows pop up during test runs.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from option_pricing import (
    PricingCurves,
    GreeksProfile,
    PayoffDiagram,
    MonteCarloVisualization,
    ConvergenceAnalysis,
    PriceHeatmap,
    AsianPayoff,
    BarrierPayoff,
    LookbackPayoff,
)

S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2


@pytest.fixture(autouse=True)
def close_all_figures():
    yield
    plt.close("all")


def test_pricing_curves_all_params():
    curves = PricingCurves(S=S, K=K, T=T, r=r, sigma=sigma)
    for param in ("stock", "volatility", "time", "rate"):
        curves.plot(param=param)


def test_pricing_curves_unknown_param_raises():
    curves = PricingCurves(S=S, K=K, T=T, r=r, sigma=sigma)
    with pytest.raises(ValueError):
        curves.plot(param="banana")


def test_greeks_profile_all_greeks():
    profile = GreeksProfile(S=S, K=K, T=T, r=r, sigma=sigma)
    for greek in ("delta", "gamma", "theta", "vega", "rho"):
        profile.plot(greek=greek)


def test_greeks_profile_unknown_greek_raises():
    profile = GreeksProfile(S=S, K=K, T=T, r=r, sigma=sigma)
    with pytest.raises(ValueError):
        profile.plot(greek="banana")


def test_payoff_diagram_call_put_both():
    diagram = PayoffDiagram(K=K, premium=5)
    diagram.call()
    diagram.put()
    diagram.both()


def test_payoff_diagram_negative_premium_raises():
    with pytest.raises(ValueError):
        PayoffDiagram(K=K, premium=-5)


def test_monte_carlo_visualization_paths_and_distribution():
    mc = MonteCarloVisualization(S=S, K=K, T=T, r=r, sigma=sigma, N=50, M=500)
    mc.plot(kind="paths", num_paths=20)
    mc.plot(kind="distribution")


def test_monte_carlo_visualization_barrier_lookback_asian():
    mc = MonteCarloVisualization(S=S, K=K, T=T, r=r, sigma=sigma, N=50, M=500)
    mc.plot(kind="barrier", H=90, barrier_type="down-and-out", num_paths=20)
    mc.plot(kind="lookback", num_paths=5)
    mc.plot(kind="asian", num_paths=5)


def test_monte_carlo_visualization_barrier_missing_args_raises():
    mc = MonteCarloVisualization(S=S, K=K, T=T, r=r, sigma=sigma, N=50, M=500)
    with pytest.raises(ValueError):
        mc.plot(kind="barrier")


def test_convergence_analysis_mc_and_binomial():
    conv = ConvergenceAnalysis(S=S, K=K, T=T, r=r, sigma=sigma)
    conv.plot(kind="mc")
    conv.plot(kind="binomial")


def test_price_heatmap_call_and_put():
    heatmap = PriceHeatmap(S=S, K=K, T=T, r=r, sigma=sigma)
    heatmap.plot(option="call")
    heatmap.plot(option="put")


def test_price_heatmap_unknown_option_raises():
    heatmap = PriceHeatmap(S=S, K=K, T=T, r=r, sigma=sigma)
    with pytest.raises(ValueError):
        heatmap.plot(option="banana")


def test_asian_payoff_both_averages():
    payoff = AsianPayoff(S=S, K=K, T=T, r=r, sigma=sigma, N=50, M=500)
    payoff.plot(average="arithmetic")
    payoff.plot(average="geometric")


def test_barrier_payoff_runs():
    payoff = BarrierPayoff(S=S, K=K, T=T, r=r, sigma=sigma, N=50, M=500)
    payoff.plot(H=90, barrier_type="down-and-out")


def test_lookback_payoff_both_strike_types():
    payoff = LookbackPayoff(S=S, K=K, T=T, r=r, sigma=sigma, N=50, M=500)
    payoff.plot(strike_type="floating")
    payoff.plot(strike_type="fixed")