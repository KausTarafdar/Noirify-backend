from typing import Union

from fastapi import FastAPI

from .api import auth, data_processor

app = FastAPI()


@app.get("/health")
async def health():
    return {
        "Response":"200",
        "Status": "OK",
    }

app.include_router(auth.router)
app.include_router(data_processor.router)
