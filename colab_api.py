import os
import time
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pyngrok import ngrok
import nest_asyncio
import uvicorn

app = FastAPI()

# 1. Broad CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)
app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")

class PromptRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat_endpoint(request: PromptRequest):
    print(f"💬 Received Chat: {request.prompt}")
    # Replace the logic below with your actual AI model inference
    return {
        "status": "success",
        "response": f"AI Response for: {request.prompt}"
    }

@app.post("/image")
async def image_endpoint(request: PromptRequest):
    print(f"🎨 Generating Image: {request.prompt}")
    # Logic for image generation goes here
    return {
        "status": "success",
        "url": f"https://typhonic-brayan-shogunal.ngrok-free.dev/outputs/sample.png"
    }

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    NGROK_TOKEN = "3AtndVDWTZpN3Fx88GrzlXQgnY2_2mK9cMGJvxMuzbDLi9To8"
    STATIC_DOMAIN = "typhonic-brayan-shogunal.ngrok-free.dev"
    
    # Cleanup and Start
    !pkill -9 ngrok
    nest_asyncio.apply()
    ngrok.set_auth_token(NGROK_TOKEN)
    
    threading.Thread(target=run_server, daemon=True).start()
    time.sleep(2)
    
    try:
        public_url = ngrok.connect(8000, domain=STATIC_DOMAIN)
        print(f"🚀 ENGINE LIVE at {public_url}")
    except Exception as e:
        print(f"Error: {e}")