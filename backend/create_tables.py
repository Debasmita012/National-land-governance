from database import engine, Base

from app.models.base_models import (
    Role,
    User,
    Dataset,
    Document,
    Policy,
    GISLayer,
    EvidenceCard,
    EvidenceCardDataset,
    EvidenceCardDocument,
    ProvenanceRecord
)


def create_tables():
    print("Creating database tables...")

    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully!")


if __name__ == "__main__":
    create_tables()