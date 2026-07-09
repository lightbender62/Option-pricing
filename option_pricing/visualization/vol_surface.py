"""
Volatility smile and surface visualization using real market data.
"""

import datetime

import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.interpolate import griddata

from option_pricing._core import calculate_iv


class VolatilitySurface:
    def __init__(self, ticker, r):
        self.ticker = ticker
        self.r = r
        self.data = yf.Ticker(ticker)
        history = self.data.history(period="1d")
        if history.empty:
            raise ValueError(f"No market data found for ticker '{ticker}'. Check the symbol is correct and actively traded.")

        self.S = history["Close"].iloc[-1]

        

    def available_expiries(self):
        """Return all available option expiry dates."""
        return self.data.options

    def _fetch_chain(self, expiry , surface = False):
        """Fetch liquid call options for the given expiry."""

        chain = self.data.option_chain(expiry)

        calls = chain.calls[
            ["strike", "bid", "ask", "volume", "openInterest"]
        ].dropna()

        # Keep only options with valid bid/ask quotes
        calls = calls[(calls["bid"] > 0) & (calls["ask"] > 0)]

        # Mid-market price
        calls["midPrice"] = (calls["bid"] + calls["ask"]) / 2

        # Liquidity filters
        calls = calls[calls["midPrice"] > 0.01]
        if surface:
            calls = calls[calls["volume"] > 50]
            calls = calls[calls["openInterest"] > 500]
        else:
            calls = calls[calls["volume"] > 10]
            calls = calls[calls["openInterest"] > 50]
        spread = (calls["ask"] - calls["bid"]) / calls["midPrice"]
        calls = calls[spread < 0.15]    

        # Keep strikes reasonably close to spot
        calls = calls[
            (calls["strike"] >= 0.5 * self.S)
            & (calls["strike"] <= 1.5 * self.S)
        ]

        return calls

    def _time_to_expiry(self, expiry):
        """Return time to expiry in years."""

        expiry_date = datetime.datetime.strptime(expiry, "%Y-%m-%d")
        today = datetime.datetime.today()

        delta = expiry_date - today
        return delta.total_seconds() / (365 * 24 * 3600)

    def _solve_iv(self, expiry , surface = False):
        """Compute implied volatilities for one expiry."""

        calls = self._fetch_chain(expiry , surface)

        if calls.empty:
            return None, None

        T = self._time_to_expiry(expiry)

        if T <= 0:
            return None, None

        strikes = []
        ivs = []

        for _, row in calls.iterrows():

            K = row["strike"]
            call_market = row["midPrice"]

            try:
                iv, _ = calculate_iv(
                    self.S,
                    K,
                    T,
                    self.r,
                    call_market,
                    call_market,
                )

                if 0.01 < iv < 2.0:
                    strikes.append(K)
                    ivs.append(iv)

            except Exception:
                continue

        return np.array(strikes), np.array(ivs)

    def smile(self, expiry):
        """Plot volatility smile for a single expiry."""

        strikes, ivs = self._solve_iv(expiry , False)

        if strikes is None or len(strikes) == 0:
            print(f"No data for expiry {expiry}")
            return

        # Sort before plotting
        idx = np.argsort(strikes)
        strikes = strikes[idx]
        ivs = ivs[idx]

        plt.figure(figsize=(10, 5))

        plt.plot(
            strikes,
            ivs * 100,
            color="navy",
            linewidth=2,
        )

        plt.scatter(
            strikes,
            ivs * 100,
            s=20,
        )

        plt.axvline(
            x=self.S,
            color="red",
            linestyle="--",
            label=f"Spot ({self.S:.1f})",
        )

        plt.title(
            f"Volatility Smile — {self.ticker} | Expiry: {expiry}"
        )

        plt.xlabel("Strike")
        plt.ylabel("Implied Volatility (%)")

        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def surface(self, num_expiries=30):
        """Plot 3D implied volatility surface."""

        expiries = self.data.options[:num_expiries]

        all_strikes = []
        all_T = []
        all_ivs = []

        for expiry in expiries:

            strikes, ivs = self._solve_iv(expiry , True)

            if strikes is None or len(strikes) < 3:
                continue

            T = self._time_to_expiry(expiry)

            if T < 7 / 365:
                continue

            all_strikes.extend(strikes)
            all_T.extend(np.full(len(strikes), T))
            all_ivs.extend(ivs)

        if not all_strikes:
            print("No data available.")
            return

        K_all = np.array(all_strikes)
        T_all = np.array(all_T)
        IV_all = np.array(all_ivs)

        K_grid = np.linspace(K_all.min(), K_all.max(), 75)
        T_grid = np.linspace(T_all.min(), T_all.max(), 75)

        K_mesh, T_mesh = np.meshgrid(K_grid, T_grid)

        IV_mesh = griddata(
            (K_all, T_all),
            IV_all * 100,
            (K_mesh, T_mesh),
            method="cubic",
            fill_value=np.nan,
        )

        IV_mesh = np.nan_to_num(IV_mesh, nan=0)
        IV_mesh = np.ma.masked_where(IV_mesh == 0, IV_mesh)

        IV_mesh = np.clip(IV_mesh, 5, 100)

        fig = go.Figure(
            data=[
                go.Surface(
                    x=K_mesh,
                    y=T_mesh,
                    z=IV_mesh,
                    colorscale="Blues",
                    colorbar=dict(title="IV (%)"),
                )
            ]
        )

        fig.update_layout(
            title=f"Volatility Surface — {self.ticker}",
            scene=dict(
                xaxis_title="Strike",
                yaxis_title="Time to Expiry (Years)",
                zaxis_title="Implied Volatility (%)",
            ),
            width=900,
            height=700,
        )

        fig.show()