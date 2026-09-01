import math
import os
from itertools import combinations
from stock_universe import STOCK_UNIVERSE, RISK_FREE_RATE, MARKET_RETURN
from investor_profiles import INVESTOR_PROFILES

# Prescribed lookup table
ALLOCATION_RULES = {
    "Conservative": ["PAYBOND", "PAYGOLD", "PAYRETAIL"],
    "Moderate": ["PAYRETAIL", "PAYINFRA", "PAYGOLD"],
    "Aggressive": ["PAYTECH", "PAYFIN", "PAYINFRA"],
}

# ---------------------------------------------------------
# Tool Call: Act stage
# ---------------------------------------------------------
def get_stock_data(ticker: str) -> dict:
    """Tool function simulating an external API lookup for stock fundamentals."""
    if ticker not in STOCK_UNIVERSE:
        raise ValueError(f"Ticker '{ticker}' not found in stock universe.")
    return STOCK_UNIVERSE[ticker]


# ---------------------------------------------------------
# LLM Generation Helper (Mock default vs Optional Groq)
# ---------------------------------------------------------
def generate_recommendation_narrative(
    investor_id: str,
    risk_tolerance: str,
    tickers: list[str],
    exp_return: float,
    volatility: float,
    escalated: bool
) -> str:
    mock_mode = os.environ.get("MOCK_LLM", "1") == "1"

    if mock_mode:
        if escalated:
            return (
                f"For {risk_tolerance} investor {investor_id}, the recommended allocation across "
                f"{', '.join(tickers)} yielded an expected return of {exp_return:.2%} with volatility of "
                f"{volatility:.2%}, triggering an ESCALATED_TO_HUMAN_ADVISOR status due to high risk."
            )
        return (
            f"For {risk_tolerance} investor {investor_id}, we recommend an allocation across "
            f"{', '.join(tickers)} with an expected portfolio return of {exp_return:.2%} and "
            f"volatility of {volatility:.2%}."
        )

    # Optional MOCK_LLM=0 extension via Groq API
    try:
        from groq import Groq
        client = Groq()
        prompt = (
            f"Summarize this investment advisory recommendation in 1-2 professional sentences:\n"
            f"Investor ID: {investor_id}, Profile: {risk_tolerance}\n"
            f"Equally-weighted portfolio: {', '.join(tickers)}\n"
            f"Expected Return: {exp_return:.2%}, Volatility: {volatility:.2%}\n"
            f"Status: {'ESCALATED_TO_HUMAN_ADVISOR' if escalated else 'APPROVED'}"
        )
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return completion.choices[0].message.content.strip()
    except Exception as err:
        # Graceful fallback if Groq API key is missing or encounters a rate limit
        return (
            f"[Fallback] For {risk_tolerance} investor {investor_id}, recommended allocation across "
            f"{', '.join(tickers)} has expected return {exp_return:.2%} and volatility {volatility:.2%} "
            f"(API error: {err})."
        )


# ---------------------------------------------------------
# Agent Loop: Think-Act-Observe Pattern
# ---------------------------------------------------------
def run_advisory_agent(investor: dict, rho: float = 0.3) -> dict:
    investor_id = investor["investor_id"]
    risk_tolerance = investor["risk_tolerance"]

    # 1. THINK: Map investor profile to prescribed asset allocation
    if risk_tolerance not in ALLOCATION_RULES:
        raise ValueError(f"Unknown risk tolerance: {risk_tolerance}")
    prescribed_tickers = ALLOCATION_RULES[risk_tolerance]
    weight = 1.0 / len(prescribed_tickers)  # Equal weight: 1/3 each

    # 2. ACT: Invoke tool call to fetch stock data for each asset
    assets_data = {ticker: get_stock_data(ticker) for ticker in prescribed_tickers}

    # 3. OBSERVE -> DECIDE:
    # Compute CAPM Expected Return per stock: E(R) = Rf + beta * (Rm - Rf)
    market_risk_premium = MARKET_RETURN - RISK_FREE_RATE  # 0.13 - 0.07 = 0.06
    stock_returns = {}
    for ticker, data in assets_data.items():
        stock_returns[ticker] = RISK_FREE_RATE + (data["beta"] * market_risk_premium)

    portfolio_expected_return = sum(weight * stock_returns[t] for t in prescribed_tickers)

    # Compute Portfolio Variance:
    # Var(Rp) = sum(w_i^2 * sigma_i^2) + 2 * sum_{i < j}(w_i * w_j * Cov(Ri, Rj))
    # where Cov(Ri, Rj) = rho * sigma_i * sigma_j
    variance_individual = sum((weight ** 2) * (assets_data[t]["std_dev"] ** 2) for t in prescribed_tickers)

    covariance_terms = 0.0
    for t_i, t_j in combinations(prescribed_tickers, 2):
        sigma_i = assets_data[t_i]["std_dev"]
        sigma_j = assets_data[t_j]["std_dev"]
        covariance_terms += weight * weight * (rho * sigma_i * sigma_j)

    portfolio_variance = variance_individual + (2 * covariance_terms)
    portfolio_std_dev = math.sqrt(portfolio_variance)

    # Human-In-The-Loop Escalation rule (> 20% volatility)
    is_escalated = portfolio_std_dev > 0.20
    status = "ESCALATED_TO_HUMAN_ADVISOR" if is_escalated else "FINALIZED"

    # Generate narrative
    narrative = generate_recommendation_narrative(
        investor_id=investor_id,
        risk_tolerance=risk_tolerance,
        tickers=prescribed_tickers,
        exp_return=portfolio_expected_return,
        volatility=portfolio_std_dev,
        escalated=is_escalated,
    )

    return {
        "investor_id": investor_id,
        "risk_tolerance": risk_tolerance,
        "allocation": {ticker: round(weight, 4) for ticker in prescribed_tickers},
        "expected_return": round(portfolio_expected_return, 4),
        "portfolio_variance": round(portfolio_variance, 6),
        "portfolio_std_dev": round(portfolio_std_dev, 4),
        "status": status,
        "narrative": narrative,
    }


if __name__ == "__main__":
    print("=" * 80)
    print("RUNNING ADVISORY AGENT ON ALL INVESTOR PROFILES (MOCK_LLM=1)")
    print("=" * 80)

    for profile in INVESTOR_PROFILES:
        result = run_advisory_agent(profile)
        print(f"\nInvestor: {result['investor_id']} ({result['risk_tolerance']})")
        print(f"Status:          {result['status']}")
        print(f"Tickers:         {list(result['allocation'].keys())}")
        print(f"Expected Return: {result['expected_return']:.2%}")
        print(f"Volatility (SD): {result['portfolio_std_dev']:.2%}")
        print(f"Narrative:       {result['narrative']}")