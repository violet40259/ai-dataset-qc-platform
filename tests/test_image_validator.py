from PIL import Image

from app.core.image_validator import validate_image


def test_valid_image(tmp_path):
    image_path = tmp_path / "valid.jpg"

    image = Image.new("RGB", (100, 100))
    image.save(image_path)

    result = validate_image(image_path)

    assert result["status"] == "PASS"
    assert result["error_type"] is None


def test_zero_byte_image(tmp_path):
    image_path = tmp_path / "zero.jpg"
    image_path.touch()

    result = validate_image(image_path)

    assert result["status"] == "ERROR"
    assert result["error_type"] == "ZERO_BYTE"


def test_corrupted_image(tmp_path):
    image_path = tmp_path / "corrupted.jpg"
    image_path.write_text("this is not an image")

    result = validate_image(image_path)

    assert result["status"] == "ERROR"
    assert result["error_type"] == "CORRUPTED_IMAGE"