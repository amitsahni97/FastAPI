from pydantic import BaseModel, Field
from typing import Optional


class TodoRequestSchema(BaseModel):
    # id: int
    title: str
    description: str
    priority: int
    complete: Optional[bool] = False


class UsersDetailsSchema(BaseModel):
    user_name: str
    first_name: str
    last_name: str
    email: str
    password: str
