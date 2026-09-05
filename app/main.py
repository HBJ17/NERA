"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
FastAPI Main Application Entrypoint
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.routers import twin, prediction, routing, simulation, fleet, reports, alerts, roles, district_employee

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="NERA: AI-Enabled Logistics Intelligence & Disaster Resilience Platform for the North Eastern Region"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(roles.router, prefix=settings.API_PREFIX)
app.include_router(district_employee.router, prefix=settings.API_PREFIX)
app.include_router(twin.router, prefix=settings.API_PREFIX)
app.include_router(prediction.router, prefix=settings.API_PREFIX)
app.include_router(routing.router, prefix=settings.API_PREFIX)
app.include_router(simulation.router, prefix=settings.API_PREFIX)
app.include_router(fleet.router, prefix=settings.API_PREFIX)
app.include_router(reports.router, prefix=settings.API_PREFIX)
app.include_router(alerts.router, prefix=settings.API_PREFIX)

# Static files directory
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "region": "NER India",
        "version": settings.VERSION
    }

if __name__ == "__main__":
    import uvicorn
    raw_port = os.environ.get("PORT", str(settings.PORT))
    try:
        port = int(raw_port)
    except (ValueError, TypeError):
        port = 8000
    host = os.environ.get("HOST", settings.HOST)
    uvicorn.run("app.main:app", host=host, port=port, reload=settings.DEBUG)
