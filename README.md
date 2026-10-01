# AI Dataset QC Platform

AI 학습용 이미지 및 annotation 데이터셋의 품질을 자동으로 검사하고 오류 리포트를 생성하는 QC 도구입니다.

반복적인 데이터 검수 작업을 자동화하고, 데이터셋 내 파일 누락부터 이미지 손상, JSON 구조 오류, annotation 좌표 오류까지 하나의 파이프라인에서 확인하는 것을 목표로 개발했습니다.

## Features

### Dataset Scan

- 이미지 및 annotation 파일 탐색
- 이미지-annotation 매칭
- 누락된 이미지 탐지
- 누락된 annotation 탐지

### Image Validation

- 0 byte 이미지 탐지
- 손상되거나 이미지 형식으로 읽을 수 없는 파일 탐지
- JPG, JPEG, PNG 지원

### JSON Validation

- 0 byte JSON 탐지
- JSON syntax 검증
- 필수 필드 검증
- 필드 데이터 타입 검증
- 이미지 width / height 유효성 검증

### Annotation Validation

- object 필수 필드 검증
- class 값 검증
- bbox 형식 및 좌표 타입 검증
- bbox 좌표 순서 검증
- 이미지 영역을 벗어난 bbox 탐지
- 하나의 annotation 파일에서 여러 object 오류 수집

### QC Report

QC 실행 결과를 두 가지 형태로 저장합니다.

- `qc_summary.json`: 전체 데이터셋 QC 요약
- `qc_errors.csv`: 파일 및 object 단위 오류 목록

## Project Structure

```text
ai-dataset-qc-platform/
├── app/
│   ├── core/
│   │   ├── annotation_validator.py
│   │   ├── image_validator.py
│   │   ├── json_validator.py
│   │   └── scanner.py
│   │
│   └── services/
│       ├── qc_service.py
│       └── report_service.py
│
├── sample_data/
│   ├── annotations/
│   └── images/
│
├── tests/
│   ├── test_annotation_validator.py
│   ├── test_image_validator.py
│   └── test_json_validator.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Dataset Format

데이터셋은 다음과 같은 구조를 기준으로 검사합니다.

```text
dataset/
├── images/
│   ├── 000001.jpg
│   ├── 000002.jpg
│   └── ...
│
└── annotations/
    ├── 000001.json
    ├── 000002.json
    └── ...
```

이미지와 annotation은 동일한 파일 stem을 기준으로 매칭합니다.

예:

```text
images/000001.jpg
annotations/000001.json
```

## Annotation Format

현재 annotation은 다음 형식을 기준으로 검증합니다.

```json
{
    "image": "000001.jpg",
    "width": 1920,
    "height": 1080,
    "objects": [
        {
            "class": "car",
            "bbox": [100, 200, 500, 600]
        }
    ]
}
```

`bbox`는 다음 좌표 형식을 사용합니다.

```text
[x1, y1, x2, y2]
```

## Installation

Python 환경에서 필요한 패키지를 설치합니다.

```bash
python -m pip install -r requirements.txt
```

## Run

프로젝트 최상위 경로에서 QC를 실행합니다.

기본 예제 데이터셋을 검사하려면:

```bash
python -m app.services.qc_service
```

검사할 데이터셋 경로를 직접 지정할 수 있습니다.

```bash
python -m app.services.qc_service --dataset "path/to/dataset"
```

결과 저장 위치도 지정할 수 있습니다.

```bash
python -m app.services.qc_service --dataset "path/to/dataset" --output "path/to/reports"
```

Windows에서 경로에 공백이 포함된 경우 경로를 따옴표로 감싸서 입력합니다.

```bash
python -m app.services.qc_service --dataset "C:\Users\user\Desktop\My Dataset"
```

사용 가능한 옵션은 다음 명령어로 확인할 수 있습니다.

```bash
python -m app.services.qc_service --help
```

기본 출력 위치는 `reports`이며 다음 파일이 생성됩니다.

```text
reports/
├── qc_errors.csv
└── qc_summary.json
```
## API

FastAPI 서버를 실행합니다.

```bash
python -m uvicorn app.api.main:app --reload
```

서버 실행 후 Swagger UI에서 API를 직접 테스트할 수 있습니다.

```text
http://127.0.0.1:8000/docs
```

### Health Check

```text
GET /health
```

### Run Dataset QC

```text
POST /qc
```

Request:

```json
{
    "dataset_path": "sample_data"
}
```

Response:

```json
{
    "status": "completed",
    "result": {
        "dataset": "sample_data",
        "summary": {
            "image_count": 5,
            "annotation_count": 5,
            "matched_count": 4,
            "missing_annotation_count": 1,
            "missing_image_count": 1,
            "image_error_count": 2,
            "annotation_error_count": 3,
            "total_error_count": 7
        }
    }
}
```

결과 수치는 입력 데이터셋의 QC 결과에 따라 달라집니다.


## Test

전체 자동 테스트를 실행합니다.

```bash
python -m pytest
```

현재 image, JSON, annotation validation에 대한 테스트를 포함하고 있습니다.

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Pillow
- pytest

## Roadmap

- FastAPI 기반 QC API
- 사용자 지정 dataset 경로 처리
- QC 결과 API 응답
- 대용량 데이터 처리 개선
- LLM API를 활용한 QC 결과 분석 및 오류 요약
- Docker 실행 환경 구성