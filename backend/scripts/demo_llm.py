"""
Script para probar el LLM service manualmente usando requests.
Usa la API directamente como lo haría el frontend.
"""
import requests
from pathlib import Path
from datetime import datetime


BASE_URL = "http://localhost:8000/api/v1"


def test_llm():
    try:
        print("👤 Creando usuario de prueba...")
        user_response = requests.post(
            f"{BASE_URL}/users",
            json={
                "email": f"llm_test_{int(datetime.now().timestamp())}@example.com",
                "full_name": "María González Test",
                "password": "testpass123",
            },
        )
        if user_response.status_code != 201:
            print(f"   ⚠️ Error creando usuario: {user_response.json()}")
            return
        
        user_data = user_response.json()
        user_id = user_data["id"]
        print(f"   Usuario creado: {user_data['full_name']} ({user_data['email']})")
        
        print("\n🎯 Creando proyecto...")
        project_response = requests.post(
            f"{BASE_URL}/projects?user_id={user_id}",
            json={
                "name": "Búsqueda Backend Developer",
                "target_role": "Backend Developer Python",
                "cv_style": "Profesional y técnico",
                "preferences": {
                    "modalidad": "remoto",
                    "ubicacion": "Chile"
                }
            },
        )
        project_data = project_response.json()
        project_id = project_data["id"]
        print(f"   Proyecto creado: {project_data['name']}")
        
        print("\n💼 Creando skills...")
        skills_response = requests.post(
            f"{BASE_URL}/users/{user_id}/skills",
            json={
                "raw_input": "Soy desarrolladora Python con 5 años de experiencia. He trabajado con FastAPI, Django, PostgreSQL. También sé React para el frontend.",
                "skills_data": {
                    "languages": ["Python", "JavaScript"],
                    "frameworks": ["FastAPI", "Django", "React"],
                    "databases": ["PostgreSQL", "MongoDB"],
                    "years_experience": 5
                }
            },
        )
        print(f"   Skills creados")
        
        print("\n📋 Obteniendo templates...")
        templates_response = requests.get(f"{BASE_URL}/templates")
        templates = templates_response.json()
        if not templates:
            print("   ⚠️ No hay templates disponibles. Ejecuta: uv run python -m scripts.seed_templates")
            return
        
        # Buscar específicamente "Simple CV"
        simple_cv = next((t for t in templates if t["name"] == "Simple CV"), None)
        if not simple_cv:
            print("   ⚠️ Template 'Simple CV' no encontrado. Ejecuta: uv run python -m scripts.seed_templates")
            return
        
        template_id = simple_cv["id"]
        print(f"   Template seleccionado: {simple_cv['name']}")
        
        print("\n🤖 Creando CV con LLM...")
        print("   (Esto puede tardar unos segundos...)")
        
        cv_response = requests.post(
            f"{BASE_URL}/projects/{project_id}/cvs",
            json={
                "project_id": project_id,
                "template_id": template_id,
                "extra_instructions": "Enfocado en desarrollo backend y APIs RESTful"
            },
        )
        
        if cv_response.status_code != 201:
            print(f"   ❌ Error creando CV (status {cv_response.status_code})")
            print(f"   Respuesta: {cv_response.text[:500]}")
            return
        
        cv_data = cv_response.json()
        content = cv_data["content"]
        
        print("\n✅ CV generado exitosamente!")
        print(f"\n📋 Contenido generado:")
        print(f"   Nombre: {content['firstname']} {content['lastname']}")
        print(f"   Email: {content['email']}")
        print(f"   Teléfono: {content['phone']}")
        print(f"   Resumen: {content['summary'][:100]}...")
        print(f"   Experiencias: {len(content['experiences'])}")
        print(f"   Educación: {len(content['education'])}")
        print(f"   Habilidades: {len(content['skills'])}")
        
        print("\n📝 Experiencias:")
        for i, exp in enumerate(content['experiences'], 1):
            print(f"   {i}. {exp['title']} en {exp['company']} ({exp['date']})")
        
        print("\n🎓 Educación:")
        for i, edu in enumerate(content['education'], 1):
            print(f"   {i}. {edu['degree']} - {edu['institution']} ({edu['date']})")
        
        print("\n🔧 Habilidades:")
        for skill in content['skills']:
            print(f"   {skill['category']}: {skill['skill_list']}")
        
        print("\n🎨 Guardando template renderizado...")
        rendered_content = cv_data["rendered_content"]
        output_path = Path("templates/llm_test_output.typ")
        output_path.write_text(rendered_content, encoding="utf-8")
        
        print(f"   ✅ Template renderizado guardado en: {output_path}")
        print("\n💡 Puedes compilarlo con:")
        print(f"   typst compile {output_path}")
        
        print(f"\n📊 CV ID: {cv_data['id']}")
        print(f"   Para ver el CV completo: GET {BASE_URL}/cvs/{cv_data['id']}")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: No se pudo conectar al servidor.")
        print("   Asegúrate de que el servidor esté corriendo:")
        print("   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("="*60)
    print("🧪 TEST DEL LLM SERVICE")
    print("="*60)
    test_llm()
    print("\n" + "="*60)
    print("✨ Test completado")
    print("="*60)

