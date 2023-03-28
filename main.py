from fastapi import FastAPI, Depends, HTTPException
from bson import ObjectId
import configparser
import secrets
from similarity_helper import find_most_similar_source
from gpt_helper import generate_response
from mongodb_helper import get_users_collection, get_sources_collection, get_chat_collection
from model import User, LoginInput, Source, QueryInput
import authenticator_helper as auth
import datetime

app = FastAPI()

config = configparser.ConfigParser()
config.read("config.ini")
connection_string = config.get("MongoDB", "connection_string")
db_name = config.get("MongoDB", "db_name")


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
    access_token = auth.create_access_token({"user_id": str(existing_user["user_id"])},
                                       expires_delta=datetime.timedelta(minutes=60))
    return {"access_token": access_token, "user_id": existing_user["user_id"], "detail": "Login successful"}


@app.post("/sources")
async def create_or_update_source(
    source: Source,
    current_user=Depends(auth.get_current_user),
    sources_col=Depends(get_sources_collection),
    users_col=Depends(get_users_collection),
):
    user = users_col.find_one({"user_id": current_user['user_id']})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_source = sources_col.find_one({"user_id": current_user['user_id'], "name": source.name})
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
