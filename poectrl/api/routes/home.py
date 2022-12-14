"""Define the Root Route."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    """Process the root route of the API."""
    return {"info": "API Functional."}
