from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from bson import ObjectId
import configparser
import secrets
from similarity_helper import find_most_similar_source
from gpt_helper import generate_response
from mongodb_helper import get_users_collection, get_sources_collection, get_chat_collection

app = FastAPI()

config = configparser.ConfigParser()
config.read("config.ini")
connection_string = config.get("MongoDB", "connection_string")
db_name = config.get("MongoDB", "db_name")


class Source(BaseModel):
    user_id: str
    name: str
    text: str


class LoginInput(BaseModel):
    username: str
    password: str


class QueryInput(BaseModel):
    query: str


class User(BaseModel):
    username: str
    email: str
    password: str
    user_type: str


@app.post("/users")
async def create_user(user: User, users_col=Depends(get_users_collection)):
    existing_user = users_col.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    user_dict = user.dict()
    user_dict["_id"] = str(ObjectId())
    user_dict["user_id"] = secrets.token_hex(16)
    users_col.insert_one(user_dict)
    return {"user_id": user_dict["user_id"], "detail": "User created"}


@app.post("/login")
async def login_user(login_input: LoginInput, users_col=Depends(get_users_collection)):
    existing_user = users_col.find_one({"username": login_input.username, "password": login_input.password})
    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"user_id": existing_user["user_id"], "detail": "Login successful"}


@app.post("/sources")
async def create_or_update_source(source: Source, sources_col=Depends(get_sources_collection),
                                  users_col=Depends(get_users_collection)):
    user = users_col.find_one({"user_id": source.user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_source = sources_col.find_one({"user_id": source.user_id, "name": source.name})
    if existing_source:
        sources_col.update_one({"_id": existing_source["_id"]}, {"$set": {"text": source.text}})
        return {"detail": "Source updated"}

    sources_col.insert_one(source.dict())
    return {"detail": "Source created"}



@app.post("/chat/{user_id}")
async def chat(user_id: str, query_input: QueryInput, sources_col=Depends(get_sources_collection),
               chat_col=Depends(get_chat_collection)):
    query = query_input.query
    sources_list = list(sources_col.find({"user_id": user_id}))
    most_similar_source = find_most_similar_source(query, sources_list)
    response = generate_response(query, most_similar_source["text"])
    chat_col.insert_one({"user_id": user_id, "query": query, "response": response})
    return {"response": response}


# @app.get("/chat/{user_id}")
# async def get_chat(user_id: str, chat_col=Depends(get_chat_collection)):
#     chat_history = list(chat_col.find({"user_id": user_id}))
#     return {"chat_history": chat_history}
