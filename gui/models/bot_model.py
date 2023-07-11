from pydantic import BaseModel


class Bot(BaseModel):
    id: str
    user_token: str
    token: str
    chat_id: str
