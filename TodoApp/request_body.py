from pydantic import BaseModel, Field
from typing import Optional


class TodoRequestSchema(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    complete: bool
