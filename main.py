from fastapi import FastAPI
from db import models
from db.database import engine
from router import user,post,comment
from auth import authentication
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(user.router)
app.include_router(post.router)
app.include_router(authentication.router)
app.include_router(comment.router)

@app.get("/")
def root():
    return 'Hello World!'


models.Base.metadata.create_all(engine)

app.mount("/images",StaticFiles(directory="images"),name='images')

import os
origin_url = os.environ.get('INSTACLONE_FASTAPI_CORS_ORIGIN')
origins = [origin_url]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)