import json


def user_schema(user) -> dict:
    schema_dict = {"id": str(user["_id"]),  # user["_id"] es un objeto, no es str porque romperia la clase User()
                   "username": user["username"],
                   "email": user["email"]}

    schema_json = json.loads(schema_dict)

    return schema_json


def users_schema(users) -> list:
    return [user_schema(user) for user in users]
