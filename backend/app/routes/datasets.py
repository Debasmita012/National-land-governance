from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from app.models.base_models import Dataset


router = APIRouter(
    prefix="/datasets",
    tags=["Datasets"]
)


@router.post("/")
def create_dataset(
    name: str,
    description: str | None = None,
    source: str | None = None,
    file_path: str | None = None,
    data_type: str | None = None,
    geography: str | None = None,
    db: Session = Depends(get_db)
):
    dataset = Dataset(
        name=name,
        description=description,
        source=source,
        file_path=file_path,
        data_type=data_type,
        geography=geography
    )

    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    return {
        "message": "Dataset created successfully",
        "dataset": {
            "id": dataset.id,
            "name": dataset.name,
            "description": dataset.description,
            "source": dataset.source,
            "file_path": dataset.file_path,
            "data_type": dataset.data_type,
            "geography": dataset.geography
        }
    }


@router.get("/")
def get_datasets(db: Session = Depends(get_db)):
    datasets = db.query(Dataset).order_by(Dataset.id).all()

    return [
        {
            "id": dataset.id,
            "name": dataset.name,
            "description": dataset.description,
            "source": dataset.source,
            "file_path": dataset.file_path,
            "data_type": dataset.data_type,
            "geography": dataset.geography
        }
        for dataset in datasets
    ]


@router.get("/{dataset_id}")
def get_dataset(
    dataset_id: int,
    db: Session = Depends(get_db)
):
    dataset = (
        db.query(Dataset)
        .filter(Dataset.id == dataset_id)
        .first()
    )

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    return {
        "id": dataset.id,
        "name": dataset.name,
        "description": dataset.description,
        "source": dataset.source,
        "file_path": dataset.file_path,
        "data_type": dataset.data_type,
        "geography": dataset.geography
    }