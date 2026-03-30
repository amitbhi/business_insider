"""
Business Insider System - Main Backend API Entry Point

This file initializes the FastAPI application, mounts routes,
setup logging, and manages the application lifecycle.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import sys

# Add backend directory to path to allow absolute imports within backend
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Module imports enforcing full architecture layout
from api.routes.intelligence_routes import router as intelligence_router
from database.postgres import PostgresManager
from graph.builder import GraphBuilder
from llm.local_llm import LocalLLM

app = FastAPI(
    title="Business Insider - AI Intelligence Engine",
    description="Sovereign multi-agent platform for deep corporate intelligence.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Execute startup routines and bootstrap architectural pillars."""
    app.state.db = PostgresManager("postgresql+asyncpg://user:pass@localhost/db")
    app.state.graph_engine = GraphBuilder(app.state.db)
    app.state.llm = LocalLLM()
    
    # Initialize connection
    # await app.state.db.connect()
    print("🧠 Business Insider Framework initialized strictly.")

# Mount Core Routes
app.include_router(intelligence_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    """Health check endpoint to ensure API is running."""
    return {"status": "healthy", "components": ["AgentManager", "PostgresManager", "GraphBuilder", "LocalLLM"]}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
