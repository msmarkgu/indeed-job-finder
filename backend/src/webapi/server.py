import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.webapi.router import api_router

origins = ["*"]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# can keep adding new routers
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        app,
        port=8000,
        host='0.0.0.0'
    )
