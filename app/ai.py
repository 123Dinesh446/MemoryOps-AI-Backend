import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

groq = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b"
)


def analyze_incident(incident, memories):

    if memories:

        memory_text = "\n\n".join(
            [
                f"""
PREVIOUS INCIDENT {i + 1}

{memory["text"]}

Type:
{memory["type"]}

Context:
{memory["context"]}
"""
                for i, memory in enumerate(memories)
            ]
        )

    else:

        memory_text = "NO PREVIOUS RELEVANT INCIDENTS FOUND."


    prompt = f"""
You are MemoryOps AI.

You are an expert Site Reliability Engineer and production incident-response agent.

Your job is to diagnose a new production incident.

You have access to historical operational memory from Hindsight.

Use historical memory when relevant.

Do not blindly copy previous solutions.

Compare the current evidence with previous incidents.

CURRENT INCIDENT

Service:
{incident.service}

Error:
{incident.error}

Logs:
{incident.logs}

Description:
{incident.description}


HINDSIGHT MEMORY

{memory_text}


Return ONLY valid JSON.

Use exactly this structure:

{{
    "summary": "short explanation of the incident",
    "root_cause": "most likely root cause",
    "recommended_fix": "specific technical resolution",
    "severity": "Critical, High, Medium or Low",
    "confidence": 0,
    "memory_used": true,
    "similar_incidents": 0,
    "learning": "what MemoryOps should remember from this incident"
}}

Rules:

confidence must be a number between 0 and 100.

memory_used must be true only if the historical memories influenced the diagnosis.

similar_incidents must equal the number of useful historical incidents.

Be technically specific.
"""


    response = groq.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a precise production incident-response AI."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        response_format={
            "type": "json_object"
        }
    )


    content = response.choices[0].message.content

    return json.loads(content)