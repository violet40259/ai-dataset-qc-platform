import json

from fastapi.testclient import TestClient
from PIL import Image

from app.api.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["service"] == "AI Dataset QC Platform"
    assert data["status"] == "running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_qc_dataset_not_found():
    response = client.post(
        "/qc",
        json={
            "dataset_path": "this_dataset_does_not_exist",
        },
    )

    assert response.status_code == 404
    assert "Dataset path not found" in response.json()["detail"]


def test_qc_success(tmp_path):
    dataset_path = tmp_path / "dataset"
    image_dir = dataset_path / "images"
    annotation_dir = dataset_path / "annotations"

    image_dir.mkdir(parents=True)
    annotation_dir.mkdir(parents=True)

    image_path = image_dir / "000001.jpg"

    image = Image.new(
        "RGB",
        (100, 100),
    )
    image.save(image_path)

    annotation = {
        "image": "000001.jpg",
        "width": 100,
        "height": 100,
        "objects": [
            {
                "class": "car",
                "bbox": [10, 10, 50, 50],
            }
        ],
    }

    annotation_path = annotation_dir / "000001.json"

    annotation_path.write_text(
        json.dumps(annotation),
        encoding="utf-8",
    )

    response = client.post(
        "/qc",
        json={
            "dataset_path": str(dataset_path),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "completed"

    summary = data["result"]["summary"]

    assert summary["image_count"] == 1
    assert summary["annotation_count"] == 1
    assert summary["matched_count"] == 1
    assert summary["total_error_count"] == 0