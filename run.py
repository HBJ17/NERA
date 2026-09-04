"""
NERA (North Eastern Resilience & Autonomous Logistics Engine)
Direct Python Production Entrypoint for Railway / Docker / Local
"""
import os
import uvicorn
from app.config import settings

if __name__ == "__main__":
    # Dynamically resolve PORT from Railway environment variable
    raw_port = os.environ.get("PORT", str(settings.PORT))
    try:
        port = int(raw_port)
    except (ValueError, TypeError):
        port = 8000

    host = os.environ.get("HOST", "0.0.0.0")
    debug = os.environ.get("DEBUG", "False").lower() in ("true", "1")

    print(f"[NERA] Booting service on {host}:{port} (debug={debug})...")
    uvicorn.run("app.main:app", host=host, port=port, reload=debug)
