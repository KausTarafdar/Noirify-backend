from typing import Union
from fastapi import FastAPI

from api.data_processor import router as data_router

app = FastAPI()

@app.get("/health")
async def health():
    return {
        "Response":"200",
        "Status": "OK",
    }

# app.include_router()
app.include_router(router=data_router)
