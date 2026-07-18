import joblib
import pandas as pd

from bp_prediction.database_bp import get_ir_data
from bp_prediction.preprocessing import preprocessing
from bp_prediction.feature_extraction import extract_features

# ======================
# Load Model
# ======================

model_sbp = joblib.load("bp_prediction/models/model_sbp.joblib")
model_dbp = joblib.load("bp_prediction/models/model_dbp.joblib")


# ======================
# Ambil Data Sensor
# ======================

ir = get_ir_data(
    limit=2000
)

print("Jumlah data :", len(ir))


# ======================
# Preprocessing
# ======================

ppg = preprocessing(ir)


# ======================
# Feature Extraction
# ======================

feature = extract_features(ppg)

if feature is None:

    print("Window tidak valid")

    exit()


# ======================
# DataFrame
# ======================

X = pd.DataFrame([feature])


# ======================
# Prediksi
# ======================

sbp = model_sbp.predict(X)[0]

dbp = model_dbp.predict(X)[0]


print()

print("===================")
print("HASIL PREDIKSI")
print("===================")

print("SBP :", round(sbp,2))

print("DBP :", round(dbp,2))
