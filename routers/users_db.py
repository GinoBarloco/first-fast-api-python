from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import users_collection
from bson import ObjectId

router = APIRouter(prefix="/usersdb",
                   tags=["usersdb"],  # sirve para agrupar la documentacion
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

users_list = []

##################
##### UTILS ######
##################


def search_user(field: str, key):
    try:
        _user = users_collection.find_one({field: key})
        return User(**user_schema(_user))

    except:
        return {"error": "El usuario no existe"}

###########################
##### GET OPERATIONS ######
###########################


@router.get("/", response_model=list[User])
async def users():
    return users_schema(users_collection.find())


# Path
@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))


# Query: parametros no necesarios para hacer una petición
@router.get("/")
async def user(id: str):
    return search_user("_id", ObjectId(id))

###########################
##### POST OPERATIONS #####
###########################


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)  # HTTP_201_CREATED -> se creó un registro en la DB.
async def user(_user: User):
    if type(search_user("email", _user.email)) == User:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="El usuario ya existe")  # 204: No Content

    user_dict = dict(_user)
    del user_dict["id"]  # lo elimino para que el id lo inserte MongoDB

    inserted_id = users_collection.insert_one(user_dict).inserted_id  # MongoClient.DB.Collections.operations()

    new_user = user_schema(users_collection.find_one({"_id": inserted_id}))  # _id lo crea MongoDB, usamos user_schema para devolver lo que queremos.

    return User(**new_user)

###########################
##### PUT OPERATIONS ######
###########################


@router.put("/", response_model=User)
async def user(user: User):
    user_dict = dict(user)
    del user_dict["id"]

    try:
        users_collection.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)

    except:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="El usuario no se ha actualizado.")

    return search_user("_id", ObjectId(user.id))

###########################
#### DELETE OPERATIONS ####
###########################


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    found = users_collection.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="El usuario no se ha eliminado.")
    else:
        return {"message": "El usuario fue eliminado correctamente."}
