from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str
    name: Optional[str] = None
    function_call: Optional[str] = None
