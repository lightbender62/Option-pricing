"""
Example demonstrating PayoffDiagram for vanilla European call/put payoffs.

Run from the project root:
    python examples/visualization/payoff_diagram_example.py
"""

from option_pricing import PayoffDiagram

diagram = PayoffDiagram(K=100, premium=5)

diagram.call()
diagram.put()
diagram.both()