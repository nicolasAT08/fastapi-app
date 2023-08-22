# FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Models, DB connection
from . import models
from .database import engine

# Routers
from .routers import post, user, auth, vote

# models.Base.metadata.create_all(bind=engine)  No needed after implement Alembic

app = FastAPI()

origins = ["*"]             # Specify domains that can access to owr API

app.add_middleware(
    CORSMiddleware,         # Function that runs before every request
    allow_origins=origins,  
    allow_credentials=True, 
    allow_methods=["*"],    # Allow specific HTTP requests
    allow_headers=["*"],    # Allow specific HTTP headers
)


app.include_router(post.router) # Attach the posts and users path operation from each router file
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")                           
def root():                             
    return {"message": "Hello World!!!"}   
 
# Open in browser http://127.0.0.1:8000/docs and you will see Swagger documentation. Or http://127.0.0.1:8000/redoc

# Video time 10:55:00