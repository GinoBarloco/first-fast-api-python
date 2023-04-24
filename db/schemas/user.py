import json


def user_schema(user) -> dict:
    schema_dict = {"id": str(user["_id"]),  # user["_id"] es un objeto, no es str porque romperia la clase User()
                   "username": user["username"],
                   "email": user["email"]}

    return schema_dict


def users_schema(users) -> list:
    return [json.dumps(user_schema(user), indent=2) for user in users]
