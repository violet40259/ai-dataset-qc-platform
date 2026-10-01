from pathlib import Path


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def scan_dataset(dataset_path):
    dataset_path = Path(dataset_path)

    image_dir = dataset_path / "images"
    annotation_dir = dataset_path / "annotations"

    if not image_dir.exists():
        raise FileNotFoundError(f"images 폴더가 없습니다: {image_dir}")

    if not annotation_dir.exists():
        raise FileNotFoundError(f"annotations 폴더가 없습니다: {annotation_dir}")

    images = [
        file
        for file in image_dir.iterdir()
        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
    ]

    annotations = [
        file
        for file in annotation_dir.iterdir()
        if file.is_file() and file.suffix.lower() == ".json"
    ]

    image_names = {file.stem for file in images}
    annotation_names = {file.stem for file in annotations}

    matched = image_names & annotation_names
    missing_annotations = image_names - annotation_names
    missing_images = annotation_names - image_names

    return {
        "image_count": len(images),
        "annotation_count": len(annotations),
        "matched_count": len(matched),
        "missing_annotations": sorted(missing_annotations),
        "missing_images": sorted(missing_images),
    }


if __name__ == "__main__":
    result = scan_dataset("sample_data")

    print(f"Images: {result['image_count']}")
    print(f"Annotations: {result['annotation_count']}")
    print(f"Matched: {result['matched_count']}")
    print(f"Missing annotations: {result['missing_annotations']}")
    print(f"Missing images: {result['missing_images']}")