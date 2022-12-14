"""Main control file for the API."""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """Process the root route of the API."""
    return {"info": "API Functional."}
