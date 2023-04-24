from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

router = APIRouter(prefix="/basicauth",
                   tags=["basicauth"],  # sirve para agrupar la documentacion
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")  # URL encargada de autenticar.


class User(BaseModel):  # Estructura de un User genérico
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):  # Herencia de la class User() y agrega la pass.
    password: str


users_db = {
    "hpotter": {
        "username": "hpotter",
        "full_name": "Harry Potter",
        "email": "harry.potter@gmail.com",
        "disabled": False,
        "password": "harry123"
    },
    "rweasley": {
        "username": "rweasley",
        "full_name": "Ron Weasley",
        "email": "ron.weasley@gmail.com",
        "disabled": True,
        "password": "ron123"
    },
    "hgranger": {
        "username": "hgranger",
        "full_name": "Hermione Granger",
        "email": "hermione.granger@gmail.com",
        "disabled": False,
        "password": "hermione123"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)  # token es el username.

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Credenciales de Autenticación inválidas",
                            headers={"WWW-Authenticate": "Bearer"}
                            )

    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo",
                            )

    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):  # el form no tiene dependencia pero hay que indicarlo.
    user = search_user_db(form.username)

    if not user:
        raise HTTPException(status_code=400, detail="El usuario no es correcto.")

    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="La contraseña es incorrecta.")

    token = {"access_token": user.username,
             "token_type": "bearer"}

    return token


@router.get("/users/me")
async def me(user: User = Depends(current_user)):  # Primera operacion para probar la autenticacion OK.
    return user
