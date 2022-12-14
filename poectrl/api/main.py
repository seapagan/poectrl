"""Main control file for the API."""
from fastapi import FastAPI

from poectrl.api.routes import control, home

app = FastAPI()

app.include_router(home.router)
app.include_router(control.router)
