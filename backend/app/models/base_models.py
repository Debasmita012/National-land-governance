from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        unique=True,
        nullable=False
    )

    description = Column(Text)


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(100),
        unique=True,
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False
    )

    role_id = Column(
        Integer,
        ForeignKey("roles.id"),
        nullable=False
    )


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(255),
        nullable=False
    )

    description = Column(Text)

    source = Column(String(500))

    file_path = Column(String(500))

    data_type = Column(String(100))

    geography = Column(String(255))

    extra_metadata = Column(JSONB)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class Document(Base):
    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(500),
        nullable=False
    )

    source = Column(String(500))

    file_path = Column(String(500))

    document_type = Column(String(100))

    text_content = Column(Text)

    extra_metadata = Column(JSONB)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class Policy(Base):
    __tablename__ = "policies"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(500),
        nullable=False
    )

    description = Column(Text)

    policy_type = Column(String(100))

    geography = Column(String(255))

    status = Column(String(100))

    extra_metadata = Column(JSONB)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class GISLayer(Base):
    __tablename__ = "gis_layers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(255),
        nullable=False
    )

    description = Column(Text)

    layer_type = Column(String(100))

    source = Column(String(500))

    file_path = Column(String(500))

    geography = Column(String(255))

    extra_metadata = Column(JSONB)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class EvidenceCard(Base):
    __tablename__ = "evidence_cards"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(500),
        nullable=False
    )

    recommendation = Column(
        Text,
        nullable=False
    )

    supporting_datasets = Column(JSONB)

    research_papers = Column(JSONB)

    affected_geography = Column(String(255))

    positive_impacts = Column(JSONB)

    negative_impacts = Column(JSONB)

    confidence_score = Column(Float)

    confidence_level = Column(String)
    retrieval_confidence = Column(Float)
    evidence_coverage = Column(Float)
    risks_limitations = Column(JSONB)

    alternatives = Column(JSONB)

    citations = Column(JSONB)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class EvidenceCardDataset(Base):
    __tablename__ = "evidence_card_datasets"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    evidence_card_id = Column(
        Integer,
        ForeignKey("evidence_cards.id"),
        nullable=False
    )

    dataset_id = Column(
        Integer,
        ForeignKey("datasets.id"),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "evidence_card_id",
            "dataset_id",
            name="uq_evidence_card_dataset"
        ),
    )


class EvidenceCardDocument(Base):
    __tablename__ = "evidence_card_documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    evidence_card_id = Column(
        Integer,
        ForeignKey("evidence_cards.id"),
        nullable=False
    )

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False
    )

    chunk_index = Column(
        Integer,
        nullable=True
    )

    __table_args__ = (
        UniqueConstraint(
            "evidence_card_id",
            "document_id",
            "chunk_index",
            name="uq_evidence_card_document_chunk"
        ),
    )
class ProvenanceRecord(Base):
    __tablename__ = "provenance_records"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    evidence_card_id = Column(
        Integer,
        ForeignKey("evidence_cards.id"),
        nullable=False
    )

    action = Column(
        String,
        nullable=False
    )

    source_documents = Column(
        JSONB,
        nullable=False
    )

    source_datasets = Column(
        JSONB,
        nullable=False
    )

    details = Column(
        JSONB,
        nullable=True
    )

    timestamp = Column(
        DateTime,
        nullable=False
    )

    previous_hash = Column(
        String,
        nullable=False
    )

    record_hash = Column(
        String,
        nullable=False,
        unique=True
    )