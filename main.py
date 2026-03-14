import os
from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# Enable CORS for Flutter Web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replace this with your Kaggle ngrok URL
TARGET_URL = "https://typhonic-brayan-shogunal.ngrok-free.dev"

@app.post("/chat")
async def proxy_chat(prompt: str = Query(...)):
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            # We send the request to Kaggle using a JSON body to match the Engine
            response = await client.post(
                f"{TARGET_URL}/chat",
                json={"prompt": prompt}, 
                headers={"ngrok-skip-browser-warning": "true"}
            )
            return response.json()
        except Exception as e:
            return {"status": "error", "response": f"Bridge Link Broken: {str(e)}"}

@app.post("/image")
async def proxy_image(prompt: str = Query(...)):
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(
                f"{TARGET_URL}/image",
                json={"prompt": prompt},
                headers={"ngrok-skip-browser-warning": "true"}
            )
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}

@app.get("/")
def health():
    return {"message": "Bridge is active"}