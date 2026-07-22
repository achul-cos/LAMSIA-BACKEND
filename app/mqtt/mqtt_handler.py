import paho.mqtt.client as mqtt
import json
from datetime import datetime
import logging
from dotenv import load_dotenv
import os
import json
# from app.models.sensormax_model import Sensormax
# from app.models.sonar_model import Sonar
from app.core.database import SessionLocal

from app.dataclass.ambil_obat_session import ambil_obat_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class MQTTHandler:
    def __init__(self):
        self.broker_host = os.getenv("BROKER_HOST") or "localhost"
        self.broker_port = int(os.getenv("BROKER_PORT", 1883))
        self.client = mqtt.Client()

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc):
        """
        Fungsi yang dijalankan secara otomatis, tepat setelah self.client
        telah terhubung dengan broker. Parameter client, userdata, flags,
        rc merupakan parameter yang diperlukan oleh on_connect berdasasarkan
        dokumentasi paho.mqtt.client
        """

        if rc == 0:
            """
            rc atau return code merupakan indikator hasil usaha connect ke broker
            jika rc sama dengan 0, artinya connect berhasil. Tetapi jika 1,2 atau hingga 5,
            artinya terdapat masalah.
            """
            
            logger.info(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : Mqtt_handler.py [MQTTHandler] <on_connect> : Connected to MQTT Broker.")
            
            # Subscribe ke topik yang dibutuhkan
            client.subscribe("lamsia/command/buzzer")           # Topic untuk mengontrol buzzer
            client.subscribe("lamsia/command/led/+")            # Topic untuk mengontrol led
            client.subscribe("lamsia/monitor/sonar/+")          # Topic untuk menerima data sensor sonar
            client.subscribe("lamsia/monitor/max")              # Topic untuk menerima data sensor max
            client.subscribe("lamsia/monitor/hrtrigger")        # Topic untuk menerima trigger dari sensor MAX bahwa sedang ada tangan yang terdeteksi
            client.subscribe("lamsia/monitor/serial_monitor")   # Topic untuk menerima serial monitor dari ESP32
            client.subscribe("lamsia/monitor/beat")             # Topic untuk menerima status koneksi IoT dengan broker MQTT atau WIFI

        else:
            logger.error(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : Mqtt_handler.py [MQTTHandler] <on_connect> : Connection to broker is failed with return code : {rc}")

    def on_message(self, client, userdata, msg):
        """
        Dijalankan secara otomatis setiap ada pesan baru pada topik yang disubscribe.
        """

        topic = msg.topic                   # Topic atau channel yang memiliki pesan baru
        payload = msg.payload.decode()      # Pesan barunya

        # Untuk melakukan testing subscibe mosquitto pada semua topic
        # C:\Windows\System32>mosquitto_sub -h localhost -t "lamsia/#"

        # Logging
        # logger.info(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : mqtt_handler.py [MQTTHandler] <on_message> : NEW MESSAGE FROM TOPIC => {topic} ; AND NEW MESSAGE => {payload} ")

        # Mapping topic
        if "sonar" in topic:
            self.handle_monitor_sonar(topic, payload)   
        elif "max" in topic:
            self.handle_monitor_max(payload)
        elif "hrtrigger" in topic:
            self.handle_monitor_hrtrigger()
        elif "serial_monitor" in topic:
            self.handle_monitor_serial_monitor(payload)
        elif "beat" in topic:
            self.handle_monitor_beat()

    def on_disconnect(self, cliet, userdata, rc):
        """
        Dijalankan secara otomatis setiap koneksi ke broker MQTT diputus atau terputus
        """

        # Debugging rc
        # Jika rc != 0, maka terjadi masalah berdasarkan indikator rc
        if rc != 0:
            logger.warning(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : Mqtt_handler.py [MQTTHandler] <on_disconnect> : Disconnection with broker is failed with return code : {rc}")

    def handle_monitor_sonar(self, topic, payload):
        """
        Fungsi yang dijalankan untuk menghandle ketikan sensor sonar memberikan data hasil monitoringnya
        """

        try:
            # topic dapat bernilai seperti: 
            # topic = "lamsia/monitor/sonar/1"; atau 
            # topic =  "lamsia/monitor/sonar/2";  atau dengan nama lainya, polanya seperti ini
            # topic = "lamsia/monitor/sonar/{sonar_id}"

            # Maka dengan itu kita mengambil data id dari sensor sonarnya,
            sonar_id = (topic.split("/"))[3]

            # payload merupakan pesan yang masuk pada topic yang disubscribe
            # pesan yang akan dikirimkan memang akan mengirimkan data mentah atau half processed data (data yang diproses minimum sebelumnya).

            # payload sonar pada dasarnya mengirimkan data jarak sensor sonar dengan objek didepan sensor sonar dengan satuan cm
            # sonar_distance = float(payload)

            sonar = json.loads(payload)
            id_sonar = sonar.get("sonar_id", "NULL")
            jarak = sonar.get("jarak", "NULL")
            lebihJauh = sonar.get("lebihJauh", "NULL")
            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Setelahnya data sonar_id dan sonar_distance dapat disimpan sebagai log pada database atau dapat ditampilkan pada log sistem
            # logger.info(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} mqtt_handler.py [MQTTHandler] <handle_monitor_sonar> (SUCCESS) : MONITORING SENSOR SONAR ID: {id_sonar}, JARAK: {jarak} CM, LEBIHJAUH: {lebihJauh}, DATETIME: {dt}")

            # db = SessionLocal()

            # sensorSonar = Sonar(
            #     sonar_id = str(id_sonar),
            #     jarak = str(jarak),
            #     lebihJauh = str(lebihJauh),
            #     created_at = datetime.now()
            # )

            # db.add(sensorSonar)
            # db.commit()

            monitor_ambil_obat(sonar_id=int(id_sonar), jarak=float(jarak))

        except Exception as e:
            # Error handler
            logger.error(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} mqtt_handler.py [MQTTHandler] <handle_monitor_sonar> (ERROR) : ERROR PARSING DATA SENSOR SONAR WITH TOPIC : {topic}, PAYLOAD: {payload}, ERROR MESSAGE: {e}")   

    def handle_monitor_max(self, payload):
        """
        fungsi yang dijalankan untuk menghandle setiap ada pesan baru pada topic sensor MAX
        untuk menerima data IR dan RED
        """

        # Contoh prompt mosquitto publisher untuk topic sensor MAX
        # PS C:\WINDOWS\system32> mosquitto_pub -h localhost -t "lamsia/monitor/max" -m '{\"ir\":123,\"red\":321,\"hr\":44,\"sp\":65}'

        try:
            # Payload merupakan pesan yang dikirimkan pada topic "lamsia/monitor/max"
            # pesan ini berupa data hasil dari sensor MAX-30100 dengan format seperti ini
            # {
            #   "ir": "123123"
            #   "red": "321321",
            #   "hr": "140",
            #   "sp": "97.2"
            # }

            result = json.loads(payload)
            ir = result.get("ir", "NULL")
            red = result.get("red", "null")
            hr = result.get("hr", "null")
            sp = result.get("sp", "null")
            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            logger.info(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} mqtt_hadler.py [MQTTHandler] <handle_monitor_max> SUCCESS : MAX SENSOR GAVE THE DATA AT {dt}, IR: {ir}, RED: {red}, HR: {hr}, SP: {sp}")

            # Todo menyimpa data sensor ini kedalam database

            db = SessionLocal()

            sensor = Sensormax(
                hr=hr,
                sp=sp,
                ir=ir,
                red=red,
                created_at=datetime.now()
            )

            db.add(sensor)
            db.commit()            

        except Exception as e:
            logger.error(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} mqtt_hadler.py [MQTTHandler] <handle_monitor_max> ERROR : ERROR TO HANDLING SENSOR MAX WITH PAYLOAD: {payload}, AND ERROR MESSAGES {e}")
    
    def handle_monitor_hrtrigger(self):
        """
        fungsi yang dijalankan ketika setiap ada trigger pada sensor MAX,
        atau ada tangan yang terdeteksi pada sensor
        """

        try:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            logger.info(f"{dt} mqtt_hadler.py [MQTTHandler] <handle_monitor_hrtrigger> SUCCESS : FINGER DETECTED IN MAX SENSOR AT {dt}")

        except Exception as e:
            logger.error(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} mqtt_hadler.py [MQTTHandler] <handle_monitor_hrtrigger> ERROR : ERROR TO HANDLING FINGER TRIGGER AT MAX SENSOR WITH ERROR MESSAGES {e}")

    def handle_monitor_serial_monitor(self, payload):
        """
        fungsi yang dijalankan setiap ada pesan baru pada topic serial_monitor,
        untuk dapat clone serial monitor pada IoT pada backend,
        """

        try:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            logger.info(f"{dt} mqtt_hadler.py [MQTTHandler] <handle_monitor_serial_monitor> SUCCESS : SERIAL MONITOR AT LAMSIA IOT AT {dt}, SERIAL MONITOR : {payload}")

        except Exception as e:
            logger.error(f"{dt} mqtt_hadler.py [MQTTHandler] <handle_monitor_serial_monitor> ERROR : ERRRO HANDLING SERIAL MONITOR AT LAMSIA IOT WITH PAYLOAD : {payload}")

    def handle_monitor_beat(self):
        """
        fungsi yang dijalankan ketika setiap ada pesan baru pada topic beat,
        sebagai topic yang memberikan informasi apakah lamsia IoT masih menyala, dan terhubung
        dengan wifi dan broker MQTT
        """

        try:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            logger.info(f"{dt} mqtt_hadler.py [MQTTHandler] <handle_monitor_beat> SUCCESS : LAMSIA IOT IS ONLINE UNTIL AT {dt}")

        except Exception as e:
            logger.error(f"{dt} mqtt_hadler.py [MQTTHandler] <handle_monitor_beat> ERROR : ERROR HANDLING TO CHECKING LAMSIA IOT BEAT")

    def connect(self):
        """
        fungsi untuk melakukan koneksi dengan MQTT Broker
        """

        try:
            self.client.connect(self.broker_host, self.broker_port, keepalive=60)
            self.client.loop_start()
            logger.info(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} mqtt_handler.py [MQTTHandler] <connect> SUCCESS : CONNECT TO MQTT BROKER WITH HOST: {self.broker_host}, PORT: {self.broker_port}")
        
        except Exception as e:
            logger.error(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} mqtt_handler.py [MQTTHandler] <connect> ERROR : ERORR TO CONNECT MQTT BROKER WITH HOST: {self.broker_host}, PORT: {self.broker_port}, WITH ERROR MESSAGES: {e}")

    def disconnect(self):
        """
        fungsi yang dijalankan untuk melakukan disconnect dengan MQTT Broker
        """

        self.client.loop_stop()
        self.client.disconnect()

        logger.info(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} mqtt_handler.py [MQTTHandler] <disconnect> SUCCESS : DISCONNECT TO MQTT BROKER")

    def handle_command_buzzer(self, command: bool = True, log: bool = True):
        """
        Fungsi yang digunakan untuk melakukan perintah pada buzzer
        """

        topic = "lamsia/command/buzzer"
        self.client.publish(topic, str(command))

        if log == True:
            logger.info(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} mqtt_handler.py [MQTTHandler] <handle_command_buzzer> SUCCESS : SUCCESS COMMAND BUZZER TO {str(command)}")

    def handle_command_led(self, led_id: int, command: bool = True, log: bool = True):
        """
        Fungsi yang digunakan untuk melakukan perintah pada lampu LED yang dapat secara spesifik
        """

        if led_id and led_id > 0:
            
            topic = f"lamsia/command/led/{led_id}"
            self.client.publish(topic, str(command))

            if bool == True:
                logger.info(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} mqtt_handler.py [MQTTHandler] <handle_command_led> SUCCESS : SUCCESS COMMAND LED WITH LED_ID: {led_id} TO {str(command)}")
        else:
            logger.error(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} mqtt_handler.py [MQTTHandler] <handle_command_led> ERROR : CAN'T COMMAND LED CAUSE LED_ID IS NOT VALID NUMBER (NULL OR UNDER 0)")

    def handle_command_buzzerbeat(self, command: bool = True):
        """
        Fungsi yang digunakan untuk melakukan perintah kepada IoT untuk menjalankan
        buzzer beep
        """

        topic = "lamsia/command/buzzerbeat"
        self.client.publish(topic, str(command))

    def handle_command_lcd(self, lcd_id: int, lcd_text: str):
        """
        Fungsi yang digunakan untuk melakukan perintah kepada komponen LCD
        IoT Untuk menampilkan teks.
        """

        if lcd_id >= 2:
            lcd_id = 2
        elif lcd_id < 2:
            lcd_id = 1

        topic = f"lamsia/command/lcd/{lcd_id}"
        self.client.publish(topic, str(lcd_text))

    def handle_command_lcdidle(self, command: bool = True):
        """
        Fungsi yang digunakan untuk menjalankan perintah kepada komponen LCD
        IOT Untuk menampilkan teks idle
        """

        topic = f"lamsia/command/lcdidle"
        self.client.publish(topic, str(command))

# Global Instance
mqtt_handler = None

def init_mqtt():
    """
    Inisiasi instance atau melakukan koneksi dengan broker mqtt
    """

    global mqtt_handler
    mqtt_handler = MQTTHandler()
    mqtt_handler.connect()

def get_mqtt_handler():
    """
    fungsi getter untuk mengambil instance dari mqtt_handler
    """
    return mqtt_handler

def monitor_ambil_obat(jarak: float, sonar_id: int):

    if not ambil_obat_session.aktif:
        return False
    
    if sonar_id != ambil_obat_session.sonar_id:
        return False
    
    else:
        sekarang = datetime.now()

        if ambil_obat_session.isMinumObat == True and ambil_obat_session.waktu_pemantauan is not None:

            if ambil_obat_session.waktu_pemantauan is not None:
                
                durasiObatDiambil = (sekarang - ambil_obat_session.waktu_pemantauan).total_seconds() - 5

                print(f"Diambilah Obat dan obat tidak didalam kotak selama {durasiObatDiambil} detik")

                if (durasiObatDiambil > 30):

                    get_mqtt_handler().handle_command_buzzerbeat(True)
                    get_mqtt_handler().handle_command_led(sonar_id, True, log= False)
                    get_mqtt_handler().handle_command_lcd(1, "LETAKKAN KEMBALI")
                    get_mqtt_handler().handle_command_lcd(2, f"OBAT KE KOTAK  {sonar_id}")  

            if jarak < 6 :

                if ambil_obat_session.waktu_minumobat is None:

                    ambil_obat_session.waktu_minumobat = sekarang

                    print("Mulai Menghitung Mengembalikan Obat 3 detik!")

                else:

                    durasi = (sekarang - ambil_obat_session.waktu_minumobat).total_seconds()

                    print(f"Obat telah diletak dengan lama {durasi} detik")

                    if durasi >= 3:

                        print("Obat Telah dikembalikan")

                        get_mqtt_handler().handle_command_buzzerbeat(False)
                        get_mqtt_handler().handle_command_led(sonar_id, False, log= False)
                        get_mqtt_handler().handle_command_lcdidle(True)

                        ambil_obat_session.aktif = False
                        ambil_obat_session.isMinumObat = False
                        ambil_obat_session.waktu_pemantauan = None
                        ambil_obat_session.waktu_minumobat = None
                        ambil_obat_session.sonar_id = None

                        # Verifikasi Obat telah dikembalikan                   
            else:             

                ambil_obat_session.waktu_minumobat = None

        elif jarak > 6:

            if ambil_obat_session.waktu_pemantauan is None:

                ambil_obat_session.waktu_pemantauan = sekarang

                print("Mulai menghitung 5 detik")

            else:

                durasi = (sekarang - ambil_obat_session.waktu_pemantauan).total_seconds()

                print(f"Sudah {durasi} obat telah diambil")
                
                if durasi >= 5:

                    print("Obat sudah diambil")

                    get_mqtt_handler().handle_command_buzzerbeat(False)
                    get_mqtt_handler().handle_command_led(sonar_id, False, log= False)
                    get_mqtt_handler().handle_command_lcdidle(True)

                    # Bagian sini bisa ditambahkan ke data base riwayat konsumsi obat

                    # Melakukan reset session,
                    # ambil_obat_session.aktif = False
                    # ambil_obat_session.sonar_id = None
                    # ambil_obat_session.waktu_pemantauan = None

                    # Update sekarang alat akan menu
                    ambil_obat_session.isMinumObat = True

        else:

            ambil_obat_session.waktu_pemantauan = None 