from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from app.models.base_models import GISLayer


router = APIRouter(
    prefix="/gis-layers",
    tags=["GIS Layers"]
)


def gis_layer_to_dict(
    layer: GISLayer
) -> Dict[str, Any]:

    return {
        "id": layer.id,
        "name": layer.name,
        "description": layer.description,
        "layer_type": layer.layer_type,
        "source": layer.source,
        "file_path": layer.file_path,
        "geography": layer.geography,
        "extra_metadata": layer.extra_metadata or {},
        "created_at": layer.created_at
    }


@router.get("/")
def get_gis_layers(
    db: Session = Depends(get_db)
):

    layers = (
        db.query(GISLayer)
        .order_by(GISLayer.id)
        .all()
    )

    return [
        gis_layer_to_dict(layer)
        for layer in layers
    ]


@router.get("/{layer_id}")
def get_gis_layer(
    layer_id: int,
    db: Session = Depends(get_db)
):

    layer = (
        db.query(GISLayer)
        .filter(GISLayer.id == layer_id)
        .first()
    )

    if not layer:
        raise HTTPException(
            status_code=404,
            detail="GIS layer not found."
        )

    return gis_layer_to_dict(layer)