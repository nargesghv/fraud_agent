
# fraud_agent/tools.py

from google.adk.tools import ToolContext
from data import TRANSACTIONS


def check_transaction(transaction_id: str) -> dict:
    """Retrieve a transaction by its ID.

    Args:
        transaction_id: Unique transaction identifier.
    """
    transaction = TRANSACTIONS.get(transaction_id)

    if transaction is None:
        return {
            "status": "not_found",
            "transaction_id": transaction_id,
        }

    return {
        "status": "success",
        "transaction": transaction.copy(),
    }


def calculate_risk_score(transaction_id: str) -> dict:
    """Calculate a rule-based fraud risk score.

    The score is computed from stored transaction data.

    Args:
        transaction_id: Transaction identifier to score.
    """
    transaction = TRANSACTIONS.get(transaction_id)

    if transaction is None:
        return {
            "status": "not_found",
            "transaction_id": transaction_id,
        }

    score = 0
    indicators = []

    if transaction["amount"] > 10000:
        score += 30
        indicators.append("Large transaction amount")

    if transaction["failed_attempts"] >= 3:
        score += 35
        indicators.append("Multiple failed attempts")

    if transaction["country"] != transaction["usual_country"]:
        score += 35
        indicators.append("Country mismatch")

    score = min(score, 100)

    if score >= 70:
        risk_level = "high"
    elif score >= 35:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "status": "success",
        "transaction_id": transaction_id,
        "risk_score": score,
        "risk_level": risk_level,
        "indicators": indicators,
        "scoring_method": "demo_rule_based",
    }


def save_fraud_score(
    transaction_id: str,
    tool_context: ToolContext,
) -> dict:
    """Calculate and save a transaction's risk in session state.

    Args:
        transaction_id: Transaction identifier to save.
    """
    result = calculate_risk_score(transaction_id)

    if result["status"] != "success":
        return result

    tool_context.state["current_transaction"] = transaction_id
    tool_context.state["risk_score"] = result["risk_score"]
    tool_context.state["risk_level"] = result["risk_level"]
    tool_context.state["risk_indicators"] = result["indicators"]

    return {
        **result,
        "saved_to_session": True,
    }
