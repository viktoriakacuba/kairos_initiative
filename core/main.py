from fastapi import FastAPI, Request, Response, HTTPException, Cookie
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4

from core.memory import init_db, save_interaction
from core.agent import generate_response
from reasoning_flow.loop import run_reasoning_loop
from pydantic import BaseModel
from core.profile import UserProfile

app = FastAPI()

class ThoughtRequest(BaseModel):
    input: str
    user_id: str

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
    user_id = data.get("user_id")
    if not message:
        raise HTTPException(status_code=400, detail="Missing 'message' field in JSON body")
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing 'user_id' field in JSON body")

    try:
        response = generate_response(message, user_id)
        save_interaction(user_id, message, response)
        return {"kairos": response}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/kairos/reason")
def reason_through_input(request: ThoughtRequest, response: Response, user_id: str = Cookie(default=None)):
    if not user_id:
        user_id = str(uuid4())
        response.set_cookie(key="user_id", value=user_id, httponly=True)
        
    result = run_reasoning_loop(request.input, user_id)
    save_interaction(user_id, request.input, result["reflection"])
    return result

@app.get("/profile", response_model=UserProfile)
def read_profile(user_id: str = Cookie(...)):
    return get_user_by_id(user_id)