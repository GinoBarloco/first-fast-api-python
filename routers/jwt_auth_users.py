from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"  # algoritmo de encriptacion
ACCESS_TOKEN_DURATION = 1  # 1 minuto de validez para el ACCESS_TOKEN.
SECRET = "f0c5c15d38aa0541c8a664ff5eb70c442bebf9d5c848d07962f6478d31932659"  # openssl rand -hex 32

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "hpotter": {
        "username": "hpotter",
        "full_name": "Harry Potter",
        "email": "harry.potter@gmail.com",
        "disabled": False,
        "password": "$2a$12$RqMY5HxXihjUOlPjT8SDWOE.ClaWH8gQXwePi9/r1wPLFlVi7Pv.O"  # harry123 con bcrypt

    },
    "rweasley": {
        "username": "rweasley",
        "full_name": "Ron Weasley",
        "email": "ron.weasley@gmail.com",
        "disabled": True,
        "password": "$2a$12$ABxZE0OTZ7nO8eImduFiwO6yDbkKVygDF5Ad.mM3HQw.L4mGINAh."  # ron123 con bcrypt
    },
    "hgranger": {
        "username": "hgranger",
        "full_name": "Hermione Granger",
        "email": "hermione.granger@gmail.com",
        "disabled": False,
        "password": "$2a$12$Q9X0KTyu2Tws4eAXtTjdd.45I4lknn21l5bx9QOx1NyA8FMo.m0Gq"  # hermione123 con bcrypt
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail="Credenciales de Autenticación inválidas",
                              headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, ALGORITHM).get("sub")

        if username is None:
            raise exception

    except JWTError:
        raise exception

    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo")

    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = search_user_db(form.username)

    if not user:
        raise HTTPException(status_code=400, detail="El usuario no es correcto.")

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="La contraseña es incorrecta.")

    access_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }

    token = {
        "access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM),
        "token_type": "bearer"
    }

    return token


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
