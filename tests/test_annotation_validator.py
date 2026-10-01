from app.core.annotation_validator import validate_object


def test_valid_object():
    obj = {
        "class": "car",
        "bbox": [100, 200, 500, 600],
    }

    result = validate_object(obj, 1920, 1080)

    assert result["status"] == "PASS"
    assert result["error_type"] is None


def test_missing_object_field():
    obj = {
        "class": "car",
    }

    result = validate_object(obj, 1920, 1080)

    assert result["status"] == "ERROR"
    assert result["error_type"] == "MISSING_OBJECT_FIELD"
    assert result["details"] == ["bbox"]


def test_invalid_class():
    obj = {
        "class": "",
        "bbox": [100, 200, 500, 600],
    }

    result = validate_object(obj, 1920, 1080)

    assert result["status"] == "ERROR"
    assert result["error_type"] == "INVALID_CLASS"


def test_invalid_bbox_format():
    obj = {
        "class": "car",
        "bbox": [100, 200, 500],
    }

    result = validate_object(obj, 1920, 1080)

    assert result["status"] == "ERROR"
    assert result["error_type"] == "INVALID_BBOX_FORMAT"


def test_invalid_bbox_value():
    obj = {
        "class": "car",
        "bbox": ["100", 200, 500, 600],
    }

    result = validate_object(obj, 1920, 1080)

    assert result["status"] == "ERROR"
    assert result["error_type"] == "INVALID_BBOX_VALUE"


def test_invalid_bbox_order():
    obj = {
        "class": "car",
        "bbox": [500, 200, 100, 600],
    }

    result = validate_object(obj, 1920, 1080)

    assert result["status"] == "ERROR"
    assert result["error_type"] == "INVALID_BBOX_ORDER"


def test_bbox_out_of_bounds():
    obj = {
        "class": "car",
        "bbox": [100, 200, 2000, 600],
    }

    result = validate_object(obj, 1920, 1080)

    assert result["status"] == "ERROR"
    assert result["error_type"] == "BBOX_OUT_OF_BOUNDS"