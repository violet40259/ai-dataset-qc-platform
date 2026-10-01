from pathlib import Path
from PIL import Image, UnidentifiedImageError

def validate_image(image_path):
    image_path = Path(image_path)

    if not image_path.exists():
        return {
            "file": image_path.name,
            "status": "ERROR",
            "error_type": "FILE_NOT_FOUND",
        }

    if image_path.stat().st_size == 0:
        return {
            "file": image_path.name,
            "status": "ERROR",
            "error_type": "ZERO_BYTE",
        }

    try:
        with Image.open(image_path) as image:
            image.verify()

    except (UnidentifiedImageError, OSError, SyntaxError):
        return {
            "file": image_path.name,
            "status": "ERROR",
            "error_type": "CORRUPTED_IMAGE",
        }

    return {
        "file": image_path.name,
        "status": "PASS",
        "error_type": None,
    }


if __name__ == "__main__":
    result = validate_image("sample_data/images/000001.jpg")
    print(result)