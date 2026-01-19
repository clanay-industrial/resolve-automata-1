from dotenv  import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

from services.agent import agent_service

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


class Message(BaseModel):
    user: str
    message: str

@app.post("/activity")
async def activity(message: Message):

    response = await agent_service.process_message(message.user, message.message)

    return {"message": response.content, "user": message.user}