from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import api_router

app = FastAPI(title="Pandit Application")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200","https://mypandit.meandmypandit.com/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
def home():
    return {"message": "API running"}
