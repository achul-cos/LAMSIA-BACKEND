from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.scheduler.history_scheduler import start_scheduler

# Import setiap route yang ada
from app.routes.user_routes import router as user_router
from app.routes.medicine_route import router as medicine_router
from app.routes.pengasuh_route import router as pengasuh_router
from app.routes.schedules_route import router as schedules_router
from app.routes.sensorresult_route import router as sensorresult_router

app = FastAPI()

@app.on_event("startup")
async def startup():
    start_scheduler()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mendaftarkan semua route ke aplikasi FastAPI
app.include_router(user_router)
app.include_router(medicine_router)
app.include_router(schedules_router)
app.include_router(pengasuh_router)
app.include_router(sensorresult_router)

@app.get("/")
async def root():
    return {
        "message": "LAMSIA Backend is online."
    }
