from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from core.memory import init_db, save_interaction
from core.agent import generate_response
from reasoning_flow.loop import run_reasoning_loop
from pydantic import BaseModel

app = FastAPI()

class ThoughtRequest(BaseModel):
    input: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

@app.post("/kairos")
async def chat_kairos(request: Request):
    if request.headers.get("content-type") != "application/json":
        raise HTTPException(status_code=400, detail="Content-Type must be application/json")

    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON format")

    message = data.get("message")
    if not message:
        raise HTTPException(status_code=400, detail="Missing 'message' field in JSON body")

    try:
        response = generate_response(message)
        save_interaction(message, response)
        return {"kairos": response}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/kairos/reason")
def reason_through_input(request: ThoughtRequest):
    result = run_reasoning_loop(request.input)
    return result