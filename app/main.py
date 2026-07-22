from fastapi import FastAPI
from contextlib import asynccontextmanager
from datetime import datetime
from app.mqtt.mqtt_handler import init_mqtt, get_mqtt_handler
from app.dataclass.ambil_obat_session import ambil_obat_session
from app.helper.routes.register_route import register_route
import app.models
from fastapi.middleware.cors import CORSMiddleware

from app.scheduler.history_scheduler import start_scheduler

# Import setiap route yang ada
from app.routes.dashboard_route import router as dashboard_router
from app.routes.user_routes import router as user_router
from app.routes.medicine_route import router as medicine_router
from app.routes.schedules_route import router as schedules_router
from app.routes.history_route import router as history_router
from app.routes.pengasuh_route import router as pengasuh_router
from app.routes.sensorresult_route import router as sensorresult_router
from app.routes.schedule_view_route import router as schedule_view_router

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
app.include_router(dashboard_router)
app.include_router(user_router)
app.include_router(medicine_router)
app.include_router(schedules_router)
app.include_router(history_router)
app.include_router(pengasuh_router)
app.include_router(sensorresult_router)
app.include_router(schedule_view_router)

register_route(app)

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

@app.post("/mqtt/command/led_1/on")
async def led_1_on():
    handler = get_mqtt_handler()
    handler.handle_command_led(1, True)
    return ({
        "type" : "command",
        "component": "led",
        "commponent_id": "1",
        "command_type": "bool",
        "command_value": "True"
    })

@app.post("/mqtt/command/led_1/off")
async def led_1_off():
    handler = get_mqtt_handler()
    handler.handle_command_led(1, False)
    return ({
        "type" : "command",
        "component": "led", 
        "commponent_id": "1",
        "command_type": "bool",
        "command_value": "False"
    })


@app.post("/mqtt/command/led_2/on")
async def led_2_on():
    handler = get_mqtt_handler()
    handler.handle_command_led(2, True)
    return ({
        "type" : "command",
        "component": "led",
        "commponent_id": "2",
        "command_type": "bool",
        "command_value": "True"
    })

@app.post("/mqtt/command/led_2/off")
async def led_2_off():
    handler = get_mqtt_handler()
    handler.handle_command_led(2, False)
    return ({
        "type" : "command",
        "component": "led", 
        "commponent_id": "2",
        "command_type": "bool",
        "command_value": "False"
    })

@app.post("/mqtt/command/buzzerbeat/on")
async def buzzer_beat_on():
    handler = get_mqtt_handler()
    handler.handle_command_buzzerbeat(True)
    return ({
        "type" : "command",
        "component": "buzzer", 
        "commponent_id": "",
        "command_type": "bool",
        "command_value": "true",
        "command": "beat"  
    })

@app.post("/mqtt/command/buzzerbeat/off")
async def buzzer_beat_off():
    handler = get_mqtt_handler()
    handler.handle_command_buzzerbeat(False)
    return ({
        "type" : "command",
        "component": "buzzer", 
        "commponent_id": "",
        "command_type": "bool",
        "command_value": "false",
        "command": "beat"  
    })

@app.post("/ambil_obat/1")
async def ambil_obat_1():
    handler = get_mqtt_handler()
    handler.handle_command_buzzerbeat(True)
    handler.handle_command_led(1, True)
    handler.handle_command_lcd(1, "   AMBIL OBAT   ")
    handler.handle_command_lcd(2, "   KOTAK -  1   ")

    ambil_obat_session.aktif = True
    ambil_obat_session.sonar_id = 1
    ambil_obat_session.waktu_pemantauan = None

    return({
        "type": "action",
        "name": "ambil_obat",
        "id": "1",
        "message": "Memerintahkan kotak obat untuk mengingatkan lansia untuk minum obat pada kotak 1"
    })

@app.post("/ambilobat/reset")
async def reset_ambil_obat(
    message: bool = False
):

    # Reset Session
    ambil_obat_session.aktif = False
    ambil_obat_session.sonar_id = None
    ambil_obat_session.waktu_pemantauan = None
    ambil_obat_session.waktu_minumobat = None 
    ambil_obat_session.isMinumObat = False

    if message == True:
        return({
            "command": "reset ambil obat session",
            "message": "berhasil"
        })

@app.post("/ambilobat")
async def ambil_obat(
    kotak_id: int
):
    if kotak_id > 2 and kotak_id < 1:
        return({
            "error": True,
            "message": "Sistem hanya memiliki dua kotak obat yaitu 1 dan 2."
        })

    handler = get_mqtt_handler()
    handler.handle_command_buzzerbeat(True)
    handler.handle_command_led(kotak_id, True)
    handler.handle_command_lcd(1, "   AMBIL OBAT   ")
    handler.handle_command_lcd(2, f"   KOTAK -  {kotak_id}   ")

    reset_ambil_obat()

    ambil_obat_session.aktif = True
    ambil_obat_session.sonar_id = kotak_id
    ambil_obat_session.waktu_pemantauan = None
    ambil_obat_session.waktu_minumobat = None

    return({
        "type": "action",
        "name": "ambil_obat",
        "id": kotak_id,
        "message": "Memerintahkan kotak obat untuk mengingatkan lansia untuk minum obat pada kotak 1"
    })

@app.post("/mqtt/command/lcd")
async def text_lcd(
    lcd_id: int,
    lcd_text: str
):
    handler = get_mqtt_handler()
    handler.handle_command_lcd(lcd_id, lcd_text)

    return({
        "type": "command",
        "component": "lcd",
        "commponent_id": str(lcd_id),
        "command_type": "string",
        "command_value": lcd_text,
        "command": "lcd_text"
    })

@app.post("/mqtt/command/lcdidle/on")
async def lcd_idle_on():
    handler = get_mqtt_handler()
    handler.handle_command_lcdidle(True)

    return({
        "type": "command",
        "component": "lcd",
        "component_id": "",
        "command_type": "bool",
        "command_value": "True",
        "command": "lcd_idle"
    })

@app.post("/mqtt/command/lcdidle/off")
async def lcd_idle_off():
    handler = get_mqtt_handler()
    handler.handle_command_lcdidle(False)

    return({
        "type": "command",
        "component": "lcd",
        "component_id": "",
        "command_type": "bool",
        "command_value": "False",
        "command": "lcd_idle"
    })
