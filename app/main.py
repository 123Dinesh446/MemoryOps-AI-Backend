from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

from app.memory import (
    setup_bank,
    recall_incidents,
    store_incident
)

from app.ai import analyze_incident


app = FastAPI(
    title="MemoryOps AI",
    description="AI Incident Response Agent with Hindsight Memory",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class Incident(BaseModel):
    service: str
    error: str
    logs: str
    description: str


@app.on_event("startup")
async def startup():

    try:
        await setup_bank()
        print("Hindsight memory bank ready")

    except Exception as e:
        print("Hindsight setup:", e)


@app.get("/")
async def root():

    return {
        "project": "MemoryOps AI",
        "status": "online",
        "memory": "Hindsight",
        "llm": "Groq",
        "message": "Incident Response Agent is ready"
    }


@app.get("/health")
async def health():

    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/incident/analyze")
async def analyze(incident: Incident):

    try:

        memories = await recall_incidents(incident)

        diagnosis = analyze_incident(
            incident,
            memories
        )

        await store_incident(
            incident,
            diagnosis
        )

        return {
            "success": True,
            "incident": incident,
            "diagnosis": diagnosis,
            "memories_found": len(memories),
            "memories": memories
        }

    except Exception as e:

        print("ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )