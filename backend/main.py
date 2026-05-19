from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, scores

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tetris API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8765", "https://hyunhong93.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(scores.router)
