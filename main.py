"""
DOCUMENTATION: https://fastapi.tiangolo.com/

1. pip install "fastapi[all]"
2. uvicorn main:app --reload (main is py file; app is FastAPI context)

API Docs: SwaggerUI (local -> http://127.0.0.1/docs

URL Local: http://127.0.0.1:8000
"""
from fastapi import FastAPI
import pprint
from routers import products, users_db, jwt_auth_users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users_db.router)
# app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)

# Static Resources
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return f"Hello FastAPI!"


@app.get("/test")
async def test():
    data = {
        "course_url": "http://www.the-course.com/"
    }

    pretty_data_formatted = pprint.pformat(data)

    return pretty_data_formatted
