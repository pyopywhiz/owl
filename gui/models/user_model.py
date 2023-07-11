from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    id: str
    user_token: str
    telegram_id: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    register_at: datetime = datetime.now()
    expired_at: datetime = datetime.now()
