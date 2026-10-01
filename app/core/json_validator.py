import json
from pathlib import Path

from app.core.annotation_validator import validate_object


REQUIRED_FIELDS = {"image", "width", "height", "objects"}


def validate_json(json_path):
    json_path = Path(json_path)

    if not json_path.exists():
        return {
            "file": json_path.name,
            "status": "ERROR",
            "error_type": "FILE_NOT_FOUND",
        }

    if json_path.stat().st_size == 0:
        return {
            "file": json_path.name,
            "status": "ERROR",
            "error_type": "ZERO_BYTE",
        }

    try:
        with json_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

    except (json.JSONDecodeError, UnicodeDecodeError):
        return {
            "file": json_path.name,
            "status": "ERROR",
            "error_type": "INVALID_JSON",
        }

    if not isinstance(data, dict):
        return {
            "file": json_path.name,
            "status": "ERROR",
            "error_type": "INVALID_ROOT_TYPE",
        }

    missing_fields = REQUIRED_FIELDS - data.keys()

    if missing_fields:
        return {
            "file": json_path.name,
            "status": "ERROR",
            "error_type": "MISSING_FIELD",
            "details": sorted(missing_fields),
        }

    if not isinstance(data["image"], str) or not data["image"].strip():
        return {
            "file": json_path.name,
            "status": "ERROR",
            "error_type": "INVALID_IMAGE_TYPE",
        }

    if not isinstance(data["width"], int) or data["width"] <= 0:
        return {
            "file": json_path.name,
            "status": "ERROR",
            "error_type": "INVALID_WIDTH",
        }

    if not isinstance(data["height"], int) or data["height"] <= 0:
        return {
            "file": json_path.name,
            "status": "ERROR",
            "error_type": "INVALID_HEIGHT",
        }

    if not isinstance(data["objects"], list):
        return {
            "file": json_path.name,
            "status": "ERROR",
            "error_type": "INVALID_OBJECTS_TYPE",
        }

    errors = []

    for index, obj in enumerate(data["objects"]):
        result = validate_object(
            obj,
            data["width"],
            data["height"],
        )

        if result["status"] == "ERROR":
            errors.append({
                "object_index": index,
                "error_type": result["error_type"],
                "details": result.get("details"),
            })

    if errors:
        return {
            "file": json_path.name,
            "status": "ERROR",
            "error_count": len(errors),
            "errors": errors,
        }

    return {
        "file": json_path.name,
        "status": "PASS",
        "error_type": None,
        "object_count": len(data["objects"]),
    }


if __name__ == "__main__":
    result = validate_json("sample_data/annotations/000001.json")
    print(result)