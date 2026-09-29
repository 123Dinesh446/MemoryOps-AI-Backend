import os
from hindsight_client import Hindsight
from dotenv import load_dotenv

load_dotenv()

HINDSIGHT_URL = os.getenv(
    "HINDSIGHT_API_URL",
    "https://api.hindsight.vectorize.io"
)

HINDSIGHT_KEY = os.getenv("HINDSIGHT_API_KEY")
BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "memoryops-ai")

client = Hindsight(
    base_url=HINDSIGHT_URL,
    api_key=HINDSIGHT_KEY
)


def setup_bank():
    try:
        client.create_bank(
            bank_id=BANK_ID,
            name="MemoryOps AI Incident Memory"
        )
        return True
    except Exception:
        return True


def store_incident(incident, diagnosis):
    content = f"""
Production Incident Record

Service: {incident.service}
Error: {incident.error}
Logs: {incident.logs}
Description: {incident.description}

AI Diagnosis:
Root Cause: {diagnosis.get("root_cause", "")}
Recommended Fix: {diagnosis.get("recommended_fix", "")}
Severity: {diagnosis.get("severity", "")}
Confidence: {diagnosis.get("confidence", "")}

Resolution Outcome:
This incident was analyzed by MemoryOps AI and should be used as historical operational knowledge for future incidents.
"""

    return client.retain(
        bank_id=BANK_ID,
        content=content,
        context="production incident response"
    )


def recall_incidents(incident):
    query = f"""
Find previous production incidents similar to this incident.

Service: {incident.service}
Error: {incident.error}
Logs: {incident.logs}
Description: {incident.description}

Focus on:
- similar services
- similar errors
- similar log patterns
- previous root causes
- successful fixes
"""

    result = client.recall(
        bank_id=BANK_ID,
        query=query
    )

    memories = []

    for item in result.results:
        memories.append({
            "text": item.text,
            "type": item.type,
            "context": item.context
        })

    return memories