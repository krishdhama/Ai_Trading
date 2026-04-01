"""FastAPI entry point for the trading psychology trainer backend."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.mongo import connect_to_mongo, disconnect_mongo
from routes.ai import router as ai_router
from routes.behavior import router as behavior_router
from routes.scenario import router as scenario_router
from routes.trade import router as trade_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize and tear down shared resources."""
    connect_to_mongo()
    yield
    disconnect_mongo()


app = FastAPI(
    title="AI-Powered Trading Psychology Trainer API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scenario_router, prefix="/scenario", tags=["scenario"])
app.include_router(trade_router, tags=["trade"])
app.include_router(behavior_router, tags=["behavior"])
app.include_router(ai_router, tags=["ai"])


@app.get("/")
def read_root():
    """Simple health endpoint for quick backend verification."""
    return {"message": "Trading Psychology Trainer API is running"}
