from pydantic import BaseModel

class Message(BaseModel):
    user: str
    message: str
    auth_token: str