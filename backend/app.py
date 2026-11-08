"""Sestavi FastAPI aplikacijo."""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .settings import FRONTEND_DIR

app = FastAPI(title="AvtoTrg")
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")