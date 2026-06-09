from fastapi import FastAPI

# Import User route /users
from app.routes.user_routes import router as user_router
from app.routes.pengasuh_route import router as pengasuh_router
from app.routes.sensorresult_route import router as sensorresult_router

app = FastAPI()

# Mendaftarkan route /users ke aplikasi FastAPI
app.include_router(user_router)
app.include_router(pengasuh_router)
app.include_router(sensorresult_router)

@app.get("/")
async def root():
    return {
        "message": "LAMSIA Backend is online."
    }
