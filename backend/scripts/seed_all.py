"""
Master seed script to populate the database with all test data.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database.setup import SessionLocal
from scripts.seed_templates import seed_templates
from scripts.seed_job_offerings import seed_job_offerings


def seed_all():
    """Run all seed scripts."""
    print("=" * 60)
    print("🌱 Starting database seeding...")
    print("=" * 60)

    print("\n1️⃣  Seeding templates...")
    print("-" * 60)
    db = SessionLocal()
    try:
        seed_templates(db)
        print("Templates seeded successfully!")
    except Exception as e:
        print(f"❌ Error seeding templates: {e}")
    finally:
        db.close()

    print("\n2️⃣  Seeding job offerings...")
    print("-" * 60)
    try:
        seed_job_offerings()
    except Exception as e:
        print(f"❌ Error seeding job offerings: {e}")

    print("\n" + "=" * 60)
    print("✨ Database seeding complete!")
    print("=" * 60)


if __name__ == "__main__":
    seed_all()

