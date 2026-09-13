from database import SessionLocal
from app.models.base_models import GISLayer


def seed_gis_layers():
    db = SessionLocal()

    try:
        existing_count = db.query(GISLayer).count()

        if existing_count > 0:
            print("GIS layers already exist.")
            return

        layers = [
            GISLayer(
                name="Pilot Cadastral Parcel Layer",
                description=(
                    "Pilot cadastral parcel layer used for demonstrating "
                    "land-record and ULPIN-based spatial exploration."
                ),
                layer_type="Cadastral",
                source="National Land Governance Platform - Pilot",
                file_path=None,
                geography="Pilot Regions",
                extra_metadata={
                    "status": "pilot",
                    "format": "GeoJSON",
                    "contains": [
                        "parcel locations",
                        "ULPIN",
                        "survey number",
                        "area",
                        "classification"
                    ]
                }
            ),

            GISLayer(
                name="Pilot Flood Risk Layer",
                description=(
                    "Pilot environmental layer representing flood-risk "
                    "areas for spatial policy analysis."
                ),
                layer_type="Flood Risk",
                source="National Land Governance Platform - Pilot",
                file_path=None,
                geography="Pilot Regions",
                extra_metadata={
                    "status": "pilot",
                    "format": "GeoJSON",
                    "hazard": "flood inundation"
                }
            ),

            GISLayer(
                name="Pilot Forest Cover Layer",
                description=(
                    "Pilot forest and community-resource layer used for "
                    "demonstrating environmental and land-governance analysis."
                ),
                layer_type="Forest Cover",
                source="National Land Governance Platform - Pilot",
                file_path=None,
                geography="Pilot Regions",
                extra_metadata={
                    "status": "pilot",
                    "format": "GeoJSON",
                    "classification": "forest/community resource"
                }
            )
        ]

        db.add_all(layers)
        db.commit()

        for layer in layers:
            db.refresh(layer)

        print("GIS layers created successfully.")

        for layer in layers:
            print(
                f"GIS Layer ID: {layer.id} | "
                f"Name: {layer.name}"
            )

    except Exception as error:
        db.rollback()
        print(f"Failed to seed GIS layers: {error}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_gis_layers()