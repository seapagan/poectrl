"""Main control file for the API."""
from fastapi import FastAPI

from poectrl.api.resources import control, home

app = FastAPI(
    title="Router PoE Control ",
    description="Turn on/off groups of PoE ports on Ubiquiti Switches.",
    version="0.1.0",
    swagger_ui_parameters={"defaultModelsExpandDepth": 0},
)

app.include_router(home.router)
app.include_router(control.router)
