# from fastapi import FastAPI
# from database.routes import router as UserRouter 

# app = FastAPI()

# app.include_router(UserRouter, tags=["User"], prefix="/user")

# @app.get("/", tags=["Root"])
# async def read_root():
#     return {"message": "Welcome to the FastAPI MongoDB CRUD app!"}
from fastapi import FastAPI
from routes import header_router, footer_router
from routes import header_router, footer_router, home_router
from fastapi.middleware.cors import CORSMiddleware  # 1. Import the middleware
from routes import api_router


main_app = FastAPI(title="Pandit Application")

# 2. Define the origins (frontend URLs) allowed to talk to your backend
origins = [
    "http://localhost:4200",   # Angular development URL
    "http://127.0.0.1:4200",   # Alternative local URL
]

# 3. Add the middleware to your app
main_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # List of allowed origins
    allow_credentials=True,     # Allows cookies and auth headers
    allow_methods=["*"],         # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],         # Allows all headers
)

# Include the main router hub
main_app.include_router(api_router)
main_app.include_router(header_router)
main_app.include_router(footer_router)
main_app.include_router(home_router)

@main_app.get("/")
def home():
    return {"message": "API is running without SQLAlchemy!"}