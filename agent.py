
# fraud_agent/agent.py

from google.adk.agents import SequentialAgent

from agents import (
    data_agent,
    risk_agent,
    report_agent,
)


root_agent = SequentialAgent(
    name="fraud_detection_workflow",
    description=(
        "Runs transaction retrieval, fraud risk analysis, "
        "and investigation reporting in sequence."
    ),
    sub_agents=[
        data_agent,
        risk_agent,
        report_agent,
    ],
)
