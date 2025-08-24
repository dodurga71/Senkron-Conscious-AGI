from fastapi import FastAPI
from onur_module.router import router as onur_router

app = FastAPI(title="SENKRON API", version="0.1.0")

@app.get("/healthz")
def healthz():
    return {"ok": True, "service": "senkron", "version": "0.1.0"}

app.include_router(onur_router)
