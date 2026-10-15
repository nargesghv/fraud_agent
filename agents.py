
# fraud_agent/agents.py

from google.adk.agents import LlmAgent

from tools import (
    check_transaction,
    calculate_risk_score,
)


MODEL = "gemini-3.1-flash-lite"


# Agent 1: Retrieve transaction data
data_agent = LlmAgent(
    name="data_agent",
    model=MODEL,
    description="Retrieves transaction evidence.",
    instruction="""
You are a transaction data retrieval specialist.

The user will provide a transaction ID.

Your tasks:
1. Call check_transaction with that ID.
2. Return the transaction information.
3. Do not invent or modify transaction values.

If the transaction does not exist, report
status: not_found.

Do not calculate fraud risk.
""",
    tools=[check_transaction],
    output_key="transaction_data",
)


# Agent 2: Calculate risk
risk_agent = LlmAgent(
    name="risk_agent",
    model=MODEL,
    description="Calculates fraud risk.",
    instruction="""
You are a fraud risk analysis specialist.

Transaction evidence:
{transaction_data}

Your tasks:
1. Identify the transaction ID in the evidence.
2. If the transaction exists, call
   calculate_risk_score with that ID.
3. Explain the returned score and indicators.

If the transaction was not found, explain
that scoring cannot be performed.

Never invent or modify a risk score.
""",
    tools=[calculate_risk_score],
    output_key="risk_analysis",
)


# Agent 3: Prepare report
report_agent = LlmAgent(
    name="report_agent",
    model=MODEL,
    description="Prepares investigation reports.",
    instruction="""
You are a financial fraud reporting specialist.

Transaction evidence:
{transaction_data}

Risk analysis:
{risk_analysis}

Create a concise investigation report with:

1. Transaction ID
2. Transaction details
3. Risk score and risk level
4. Suspicious indicators
5. Recommended investigation steps

Rules:
- Do not invent missing evidence.
- Do not change the calculated score.
- Distinguish suspicious activity from proven fraud.
- Do not make final account-blocking decisions.
""",
    output_key="final_report",
)
