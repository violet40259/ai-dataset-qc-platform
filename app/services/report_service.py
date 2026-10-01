import csv
import json
from pathlib import Path


def save_summary(qc_result, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "qc_summary.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            qc_result["summary"],
            file,
            ensure_ascii=False,
            indent=4,
        )

    return output_path


def save_error_report(qc_result, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "qc_errors.csv"
    rows = []

    for file_name in qc_result["missing_annotations"]:
        rows.append({
            "file": file_name,
            "error_type": "MISSING_ANNOTATION",
            "object_index": "",
        })

    for file_name in qc_result["missing_images"]:
        rows.append({
            "file": file_name,
            "error_type": "MISSING_IMAGE",
            "object_index": "",
        })

    for error in qc_result["image_errors"]:
        rows.append({
            "file": error["file"],
            "error_type": error["error_type"],
            "object_index": "",
        })

    for annotation_error in qc_result["annotation_errors"]:
        if "errors" in annotation_error:
            for error in annotation_error["errors"]:
                rows.append({
                    "file": annotation_error["file"],
                    "error_type": error["error_type"],
                    "object_index": error["object_index"],
                })
        else:
            rows.append({
                "file": annotation_error["file"],
                "error_type": annotation_error["error_type"],
                "object_index": "",
            })

    with output_path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "file",
                "error_type",
                "object_index",
            ],
        )

        writer.writeheader()
        writer.writerows(rows)

    return output_path