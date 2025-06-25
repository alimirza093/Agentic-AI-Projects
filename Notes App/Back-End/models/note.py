from pydantic import BaseModel


class Note(BaseModel):
    Note: str
    id : str
    date : str
