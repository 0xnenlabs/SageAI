from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str
    name: str
    function_call: str
