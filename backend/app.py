from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot import process_query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Get absolute path of frontend directory
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))

# Check if the frontend folder exists
if not os.path.exists(frontend_path):
    raise RuntimeError(f"Frontend directory '{frontend_path}' does not exist")

# Mount the frontend folder to serve static files
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Serve index.html when accessing "/"
@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# Define request model
class ChatRequest(BaseModel):
    message: str
    
@app.post("/chat")
def chat(request: ChatRequest):
    response = process_query(request.message)
    return {"response": response}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
