from pydantic import BaseModel

class Comment(BaseModel):
    title: str
    comment: str


