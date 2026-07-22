from dataclasses import dataclass
from datetime import datetime

@dataclass
class AmbilObatSession:
    aktif: bool = False
    sonar_id: int | None = None
    waktu_pemantauan: datetime | None = None
    isMinumObat: bool = False
    waktu_minumobat: datetime | None = None

ambil_obat_session = AmbilObatSession()