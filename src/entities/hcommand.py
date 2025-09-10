from typing import Optional
from pydantic import BaseModel, PydanticUserError

try:
    class HCommand(BaseModel):
        idcliente: int 
        idusuario: int 
        idservidor: int 
        idoperacion: int 
        idcola_comando: str 
        fecha: str 
        accion:str 
        comando: str 
        resultado: str 

    model_config = {"from_attributes": True}
except PydanticUserError as exc_info:
    assert exc_info.code == 'schema-for-unknown-type'