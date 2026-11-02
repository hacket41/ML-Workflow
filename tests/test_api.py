import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session", autouse=True)
def trained_model():
    if not (ROOT / "model.joblib").exists():
        subprocess.run([sys.executable, "train.py"], cwd=ROOT, check=True)


@pytest.fixture()
def client():
    from app.main import app
    return TestClient(app)


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_setosa(client):
    response = client.post("/predict", json={
        "sepal_length": 5.1, "sepal_width": 3.5,
        "petal_length": 1.4, "petal_width": 0.2,
    })
    assert response.status_code == 200
    assert response.json()["label"] == "setosa"


def test_predict_rejects_bad_input(client):
    response = client.post("/predict", json={"sepal_length": -1})
    assert response.status_code == 422
