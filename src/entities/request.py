from typing import Optional
from pydantic import BaseModel, Field, field_serializer

class Data(BaseModel):
    id: int = None
    cmd: str = None

class Request(BaseModel):
    action: str = None
    identificador: Optional[str] = None
    data: list[Data]