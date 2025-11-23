"""
Script to seed job offerings in the database.
"""
import json
import os
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from app.database.setup import SessionLocal
from app.database.models import JobOffering


def seed_job_offerings():
    """Seed job offerings with data from job_offerings_final.json."""
    db = SessionLocal()
    
    # Path to the JSON file
    json_path = os.path.join(os.path.dirname(__file__), 'job_offerings_final.json')
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            job_data_list = json.load(f)
            
        print(f"Found {len(job_data_list)} job offerings in JSON file.")
        
        batch_size = 50
        processed_count = 0
        added_count = 0
        skipped_count = 0
        
        for i in range(0, len(job_data_list), batch_size):
            batch = job_data_list[i:i + batch_size]
            
            for job_data in batch:
                uid = job_data.get("uid")
                if not uid:
                    print("⚠️  Skipping job with no UID")
                    continue
                
                # Create a unique ID based on UID
                job_id = f"job-{uid}"
                
                # Check if already exists
                existing = db.query(JobOffering).filter(JobOffering.id == job_id).first()
                if existing:
                    # Optional: Update existing record? For now, just skip as per original script logic
                    # print(f"⚠️  Job offering '{job_id}' already exists, skipping...")
                    skipped_count += 1
                    continue
                
                # Parse dates
                post_date_str = job_data.get("post_date")
                post_date = None
                if post_date_str:
                    try:
                        # Handle ISO format with Z
                        post_date = datetime.fromisoformat(post_date_str.replace('Z', '+00:00'))
                    except ValueError:
                        print(f"⚠️  Could not parse date: {post_date_str}")
                
                # Create JobOffering object
                job_offering = JobOffering(
                    id=job_id,
                    keyword=job_data.get("keyword", "unknown"),
                    company_name=job_data.get("company_name"),
                    role_name=job_data.get("role_name"),
                    description=job_data.get("description"),
                    url=job_data.get("url"),
                    location=job_data.get("location"),
                    work_mode=job_data.get("work_mode"),
                    type=job_data.get("type"),
                    salary=job_data.get("salary"),
                    sectors=job_data.get("sectors"),
                    post_date=post_date,
                    last_updated=datetime.utcnow(), # Default to now if not available
                    uid=uid,
                    api_url=job_data.get("api_url"),
                    extra_data=job_data.get("extra_data")
                )
                
                db.add(job_offering)
                added_count += 1
            
            # Commit the batch
            try:
                db.commit()
                print(f"✅ Committed batch {i // batch_size + 1} ({len(batch)} records processed)")
            except IntegrityError as e:
                db.rollback()
                print(f"❌ Error committing batch: {e}")
            
            processed_count += len(batch)
            
        print(f"\n🎉 Finished seeding!")
        print(f"   - Added: {added_count}")
        print(f"   - Skipped: {skipped_count}")
        print(f"   - Total processed: {processed_count}")
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find file {json_path}")
    except json.JSONDecodeError:
        print(f"❌ Error: Could not decode JSON from {json_path}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Seeding job offerings...")
    seed_job_offerings()

