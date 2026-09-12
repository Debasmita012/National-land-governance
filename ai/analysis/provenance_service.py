import hashlib
import json

from datetime import datetime, timezone

from typing import Dict, Optional

from sqlalchemy.orm import Session

from app.models.base_models import ProvenanceRecord


class ProvenanceService:

    # ============================================================
    # CALCULATE HASH
    # ============================================================

    def _calculate_hash(
        self,
        record: Dict
    ) -> str:

        record_json = json.dumps(
            record,
            sort_keys=True,
            separators=(",", ":")
        )

        return hashlib.sha256(
            record_json.encode("utf-8")
        ).hexdigest()


    # ============================================================
    # CREATE PROVENANCE RECORD
    # ============================================================

    def create_record(
        self,
        db: Session,
        evidence_card_id: int,
        action: str,
        source_documents: list,
        source_datasets: list,
        details: Optional[Dict] = None
    ) -> Dict:

        if evidence_card_id is None:

            raise ValueError(
                "Evidence card ID is required."
            )

        if not action or not action.strip():

            raise ValueError(
                "Action cannot be empty."
            )

        # --------------------------------------------------------
        # Find previous record
        # --------------------------------------------------------

        previous_record = (
            db.query(ProvenanceRecord)
            .order_by(
                ProvenanceRecord.id.desc()
            )
            .first()
        )

        if previous_record:

            previous_hash = (
                previous_record.record_hash
            )

        else:

            previous_hash = "GENESIS"

        # --------------------------------------------------------
        # Timestamp
        # --------------------------------------------------------

        timestamp = datetime.now(
            timezone.utc
        )

        # --------------------------------------------------------
        # Data used for hash calculation
        # --------------------------------------------------------

        record_data = {

            "evidence_card_id":
                evidence_card_id,

            "action":
                action,

            "source_documents":
                source_documents,

            "source_datasets":
                source_datasets,

            "details":
                details or {},

            "timestamp":
                timestamp.isoformat(),

            "previous_hash":
                previous_hash
        }

        # --------------------------------------------------------
        # Calculate record hash
        # --------------------------------------------------------

        record_hash = self._calculate_hash(
            record_data
        )

        # --------------------------------------------------------
        # Create database record
        # --------------------------------------------------------

        provenance_record = ProvenanceRecord(

            evidence_card_id=
                evidence_card_id,

            action=
                action,

            source_documents=
                source_documents,

            source_datasets=
                source_datasets,

            details=
                details or {},

            timestamp=
                timestamp,

            previous_hash=
                previous_hash,

            record_hash=
                record_hash
        )

        db.add(
            provenance_record
        )

        db.commit()

        db.refresh(
            provenance_record
        )

        return {

            "record_id":
                provenance_record.id,

            "evidence_card_id":
                provenance_record.evidence_card_id,

            "action":
                provenance_record.action,

            "source_documents":
                provenance_record.source_documents,

            "source_datasets":
                provenance_record.source_datasets,

            "details":
                provenance_record.details,

            "timestamp":
                provenance_record.timestamp.isoformat(),

            "previous_hash":
                provenance_record.previous_hash,

            "record_hash":
                provenance_record.record_hash
        }


    # ============================================================
    # VERIFY HASH CHAIN
    # ============================================================

    def verify_chain(
        self,
        db: Session
    ) -> Dict:

        records = (
            db.query(ProvenanceRecord)
            .order_by(
                ProvenanceRecord.id.asc()
            )
            .all()
        )

        # --------------------------------------------------------
        # Empty chain
        # --------------------------------------------------------

        if not records:

            return {

                "valid": True,

                "records_checked": 0,

                "errors": []
            }

        errors = []

        # --------------------------------------------------------
        # Verify every record
        # --------------------------------------------------------

        for index, record in enumerate(records):

            # ----------------------------------------------------
            # Expected previous hash
            # ----------------------------------------------------

            if index == 0:

                expected_previous_hash = "GENESIS"

            else:

                expected_previous_hash = (
                    records[index - 1].record_hash
                )

            # ----------------------------------------------------
            # Check previous hash
            # ----------------------------------------------------

            if (
                record.previous_hash
                != expected_previous_hash
            ):

                errors.append(
                    f"Record {record.id} has an "
                    f"invalid previous hash."
                )

            # ----------------------------------------------------
            # Reconstruct original record
            # ----------------------------------------------------

            record_timestamp = (
                record.timestamp
            )

            if (
                record_timestamp.tzinfo
                is None
            ):

                record_timestamp = (
                    record_timestamp.replace(
                        tzinfo=timezone.utc
                    )
                )

            else:

                record_timestamp = (
                    record_timestamp.astimezone(
                        timezone.utc
                    )
                )

            record_data = {

                "evidence_card_id":
                    record.evidence_card_id,

                "action":
                    record.action,

                "source_documents":
                    record.source_documents,

                "source_datasets":
                    record.source_datasets,

                "details":
                    record.details or {},

                "timestamp":
                    record_timestamp.isoformat(),

                "previous_hash":
                    record.previous_hash
            }

            # ----------------------------------------------------
            # Recalculate hash
            # ----------------------------------------------------

            expected_hash = (
                self._calculate_hash(
                    record_data
                )
            )

            # ----------------------------------------------------
            # Compare hash
            # ----------------------------------------------------

            if (
                record.record_hash
                != expected_hash
            ):

                errors.append(
                    f"Record {record.id} "
                    f"has been modified."
                )

        # --------------------------------------------------------
        # Final verification result
        # --------------------------------------------------------

        return {

            "valid":
                len(errors) == 0,

            "records_checked":
                len(records),

            "errors":
                errors
        }


    # ============================================================
    # GET ALL RECORDS
    # ============================================================

    def get_records(
        self,
        db: Session
    ) -> list:

        records = (
            db.query(ProvenanceRecord)
            .order_by(
                ProvenanceRecord.id.asc()
            )
            .all()
        )

        return [

            {

                "record_id":
                    record.id,

                "evidence_card_id":
                    record.evidence_card_id,

                "action":
                    record.action,

                "source_documents":
                    record.source_documents,

                "source_datasets":
                    record.source_datasets,

                "details":
                    record.details,

                "timestamp":
                    record.timestamp.isoformat(),

                "previous_hash":
                    record.previous_hash,

                "record_hash":
                    record.record_hash
            }

            for record in records
        ]