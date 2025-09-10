from typing import Optional
from pydantic.v1 import BaseModel, Field

class Data(BaseModel):
    id: int = None
    cmd: str = None

class Request(BaseModel):
    action: str = None
    identificador: Optional[str] = None
    data: list[Data]