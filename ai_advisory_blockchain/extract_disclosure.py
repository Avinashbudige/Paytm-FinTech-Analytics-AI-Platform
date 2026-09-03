import re

from disclosure_snippets import DISCLOSURE_SNIPPETS

def extract_signals(snippet: str) -> dict:
    """
    This function provides extra signals for the AI advisory blockchain system.
    It can be used to enhance decision-making processes by incorporating additional data points.
    """
    snippet = snippet.lower()

    risk_patterns = {
        "litigation": r"\blitigation\b",
        "regulatory": r"\bregulat(?:ory|or)\b|data[- ]locali[sz]ation|compliance",
        "customer concentration": r"(?:top\s+\w+\s+customers|customer concentration).*?\b(?:revenue|sales)\b|\b\d+\s*percent\b.*?\brevenue\b",
    }
    risk_flags = [
        flag for flag, pattern in risk_patterns.items()
        if re.search(pattern, snippet)
    ]

    hedging_phrases = (
        "assuming",
        "cautiously",
        "though",
        "visibility",
        "limited",
        "uncertainty",
    )
    hedging_detected = any(phrase in snippet for phrase in hedging_phrases)

    if re.search(r"\b(confident|approved)\b", snippet):
        sentiment = "confident"
    elif hedging_detected:
        sentiment = "cautious"
    else:
        sentiment = "neutral"

    return {
        "risk_flags": risk_flags,
        "hedging_detected": hedging_detected,
        "sentiment": sentiment,
    }


if __name__ == "__main__":
    for snippet in DISCLOSURE_SNIPPETS:
        signals = extract_signals(snippet)
        print(f"Snippet: {snippet}\nSignals: {signals}\n")
