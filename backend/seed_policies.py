from database import SessionLocal

from app.models.base_models import Policy


def seed_policies():
    db = SessionLocal()

    try:
        existing_policy = (
            db.query(Policy)
            .filter(
                Policy.title
                == "National Land Records Modernization"
            )
            .first()
        )

        if existing_policy:
            print("Policy already exists.")
            return

        policy = Policy(
            title="National Land Records Modernization",
            description=(
                "Pilot policy record for demonstrating "
                "evidence-based land governance analysis."
            ),
            policy_type="Land Governance",
            geography="India",
            status="Active",
            extra_metadata={
                "code": "NLRM-2026",
                "year": 2026,
                "implementationRate": 68,
                "leadMinistry": (
                    "Ministry of Rural Development"
                ),
                "overview": (
                    "A pilot policy framework focused on "
                    "modernizing land records and improving "
                    "land administration through digital "
                    "systems."
                ),
                "keyClauses": [
                    "Digitization of land records",
                    "Improved record accessibility",
                    "Inter-departmental data integration",
                    "Support for transparent land administration"
                ],
                "impact": (
                    "Expected to improve land-record "
                    "accessibility and administrative efficiency."
                )
            }
        )

        db.add(policy)
        db.commit()
        db.refresh(policy)

        print(
            f"Policy created successfully. "
            f"Policy ID: {policy.id}"
        )

    except Exception as error:
        db.rollback()
        print(
            f"Failed to create policy: {error}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    seed_policies()