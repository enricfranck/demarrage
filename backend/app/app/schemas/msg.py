# Shared properties
from typing import Optional
from pydantic import BaseModel


class Msg(BaseModel):
    title: Optional[str] = None

