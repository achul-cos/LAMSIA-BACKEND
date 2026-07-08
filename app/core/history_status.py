from enum import Enum

class HistoryStatus(str, Enum):
  PENDING = "PENDING"
  TAKEN = "TAKEN"
  MISSED = "MISSED"
  LATE = "LATE"
