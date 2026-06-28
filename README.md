# Option Pricing
A Project developed by our team for **IITI Summer of Code (IITI-SOC)** program. This is a Python Library implementing several option pricing models used in quantitative finance. This project, when completed will provide analytical and visual aid, for several option models, and their Greeks.The repository is currently under active development, and new features and improvements will be added over time. The sections below describe the features implemented so far and provide instructions for installing and using the library.

---
## Features
- Black-Scholes analytical pricing model
- Cox-Ross-Rubinstein (CRR) Binomial Tree Model
- Monte Carlo Simulation using Geometric Brownian Motion
- Implied Volatility estimation using the Newton-Raphson method
- Calculation of Option Greeks
  - Delta
  - Gamma
  - Theta
  - Vega
  - Rho
- Interactive command-line interface
---
## Project Structure
```text
Option-pricing/
│
├── Theory/                  # Project documentation and notes
├── .gitignore
├── README.md
├── main.py                  # Main executable
├── black_scholes.py         # Black-Scholes pricing model
├── Binomial_model.py        # Binomial pricing model
├── Monte_Carlo.py           # Monte Carlo simulation
├── Greeks.py                # Option Greeks
└── Implied_Volatility.py    # Implied volatility calculation
```
---
## Mathematical Models
### 1. Black-Scholes Model
Provides a closed form solution for pricing European Call and Put Options under the assumption of constant volatility, constant risk-free interest rate, and lognormally distributed stock prices.

---
### 2. Binomial Pricing Model
Implements the Cox-Ross-Rubinstein (CRR) binomial tree to price European options through backward induction.

---
### 3. Monte Carlo Simulation
Simulates stock price paths using Geometric Brownian Motion (GBM) and estimates option prices by discounting the average payoff at maturity.

---
### 4. Implied Volatility
Computes the volatility implied by a market option price using the Newton-Raphson iterative method.

---
### 5. Greeks
Calculates the primary risk sensitivities of European options:
-Delta
-Gamma
-Theta
-Vega
-Rho

---
## Installation
```bash
git clone https://github.com/lightbender62/Option-pricing.git
cd Option-pricing
```

Install the required dependencies
```bash
pip install -r requirements.txt
```

Or install the package locally
```bash
pip install -e .
```

---
## Dependencies
- Python 3.10+
- NumPy
- SciPy

---
## Input Parameters

### Common Parameters

| Parameter | Description |
|:---------:|-------------|
| **S** | Current price of the underlying asset (Spot Price). |
| **K** | Strike price of the option. |
| **T** | Time to maturity (in years). |
| **r** | Risk-free interest rate (decimal form). |
| **σ (vol)** | Annual volatility (decimal form). |

### Model-Specific Parameters

| Parameter | Used In | Description |
|:---------:|:-------:|-------------|
| **N** | Binomial Tree | Number of time steps in the tree. |
| **M** | Monte Carlo | Number of simulated stock price paths. |
| **Cm** | Implied Volatility | Market call option price. |
| **Pm** | Implied Volatility | Market put option price. |
---

## Validation & Testing
To Validate the results by our algorithms, the outputs of all pricing models were compared by using identical input parameters. We use Black-scholes model as benchmark, and Binomial Tree and Monte Carlo methods were evaluated based on their convergence to the Black-Scholes Model solution.

### Cross-Model Validation

Example Input:

| Parameter | Value |
|-----------|------:|
| Stock Price (S) | 100 |
| Strike Price (K) | 100 |
| Time to Maturity (T) | 1 year |
| Risk-free Rate (r) | 0.05 |
| Volatility (σ) | 0.20 |

#### Option Pricing Results

| Model | Call Price | Put Price | Error vs BS |
|:------|-----------:|----------:|:-----------:|
| Black-Scholes | 10.450584 | 5.573526 | — |
| Binomial Tree (N = 500) | 10.484155 | 5.578729 | 0.32% |
| Monte Carlo (M = 100000) | 10.446585 | 5.569528 | 0.04% |

The close agreement in between of three models, shows the validity of the results. The result gets more accurate, when Time steps(N) for Binomial Tree, and number of Simulations(M) for Monte carlo are increased.

#### Greeks

| Greek | Call | Put |
|:------|-----:|----:|
| Delta | 0.636831 | -0.363169 |
| Gamma | 0.018762 | 0.018762 |
| Theta | -6.414028 | -1.657880 |
| Vega | 37.524035 | 37.524035 |
| Rho | 53.232482 | -41.890461 |

The calculated Greeks closely match the expected analytical values for the given test case.

#### Implied Volatility

| Method | Implied Volatility |
|:------|-------------------:|
| Newton-Raphson | 0.200000 |

The implied volatility solver converges to the expected market volatility for the given option price, confirming the accuracy of the Newton-Raphson implementation.

---
## Team

| Name | Roll Number | GitHub |
|------|------------:|--------|
| Eklavya | 250001028 | [@lightbender62](https://github.com/lightbender62) |
| Soham Gupta | 250003073 | [@aspiringchoker](https://github.com/aspiringchoker) |
| Prasad Wagh | 250004051 | [@ce250004051](https://github.com/ce250004051) |
| Parth Kalia | 250001054 | [@Parth-250001054](https://github.com/Parth-250001054) |
