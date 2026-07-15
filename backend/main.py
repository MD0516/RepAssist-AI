from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.chat import router as chatRouter
from app.api.interactions import (
    router as interactionRouter
)

app = FastAPI(
    title="AI First CRM API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],

    allow_methods=["*"],

    allow_headers=["*"],
)


@app.get("/")
def health():
    return {
        "status": "healthy"
    }

app.include_router(
    chatRouter
)

app.include_router(
    interactionRouter
)
