
from pydantic import BaseModel


class SendModel(BaseModel):
    jwt: str
    friend_email: str
    text_data: str

class GetChatModel(BaseModel):
    jwt: str
    friend_email: str
    