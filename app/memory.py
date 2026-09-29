import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_API_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "memoryops-ai")


async def setup_bank():
    return await client.acreate_bank(
        bank_id=BANK_ID,
        name="MemoryOps AI",
        reflect_mission="You are an expert production incident response memory system. Prioritize previous incidents, root causes, successful fixes, and operational outcomes.",
        background="Memory bank for production incidents, service failures, debugging patterns, root causes and resolutions."
    )


async def recall_incidents(incident):
    query = f"""
Production incident requiring diagnosis.

Service: {incident.service}
Error: {incident.error}
Logs: {incident.logs}
Description: {incident.description}

Find previous incidents with similar:
- service failures
- errors
- log patterns
- root causes
- successful resolutions
- operational outcomes
"""

    result = await client.arecall(
        bank_id=BANK_ID,
        query=query,
        max_tokens=3000,
        budget="mid"
    )

    memories = []

    for item in result.results:
        memories.append({
            "text": item.text,
            "type": item.type,
            "context": item.context
        })

    return memories


async def store_incident(incident, diagnosis):
    content = f"""
PRODUCTION INCIDENT

Service:
{incident.service}

Error:
{incident.error}

Logs:
{incident.logs}

Description:
{incident.description}

AI ANALYSIS

Summary:
{diagnosis.get("summary", "")}

Root Cause:
{diagnosis.get("root_cause", "")}

Recommended Fix:
{diagnosis.get("recommended_fix", "")}

Severity:
{diagnosis.get("severity", "")}

Confidence:
{diagnosis.get("confidence", "")}%

Learning:
{diagnosis.get("learning", "")}

This incident has been analyzed and should become operational knowledge for future incident response.
"""

    return await client.aretain(
        bank_id=BANK_ID,
        content=content,
        context="MemoryOps AI production incident learning"
    )
