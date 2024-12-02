from fastapi import FastAPI
from app.routers import crypto, weathers
from decouple import config

app=FastAPI()
app.include_router(crypto.router, prefix="/crypto", tags=["crypto"])
app.include_router(weathers.router, prefix="/weathers", tags=["weathers"])

@app.get("/")
async def root():
    responses = config("TEST_ROOT_APP")
    return {"message": responses}
