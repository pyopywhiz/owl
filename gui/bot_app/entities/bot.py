from pydantic import BaseModel


class Bot(BaseModel):
    id: str
    token: str
    chat_id: str
