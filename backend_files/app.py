import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)
MODEL_PATH = os.path.join(os.getcwd(), "backend_files", "superkart_model.joblib")
model = joblib.load(MODEL_PATH)

FEATURE_COLUMNS = [
    "Product_Weight",
    "Product_Sugar_Content",
    "Product_Allocated_Area",
    "Product_MRP",
    "Store_Size",
    "Store_Location_City_Type",
    "Store_Type",
    "Product_Id_char",
    "Store_Age_Years",
    "Product_Type_Category",
]

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/v1/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    record = pd.DataFrame([data])[FEATURE_COLUMNS]
    prediction = model.predict(record)[0]
    return jsonify({"prediction": float(prediction)})

@app.route("/v1/predictbatch", methods=["POST"])
def predict_batch():
    uploaded = request.files.get("file")
    if uploaded is None:
        return jsonify({"error": "Please upload a CSV file."}), 400

    dataframe = pd.read_csv(uploaded)
    missing = [column for column in FEATURE_COLUMNS if column not in dataframe.columns]
    if missing:
        return jsonify({"error": f"Missing required columns: {missing}"}), 400

    predictions = model.predict(dataframe[FEATURE_COLUMNS])
    return jsonify({str(index): float(value) for index, value in enumerate(predictions)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
