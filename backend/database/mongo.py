"""MongoDB connection setup with lightweight fail-safe behavior."""

from __future__ import annotations

import os

from pymongo import MongoClient

client: MongoClient | None = None
db = None


def connect_to_mongo() -> None:
    """Attempt MongoDB connection without crashing local hackathon setup."""
    global client, db
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DB", "trading_psychology")

    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=1000)
        client.admin.command("ping")
        db = client[db_name]
    except Exception:
        client = None
        db = None


def get_database():
    """Expose the selected database or `None` when MongoDB is unavailable."""
    return db


def disconnect_mongo() -> None:
    """Close the MongoDB client cleanly on shutdown."""
    global client
    if client is not None:
        client.close()
