from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: str | Optional[str]  # MongoDB toma los ID como Strings, y lo marco None porque MongoDB lo inserta.
    username: str
    email: str
