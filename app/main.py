from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.mqtt.mqtt_handler import init_mqtt, get_mqtt_handler

# Import User route /users
from app.routes.user_routes import router as user_router
from app.routes.pengasuh_route import router as pengasuh_router
from app.routes.sensorresult_route import router as sensorresult_router

# Lifecycle event
# Menjelaskan lifecycle dari aplikasi, dari mulai ON hingga SHUTDOWN
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start (On)
    print("Starting MQTT Connection...")
    init_mqtt()
    yield

    # Shutdown
    print("Disconnecting or stop MQTT Connection...")
    handler = get_mqtt_handler()

    if handler:
        handler.disconnect()

app = FastAPI(lifespan=lifespan)

# Mendaftarkan route /users ke aplikasi FastAPI
app.include_router(user_router)
app.include_router(pengasuh_router)
app.include_router(sensorresult_router)

@app.get("/")
async def root():
    return {
        "message": "LAMSIA Backend is online."
    }

# ============== Route MQTT Sementara ============== #

@app.post("/mqtt/command/buzzer/on")
async def buzzer_on():
    handler = get_mqtt_handler()
    handler.handle_command_buzzer(command=True)
    return ({
        "type": "command",
        "component": "buzzer",
        "component_id": "",
        "command_type": "bool",
        "command_value": "True"
    }) 

@app.post("/mqtt/command/buzzer/off")
async def buzzer_off():
    handler = get_mqtt_handler()
    handler.handle_command_buzzer(command=False)
    return ({
        "type": "command",
        "component": "buzzer",
        "component_id": "",
        "command_type": "bool",
        "command_value": "False"
    }) 

