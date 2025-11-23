"""
Script para borrar todos los usuarios y crear uno nuevo de prueba.
"""
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.setup import SessionLocal
from app.database.models import User


def reset_users():
    """Borra todos los usuarios y crea uno nuevo de prueba."""
    db: Session = SessionLocal()
    
    try:
        # Obtener todos los usuarios
        users = db.query(User).all()
        
        if users:
            print(f"🗑️  Borrando {len(users)} usuario(s)...")
            
            # Borrar todos los usuarios (cascade automático por relationships)
            for user in users:
                print(f"  - Borrando usuario: {user.full_name} ({user.email})")
                db.delete(user)
            
            db.commit()
            print("✅ Todos los usuarios y sus datos relacionados han sido borrados.")
        else:
            print("✅ No hay usuarios para borrar.")
        
        # Reiniciar la secuencia del ID a 1
        print("\n🔄 Reiniciando secuencia de IDs...")
        db.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1;"))
        db.commit()
        
        # Crear nuevo usuario de prueba
        print("👤 Creando nuevo usuario de prueba...")
        new_user = User(
            email="test@example.com",
            hashed_password="hashed_password_placeholder",  # En producción, usar hash real
            full_name="Pablo Skewes"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print(f"✅ Usuario creado:")
        print(f"   - ID: {new_user.id}")
        print(f"   - Nombre: {new_user.full_name}")
        print(f"   - Email: {new_user.email}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    reset_users()

