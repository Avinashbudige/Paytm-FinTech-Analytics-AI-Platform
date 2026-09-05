from  stock_universe import STOCK_UNIVERSE
import pandas as pd

base_fcff = 1000  # in INR crores
tax_rate = 0.30
beta = 1.35  # pick from STOCK_UNIVERSE
risk_free_rate = 0.07
market_return = 0.13
cost_of_debt = 0.08
equity_weight = 0.70  # 70% equity
debt_weight = 0.30   # 30% debt 

# Cost of Equity using CAPM
r_e = risk_free_rate + beta * (market_return - risk_free_rate)

# WACC
wacc = (equity_weight * r_e) + (debt_weight * cost_of_debt * (1 - tax_rate))

# Terminal growth rate (lower than WACC)
terminal_growth = 0.05  # 5%

# Constraint check
print(f"WACC: {wacc:.2%}, Terminal Growth: {terminal_growth:.2%}")
print(f"Spread: {(wacc - terminal_growth):.2%} (must be ≥ 1%)") 

# Define declining growth rates for 5 years
growth_rates = [0.20, 0.18, 0.15, 0.12, 0.08]  # declining each year

fcf_projections = []
fcf = base_fcff

for year, growth in enumerate(growth_rates, 1):
    fcf = fcf * (1 + growth)
    fcf_projections.append(fcf)
    print(f"Year {year}: FCF = {fcf:.2f}") 

# Terminal value at end of Year 5
terminal_fcf = fcf_projections[-1] * (1 + terminal_growth)
terminal_value = terminal_fcf / (wacc - terminal_growth)

print(f"Terminal Value: {terminal_value:.2f}") 

# Discount 5-year projections
pv_fcf = sum([fcf / ((1 + wacc) ** (i + 1)) 
              for i, fcf in enumerate(fcf_projections)])

# Discount terminal value
pv_terminal = terminal_value / ((1 + wacc) ** 5)

# Enterprise Value
enterprise_value = pv_fcf + pv_terminal

print(f"PV of FCF (5 years): {pv_fcf:.2f}")
print(f"PV of Terminal Value: {pv_terminal:.2f}")
print(f"Enterprise Value: {enterprise_value:.2f}")

# Vary WACC and terminal growth by ±1 percentage point
wacc_range = [wacc - 0.01, wacc, wacc + 0.01]
growth_range = [terminal_growth - 0.01, terminal_growth, terminal_growth + 0.01]

sensitivity_table = pd.DataFrame(index=[f"{g:.1%}" for g in growth_range],
                                 columns=[f"{w:.1%}" for w in wacc_range])

for w in wacc_range:
    for g in growth_range:
        if w - g >= 0.01:  # Check constraint
            # Recalculate EV with new parameters
            tv = fcf_projections[-1] * (1 + g) / (w - g)
            pv = sum([f / ((1 + w) ** (i + 1)) 
                     for i, f in enumerate(fcf_projections)]) + tv / ((1 + w) ** 5)
            sensitivity_table.loc[f"{g:.1%}", f"{w:.1%}"] = pv
        else:
            sensitivity_table.loc[f"{g:.1%}", f"{w:.1%}"] = "Invalid"

print("\nSensitivity Analysis (Enterprise Value):")
print(sensitivity_table)

# Choose an illustrative EBITDA and multiple
illustrative_ebitda = 200  # in INR crores
ebitda_multiple = 12  # typical for fintech

ebitda_valuation = illustrative_ebitda * ebitda_multiple

print(f"\nEBITDA-based Valuation: {ebitda_valuation:.2f}")
print(f"DCF Valuation: {enterprise_value:.2f}")
print(f"Comparison: DCF is {((enterprise_value/ebitda_valuation - 1) * 100):.1f}% {'higher' if enterprise_value > ebitda_valuation else 'lower'}")
print(f"\nComment: The DCF approach values the business higher/lower due to [explain growth assumptions]")