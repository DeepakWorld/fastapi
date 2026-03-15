from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TARGET_URL = "https://typhonic-brayan-shogunal.ngrok-free.dev"

@app.post("/chat")
async def proxy_chat(prompt: str = Query(...)):
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            # FIXED: Sending as params to match your Kaggle 'Query(...)' requirement
            response = await client.post(
                f"{TARGET_URL}/chat",
                params={"prompt": prompt}, 
                headers={"ngrok-skip-browser-warning": "true"}
            )
            return response.json()
        except Exception as e:
            return {"status": "error", "response": f"Bridge Link Broken: {str(e)}"}

@app.post("/create-anime") # Renamed to match your CogVideoX endpoint
async def proxy_video(prompt: str = Query(...)):
    async with httpx.AsyncClient(timeout=300.0) as client: # Video takes longer!
        try:
            response = await client.post(
                f"{TARGET_URL}/create-anime",
                params={"prompt": prompt},
                headers={"ngrok-skip-browser-warning": "true"}
            )
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}

@app.get("/")
def health():
    return {"message": "Bridge is active"}