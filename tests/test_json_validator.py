import json

from app.core.json_validator import validate_json


def write_json(path, data):
    path.write_text(
        json.dumps(data),
        encoding="utf-8",
    )


def test_valid_json(tmp_path):
    json_path = tmp_path / "valid.json"

    write_json(json_path, {
        "image": "000001.jpg",
        "width": 1920,
        "height": 1080,
        "objects": [
            {
                "class": "car",
                "bbox": [100, 200, 500, 600],
            }
        ],
    })

    result = validate_json(json_path)

    assert result["status"] == "PASS"
    assert result["object_count"] == 1


def test_zero_byte_json(tmp_path):
    json_path = tmp_path / "zero.json"
    json_path.touch()

    result = validate_json(json_path)

    assert result["status"] == "ERROR"
    assert result["error_type"] == "ZERO_BYTE"


def test_invalid_json(tmp_path):
    json_path = tmp_path / "invalid.json"
    json_path.write_text(
        '{"image": "000001.jpg", "width": }',
        encoding="utf-8",
    )

    result = validate_json(json_path)

    assert result["status"] == "ERROR"
    assert result["error_type"] == "INVALID_JSON"


def test_missing_field(tmp_path):
    json_path = tmp_path / "missing.json"

    write_json(json_path, {
        "image": "000001.jpg",
        "width": 1920,
        "objects": [],
    })

    result = validate_json(json_path)

    assert result["status"] == "ERROR"
    assert result["error_type"] == "MISSING_FIELD"
    assert result["details"] == ["height"]


def test_invalid_width(tmp_path):
    json_path = tmp_path / "invalid_width.json"

    write_json(json_path, {
        "image": "000001.jpg",
        "width": "1920",
        "height": 1080,
        "objects": [],
    })

    result = validate_json(json_path)

    assert result["status"] == "ERROR"
    assert result["error_type"] == "INVALID_WIDTH"


def test_multiple_object_errors(tmp_path):
    json_path = tmp_path / "objects.json"

    write_json(json_path, {
        "image": "000001.jpg",
        "width": 1920,
        "height": 1080,
        "objects": [
            {
                "class": "car",
                "bbox": [100, 200, 500, 600],
            },
            {
                "class": "person",
                "bbox": [1700, 200, 2100, 800],
            },
            {
                "class": "",
                "bbox": [100, 200, 500, 600],
            },
            {
                "class": "truck",
                "bbox": [1500, 300, 1200, 900],
            },
        ],
    })

    result = validate_json(json_path)

    assert result["status"] == "ERROR"
    assert result["error_count"] == 3

    assert result["errors"][0]["object_index"] == 1
    assert result["errors"][0]["error_type"] == "BBOX_OUT_OF_BOUNDS"

    assert result["errors"][1]["object_index"] == 2
    assert result["errors"][1]["error_type"] == "INVALID_CLASS"

    assert result["errors"][2]["object_index"] == 3
    assert result["errors"][2]["error_type"] == "INVALID_BBOX_ORDER"