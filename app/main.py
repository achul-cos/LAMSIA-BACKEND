from fastapi import FastAPI

# Import User route /users
from app.routes.user_routes import router as user_router

app = FastAPI()

# Mendaftarkan route /users ke aplikasi FastAPI
app.include_router(user_router)

@app.get("/")
async def root():
    return {
        "message": "LAMSIA Backend is online."
    }
