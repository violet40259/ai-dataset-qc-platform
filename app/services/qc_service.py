from pathlib import Path

from app.core.scanner import scan_dataset
from app.core.image_validator import validate_image
from app.core.json_validator import validate_json
from app.services.report_service import save_error_report, save_summary


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def run_qc(dataset_path):
    dataset_path = Path(dataset_path)

    image_dir = dataset_path / "images"
    annotation_dir = dataset_path / "annotations"

    scan_result = scan_dataset(dataset_path)

    image_results = []
    annotation_results = []

    for image_path in sorted(image_dir.iterdir()):
        if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        result = validate_image(image_path)

        if result["status"] == "ERROR":
            image_results.append(result)

    for json_path in sorted(annotation_dir.glob("*.json")):
        result = validate_json(json_path)

        if result["status"] == "ERROR":
            annotation_results.append(result)

    annotation_error_count = sum(
        result.get("error_count", 1)
        for result in annotation_results
    )

    total_errors = (
        len(scan_result["missing_annotations"])
        + len(scan_result["missing_images"])
        + len(image_results)
        + annotation_error_count
    )

    return {
        "dataset": str(dataset_path),
        "summary": {
            "image_count": scan_result["image_count"],
            "annotation_count": scan_result["annotation_count"],
            "matched_count": scan_result["matched_count"],
            "missing_annotation_count": len(
                scan_result["missing_annotations"]
            ),
            "missing_image_count": len(
                scan_result["missing_images"]
            ),
            "image_error_count": len(image_results),
            "annotation_error_count": annotation_error_count,
            "total_error_count": total_errors,
        },
        "missing_annotations": scan_result["missing_annotations"],
        "missing_images": scan_result["missing_images"],
        "image_errors": image_results,
        "annotation_errors": annotation_results,
    }


if __name__ == "__main__":
    result = run_qc("sample_data")

    summary_path = save_summary(result, "reports")
    error_report_path = save_error_report(result, "reports")

    summary = result["summary"]

    print("=== Dataset QC Summary ===")
    print(f"Images: {summary['image_count']}")
    print(f"Annotations: {summary['annotation_count']}")
    print(f"Matched: {summary['matched_count']}")
    print(
        "Missing annotations: "
        f"{summary['missing_annotation_count']}"
    )
    print(
        "Missing images: "
        f"{summary['missing_image_count']}"
    )
    print(
        "Image errors: "
        f"{summary['image_error_count']}"
    )
    print(
        "Annotation errors: "
        f"{summary['annotation_error_count']}"
    )
    print(
        "Total errors: "
        f"{summary['total_error_count']}"
    )

    print(f"Summary saved: {summary_path}")
    print(f"Error report saved: {error_report_path}")