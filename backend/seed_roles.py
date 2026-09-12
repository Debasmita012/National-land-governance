from database import SessionLocal
from app.models.base_models import Role


ROLES = [
    {
        "name": "Admin",
        "description": "Manages users, roles, data, and platform configuration."
    },
    {
        "name": "Researcher",
        "description": "Accesses research documents, datasets, and evidence."
    },
    {
        "name": "Policy Maker",
        "description": "Uses evidence, recommendations, and policy insights for decision-making."
    },
    {
        "name": "Analyst",
        "description": "Analyzes datasets, spatial information, and policy impacts."
    }
]


def seed_roles():
    db = SessionLocal()

    try:
        for role_data in ROLES:
            existing_role = (
                db.query(Role)
                .filter(Role.name == role_data["name"])
                .first()
            )

            if existing_role:
                print(f"Role already exists: {role_data['name']}")
                continue

            role = Role(**role_data)
            db.add(role)
            print(f"Added role: {role_data['name']}")

        db.commit()
        print("\nRoles seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_roles()