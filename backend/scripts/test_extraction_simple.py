"""
Script simple para testear solo el endpoint de extracción.

Uso:
    uv run python -m scripts.test_extraction_simple
    
    # O con un user_id existente:
    uv run python -m scripts.test_extraction_simple --user-id 1
"""

import requests
import json
import sys
import argparse


BASE_URL = "http://localhost:8000/api/v1"


SAMPLE_TEXTS = {
    "cv_completo": """
Soy un desarrollador full-stack con 5 años de experiencia.

Trabajé 3 años en Google como Software Engineer desarrollando microservicios en Python y Go.
Antes estuve 2 años en una startup usando React y Django.

Habilidades: Python (expert), JavaScript/TypeScript, React, Django, FastAPI, PostgreSQL, AWS.

Certificaciones: AWS Solutions Architect, Certified Kubernetes Administrator.

Hablo español nativo, inglés fluido (C1) y francés básico.

Busco posiciones Senior con salario $120k-$150k USD.
    """,
    
    "linkedin_profile": """
🚀 Senior Full Stack Engineer | Python Expert | Cloud Architecture

Apasionado por crear sistemas escalables y código limpio.

💼 Experience:
• Google (2020-2023): Backend systems, microservices, Python/Go
• Startup XYZ (2018-2020): Full stack development, React + Django

🛠️ Tech Stack: Python • TypeScript • React • PostgreSQL • AWS • Docker

🎓 AWS Certified Solutions Architect
📍 Santiago, Chile | Open to remote
💰 Looking for $100k+ positions
    """,
    
    "texto_corto": """
Desarrollador Python con 3 años de experiencia en Django y FastAPI.
Trabajé en startups y tengo certificación AWS.
Hablo español e inglés.
    """,
    
    "solo_skills": """
Nuevas tecnologías que aprendí:
- GraphQL con Apollo (2 años)
- Testing: Jest, Pytest, coverage al 100%
- CI/CD: GitHub Actions, Jenkins
- Kubernetes y Helm charts
- Speaker en PyCon 2023
    """
}


def print_section(title: str):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_extraction(user_id: int, text_key: str = "cv_completo"):
    """Test extraction endpoint con un texto de ejemplo"""
    
    if text_key not in SAMPLE_TEXTS:
        print(f"❌ Texto '{text_key}' no existe. Opciones: {list(SAMPLE_TEXTS.keys())}")
        return
    
    text = SAMPLE_TEXTS[text_key]
    
    print_section(f"TEST: Extracción con '{text_key}'")
    print(f"User ID: {user_id}")
    print(f"\nTexto a extraer ({len(text)} caracteres):")
    print("-" * 70)
    print(text.strip())
    print("-" * 70)
    
    # Hacer request
    print("\n⏳ Extrayendo información con LLM...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/users/{user_id}/extract-profile",
            json={"text": text},
            timeout=30
        )
        
        print(f"\nStatus: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ ÉXITO!")
            print(f"\nMensaje: {result['message']}")
            print(f"\n📊 Resultados:")
            print(f"   - Perfil creado: {result['profile_created']}")
            print(f"   - Perfil actualizado: {result['profile_updated']}")
            print(f"   - Skills agregados: {result['skills_added']}")
            
            if result['details']:
                print(f"\n📝 Detalles:")
                for detail in result['details']:
                    print(f"   • {detail}")
            
            # Ver el perfil actualizado
            print_section("PERFIL ACTUAL")
            profile_resp = requests.get(f"{BASE_URL}/users/{user_id}/profile")
            if profile_resp.status_code == 200:
                profile = profile_resp.json()
                print(f"Rol: {profile.get('current_role', 'N/A')}")
                print(f"Años de experiencia: {profile.get('years_of_experience', 'N/A')}")
                print(f"Rango salarial: {profile.get('salary_range', 'N/A')}")
                print(f"Idiomas: {', '.join(profile.get('spoken_languages', []) or ['N/A'])}")
            
            # Ver skills agrupados
            print_section("SKILLS AGRUPADOS")
            skills_resp = requests.get(f"{BASE_URL}/users/{user_id}/skills")
            if skills_resp.status_code == 200:
                skills = skills_resp.json()
                
                for skill_type, skill_list in skills.items():
                    if skill_list:
                        print(f"\n📌 {skill_type.upper()} ({len(skill_list)}):")
                        for i, skill in enumerate(skill_list[:3], 1):  # Mostrar solo 3
                            text = skill['skill_text']
                            short_text = text[:80] + "..." if len(text) > 80 else text
                            print(f"   {i}. {short_text}")
                        if len(skill_list) > 3:
                            print(f"   ... y {len(skill_list) - 3} más")
        
        elif response.status_code == 404:
            print(f"\n❌ Usuario {user_id} no encontrado.")
            print("💡 Crea un usuario primero o usa --create-user")
        
        else:
            print(f"\n❌ Error:")
            print(response.text)
    
    except requests.exceptions.ConnectionError:
        print("\n❌ No se puede conectar al servidor.")
        print("   Asegúrate de que esté corriendo: uv run uvicorn app.main:app --reload")
    
    except requests.exceptions.Timeout:
        print("\n❌ Timeout: El LLM tardó demasiado (>30s)")
    
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")


def create_test_user():
    """Crea un usuario de prueba y retorna su ID"""
    from datetime import datetime
    
    print_section("Creando Usuario de Prueba")
    
    user_data = {
        "email": f"test_{datetime.now().timestamp()}@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    }
    
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    
    if response.status_code == 201:
        user = response.json()
        print(f"✅ Usuario creado: {user['full_name']} (ID: {user['id']})")
        return user['id']
    else:
        print(f"❌ Error creando usuario: {response.text}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Test extraction endpoint")
    parser.add_argument("--user-id", type=int, help="ID del usuario (si no existe, usa --create-user)")
    parser.add_argument("--create-user", action="store_true", help="Crear usuario de prueba")
    parser.add_argument("--text", choices=list(SAMPLE_TEXTS.keys()), 
                       default="cv_completo", help="Texto de ejemplo a usar")
    
    args = parser.parse_args()
    
    # Determinar user_id
    user_id = args.user_id
    
    if args.create_user or not user_id:
        user_id = create_test_user()
        if not user_id:
            return
    
    if not user_id:
        print("❌ Debes especificar --user-id o --create-user")
        return
    
    # Ejecutar test
    test_extraction(user_id, args.text)
    
    print_section("OPCIONES PARA MÁS TESTS")
    print(f"\n# Probar otro texto con el mismo usuario:")
    print(f"uv run python -m scripts.test_extraction_simple --user-id {user_id} --text linkedin_profile")
    print(f"\n# Textos disponibles:")
    for key in SAMPLE_TEXTS.keys():
        print(f"  - {key}")


if __name__ == "__main__":
    main()

