from fastapi import FastAPI

app = FastAPI(
    title="Trace Markets API",
    description="AI-powered Data Platform for Indian Stock Markets",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "service": "Trace Markets",
        "status": "running",
        "version": "0.1.0"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }