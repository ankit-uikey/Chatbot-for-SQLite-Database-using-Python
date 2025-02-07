from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.chatbot import process_query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

print("DB_HOST:", os.getenv("DB_HOST"))  
print("DB_NAME:", os.getenv("DB_NAME"))  
print("DB_USER:", os.getenv("DB_USER"))  # Remove after testing

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#print("Current Working Directory:", os.getcwd())  
#print("Database Exists:", os.path.exists("backend/company.db")) # Check if the database exists

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
