# Option Pricing 
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Scientific%20Computing-013243?logo=numpy)
![SciPy](https://img.shields.io/badge/SciPy-Optimization-8CAAE6?logo=scipy)
![Last Commit](https://img.shields.io/github/last-commit/lightbender62/Option-pricing)
![Repo Size](https://img.shields.io/github/repo-size/lightbender62/Option-pricing)
![Status](https://img.shields.io/badge/Status-Active%20Development-success)

A Python library implementing classical option pricing models and quantitative finance analytics, developed as part of the IITI Summer of Code (IITI-SOC) program.

The project aims to provide a modular, easy-to-use implementation of widely used pricing models for European options, along with analytical tools such as option Greeks and implied volatility estimation. In addition to functioning as a Python package, the repository includes a command-line interface, example programs, and supporting documentation.
Currently, the library supports pricing European Call and Put options.

**Project Status:** This project is currently under active development. The core pricing models and analytical tools have been implemented, while additional features, documentation, visualizations, and pricing models will continue to be added over time.

---
## Features

### Pricing Models
- Black-Scholes analytical pricing model
- Cox-Ross-Rubinstein (CRR) Binomial Tree Model
- Monte Carlo Simulation using Geometric Brownian Motion

### Analytics
- Implied Volatility estimation using the Newton-Raphson method
- Calculation of Option Greeks
  - Delta
  - Gamma
  - Theta
  - Vega
  - Rho

### Utilities
- Interactive command-line interface (`main.py`)
- Modular Python package
- Individual example scripts for each implemented model
- Supporting theoretical documentation

---
## Project Structure
```
Option-pricing/
│
├── docs/
│   ├── README.md
│   ├── theory/                      # Mathematical references and notes
│   └── report/                      # Reports made for evaluations  
│
├── examples/                        # Example scripts
│   ├── black_scholes_example.py
│   ├── binomial_model_example.py
│   ├── monte_carlo_example.py
│   ├── greeks_example.py
│   └── implied_volatility_example.py
│
├── option_pricing/
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── greeks.py
│   │   └── implied_volatility.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── black_scholes.py
│   │   ├── binomial_model.py
│   │   └── monte_carlo.py
│   │
│   └── __init__.py
│
├── .gitignore
├── main.py                          # Interactive CLI
├── pyproject.toml                   # Package configuration
├── README.md
└── requirements.txt
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
- Delta
- Gamma
- Theta
- Vega
- Rho

---
## Installation
Clone the repository:

```bash
git clone https://github.com/lightbender62/Option-pricing.git
cd Option-pricing
```

Create and activate a virtual environment (recommended):

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

Install the package:

```bash
pip install .
```

Run the demo:

```bash
python main.py
```

---
## Quick Start
Run the interactive command-line application
```bash
python main.py
```
or use the library directly
```python
from option_pricing import Calculate_Price

call, put = Calculate_Price(
    S=100,
    K=100,
    T=1,
    r=0.05,
    vol=0.20,
)

print(call)
print(put)
```
Examples demonstrating the usage of each pricing model are available in the `examples/` directory.


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

#### Greeks Validation

| Greek | Call | Put |
|:------|-----:|----:|
| Delta | 0.636831 | -0.363169 |
| Gamma | 0.018762 | 0.018762 |
| Theta | -6.414028 | -1.657880 |
| Vega | 37.524035 | 37.524035 |
| Rho | 53.232482 | -41.890461 |

The calculated Greeks closely match the expected analytical values for the given test case.

#### Implied Volatility Validation

| Method | Implied Volatility |
|:------|-------------------:|
| Newton-Raphson | 0.200000 |

The implied volatility solver converges to the expected market volatility for the given option price, confirming the accuracy of the Newton-Raphson implementation.

---
## Documentation

Supporting documentation and reference material are available in the `docs/` directory.

### Contents

#### `theory/`

Contains the theoretical references and study material used during the implementation of the pricing models, including:

* Black-Scholes Theory
* Risk-Neutral Valuation
* Stochastic Processes
* Itô Calculus
* Option Greeks

These references were used to understand the mathematical foundations of the implemented algorithms and to verify their correctness.

#### `report/`

Contains project reports and documentation prepared throughout the development of the project, including the IITI Summer of Code (IITI-SOC) mid-evaluation report and future project reports.

The documentation is intended to complement the source code by providing both the mathematical background and the project's development progress.

---
## Future Work
Planned additions include : 
- Support for American options
- Additional pricing models
- Performance optimizations
- More visualization utilities
- Expanded documentation
- Additional examples and tutorials
- Packaging for PyPI distribution

---
## Team

| Name | Roll Number | GitHub |
|------|------------:|--------|
| Eklavya | 250001028 | [@lightbender62](https://github.com/lightbender62) |
| Soham Gupta | 250003073 | [@aspiringchoker](https://github.com/aspiringchoker) |
| Prasad Wagh | 250004051 | [@ce250004051](https://github.com/ce250004051) |
| Parth Kalia | 250001054 | [@Parth-250001054](https://github.com/Parth-250001054) |
