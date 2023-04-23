from pydantic import BaseModel


class User(BaseModel):
    id: str | None  # MongoDB toma los ID como Strings, y lo marco None porque MongoDB lo inserta.
    username: str
    email: str
