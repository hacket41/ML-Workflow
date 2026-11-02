import logging
import time
from pathlib import Path

import joblib
from fastapi import FastAPI
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("ml-service")

MODEL_PATH = Path(__file__).resolve().parent.parent / "model.joblib"
bundle = joblib.load(MODEL_PATH)
model = bundle["model"]
classes = bundle["classes"]

app = FastAPI(title="Linux ML Demo Service")
started_at = time.time()
request_count = 0


class Flower(BaseModel):
    sepal_length: float = Field(gt=0, description="cm")
    sepal_width: float = Field(gt=0, description="cm")
    petal_length: float = Field(gt=0, description="cm")
    petal_width: float = Field(gt=0, description="cm")


@app.get("/health")
def health():
    return {"status": "ok", "uptime_seconds": round(time.time() - started_at, 1)}


@app.post("/predict")
def predict(flower: Flower):
    global request_count
    request_count += 1
    features = [[
        flower.sepal_length,
        flower.sepal_width,
        flower.petal_length,
        flower.petal_width,
    ]]
    probabilities = model.predict_proba(features)[0]
    index = int(probabilities.argmax())
    log.info("prediction=%s confidence=%.2f", classes[index], probabilities[index])
    return {
        "label": classes[index],
        "confidence": round(float(probabilities[index]), 3),
    }


@app.get("/stats")
def stats():
    return {"requests_served": request_count}
