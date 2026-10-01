REQUIRED_OBJECT_FIELDS = {"class", "bbox"}


def validate_object(obj, image_width, image_height):
    if not isinstance(obj, dict):
        return {
            "status": "ERROR",
            "error_type": "INVALID_OBJECT_TYPE",
        }

    missing_fields = REQUIRED_OBJECT_FIELDS - obj.keys()

    if missing_fields:
        return {
            "status": "ERROR",
            "error_type": "MISSING_OBJECT_FIELD",
            "details": sorted(missing_fields),
        }

    if not isinstance(obj["class"], str) or not obj["class"].strip():
        return {
            "status": "ERROR",
            "error_type": "INVALID_CLASS",
        }

    bbox = obj["bbox"]

    if not isinstance(bbox, list) or len(bbox) != 4:
        return {
            "status": "ERROR",
            "error_type": "INVALID_BBOX_FORMAT",
        }

    if not all(isinstance(value, (int, float)) for value in bbox):
        return {
            "status": "ERROR",
            "error_type": "INVALID_BBOX_VALUE",
        }

    x1, y1, x2, y2 = bbox

    if x1 >= x2 or y1 >= y2:
        return {
            "status": "ERROR",
            "error_type": "INVALID_BBOX_ORDER",
        }

    if x1 < 0 or y1 < 0 or x2 > image_width or y2 > image_height:
        return {
            "status": "ERROR",
            "error_type": "BBOX_OUT_OF_BOUNDS",
        }

    return {
        "status": "PASS",
        "error_type": None,
    }


if __name__ == "__main__":
    sample_object = {
        "class": "car",
        "bbox": [100, 200, 500, 600],
    }

    result = validate_object(sample_object, 1920, 1080)
    print(result)