import uvicorn
import sys
import os

# Add src to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    reload = os.environ.get("ENV") != "production"
    uvicorn.run("app.api.endpoints:app", host="0.0.0.0", port=port, reload=reload)

