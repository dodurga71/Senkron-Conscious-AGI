from fastapi import FastAPI

app = FastAPI(title="SENKRON API", version="0.1.0")

@app.get("/healthz")
def healthz():
    return {"ok": True, "service": "senkron", "version": "0.1.0"}
