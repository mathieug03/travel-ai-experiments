from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.routers import chat, search, itinerary

settings = get_settings()

app = FastAPI(
    title="Travel AI",
    description="Assistant de voyage bas-carbone en Europe",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(search.router)
app.include_router(itinerary.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
