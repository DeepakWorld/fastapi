import os
import time
import threading
import nest_asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pyngrok import ngrok

# --- CONFIGURATION ---
OUTPUT_DIR = "outputs"
NGROK_TOKEN = "3AtndVDWTZpN3Fx88GrzlXQgnY2_2mK9cMGJvxMuzbDLi9To8"
STATIC_DOMAIN = "typhonic-brayan-shogunal.ngrok-free.dev"

# 1. Create directory BEFORE starting the app
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI()

# 2. Broad CORS policy (Essential for Flutter Web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Static Files (This lets you view generated images/videos in browser)
app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")

class PromptRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat_endpoint(request: PromptRequest):
    print(f"💬 Received Chat: {request.prompt}")
    return {
        "status": "success",
        "response": f"AI Response for: {request.prompt}"
    }

@app.post("/image")
async def image_endpoint(request: PromptRequest):
    print(f"🎨 Generating Image: {request.prompt}")
    # Example filename - in real use, this would be your AI generated file
    return {
        "status": "success",
        "url": f"https://{STATIC_DOMAIN}/outputs/sample.png"
    }

def run_server():
    # Use config instead of uvicorn.run for better control in notebooks
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    server.run()

if __name__ == "__main__":
    # Cleanup old ngrok sessions
    os.system("pkill -9 ngrok")
    
    nest_asyncio.apply()
    ngrok.set_auth_token(NGROK_TOKEN)
    
    # Start server in a background thread
    threading.Thread(target=run_server, daemon=True).start()
    time.sleep(2) # Give server a moment to bind to port 8000
    
    try:
        public_url = ngrok.connect(8000, domain=STATIC_DOMAIN)
        print(f"\n🚀 ENGINE LIVE at: {public_url}\n")
    except Exception as e:
        print(f"❌ Ngrok Error: {e}")