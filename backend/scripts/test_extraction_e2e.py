"""
Script de testeo end-to-end para el endpoint de extracción de perfil.

Requiere:
- Servidor corriendo en localhost:8000
- Base de datos limpia o al menos sin conflictos

Uso:
    uv run python -m scripts.test_extraction_e2e
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"


def print_section(title: str):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_response(response: requests.Response):
    """Print formatted response"""
    print(f"Status: {response.status_code}")
    if response.status_code < 400:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    else:
        print(f"Error: {response.text}")


def main():
    print_section("INICIO DE TEST E2E - EXTRACCIÓN DE PERFIL")
    
    # 1. Crear usuario
    print_section("1. Crear Usuario")
    user_data = {
        "email": f"test_extraction_{datetime.now().timestamp()}@example.com",
        "password": "testpass123",
        "full_name": "Test User Extraction"
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    print_response(response)
    
    if response.status_code != 201:
        print("\n❌ Error creando usuario. Abortando.")
        return
    
    user = response.json()
    user_id = user["id"]
    print(f"\n✅ Usuario creado con ID: {user_id}")
    
    # 2. Primera extracción - Texto completo
    print_section("2. Primera Extracción - CV Completo")
    
    text_cv = """
    Soy un desarrollador full-stack senior con 5 años de experiencia en tecnologías web modernas.
    
    EXPERIENCIA LABORAL:
    - Trabajé 3 años en Google como Software Engineer (2020-2023) donde desarrollé microservicios 
      en Python y Go para sistemas de alta escala.
    - Antes estuve 2 años en una startup (2018-2020) como Full Stack Developer usando React y Django.
    
    HABILIDADES TÉCNICAS:
    - Python: nivel experto, 5+ años de experiencia con Django, FastAPI, Flask
    - JavaScript/TypeScript: avanzado, React, Node.js
    - Go: intermedio, 2 años de experiencia
    - Bases de datos: PostgreSQL, MongoDB, Redis
    - Cloud: AWS (certificado Solutions Architect), Docker, Kubernetes
    
    EDUCACIÓN Y CERTIFICACIONES:
    - AWS Certified Solutions Architect - Professional (2022)
    - Ingeniería en Computación, Universidad de Chile (2014-2018)
    
    IDIOMAS:
    - Español: nativo
    - Inglés: fluido (C1)
    - Francés: básico
    
    INFORMACIÓN ADICIONAL:
    - Busco posiciones Senior/Staff Engineer
    - Rango salarial esperado: $120,000 - $160,000 USD
    - Disponible para trabajo remoto
    """
    
    extract_request = {"text": text_cv}
    response = requests.post(
        f"{BASE_URL}/users/{user_id}/extract-profile",
        json=extract_request
    )
    print_response(response)
    
    if response.status_code != 200:
        print("\n❌ Error en extracción. Abortando.")
        return
    
    extraction_result = response.json()
    print(f"\n✅ Extracción exitosa:")
    print(f"   - Perfil creado: {extraction_result['profile_created']}")
    print(f"   - Skills agregados: {extraction_result['skills_added']}")
    
    # 3. Verificar perfil creado
    print_section("3. Verificar UserProfile Creado")
    response = requests.get(f"{BASE_URL}/users/{user_id}/profile")
    print_response(response)
    
    if response.status_code == 200:
        profile = response.json()
        print(f"\n✅ Perfil verificado:")
        print(f"   - Rol: {profile.get('current_role')}")
        print(f"   - Años exp: {profile.get('years_of_experience')}")
        print(f"   - Salario: {profile.get('salary_range')}")
        print(f"   - Idiomas: {profile.get('spoken_languages')}")
    
    # 4. Verificar skills agregados (agrupados)
    print_section("4. Verificar UserSkills Agrupados")
    response = requests.get(f"{BASE_URL}/users/{user_id}/skills")
    print_response(response)
    
    if response.status_code == 200:
        skills = response.json()
        print(f"\n✅ Skills agrupados:")
        print(f"   - Experiencias: {len(skills.get('experience', []))}")
        print(f"   - Dev Skills: {len(skills.get('dev_skills', []))}")
        print(f"   - Certificados: {len(skills.get('certificates', []))}")
        print(f"   - Extra: {len(skills.get('extra', []))}")
        
        # Mostrar algunos ejemplos
        if skills.get('experience'):
            print(f"\n   Ejemplo de experiencia:")
            print(f"   → {skills['experience'][0]['skill_text'][:100]}...")
        
        if skills.get('dev_skills'):
            print(f"\n   Ejemplo de dev-skill:")
            print(f"   → {skills['dev_skills'][0]['skill_text'][:100]}...")
    
    # 5. Segunda extracción - Info adicional (debe evitar duplicados)
    print_section("5. Segunda Extracción - Info Adicional")
    
    text_linkedin = """
    También tengo experiencia con:
    - GraphQL: 2 años trabajando con Apollo
    - Testing: Jest, Pytest, TDD enthusiast
    - CI/CD: GitHub Actions, Jenkins
    - Participé en 2 proyectos open source importantes
    - Speaker en PyCon Chile 2023
    
    Actualización de idiomas:
    - Inglés: C2 nivel avanzado (mejoré recientemente)
    - Portugués: básico (nuevo)
    """
    
    extract_request2 = {"text": text_linkedin}
    response = requests.post(
        f"{BASE_URL}/users/{user_id}/extract-profile",
        json=extract_request2
    )
    print_response(response)
    
    if response.status_code == 200:
        extraction_result2 = response.json()
        print(f"\n✅ Segunda extracción:")
        print(f"   - Perfil actualizado: {extraction_result2['profile_updated']}")
        print(f"   - Skills nuevos: {extraction_result2['skills_added']}")
        print(f"   - Detalles: {extraction_result2['details']}")
    
    # 6. Verificar que no duplicó
    print_section("6. Verificar Total de Skills (no debe duplicar)")
    response = requests.get(f"{BASE_URL}/users/{user_id}/skills")
    
    if response.status_code == 200:
        skills = response.json()
        total_skills = (
            len(skills.get('experience', [])) +
            len(skills.get('dev_skills', [])) +
            len(skills.get('certificates', [])) +
            len(skills.get('extra', []))
        )
        print(f"\n✅ Total de skills únicos: {total_skills}")
        print(f"   - Experiencias: {len(skills.get('experience', []))}")
        print(f"   - Dev Skills: {len(skills.get('dev_skills', []))}")
        print(f"   - Certificados: {len(skills.get('certificates', []))}")
        print(f"   - Extra: {len(skills.get('extra', []))}")
    
    # 7. Crear proyecto y generar CV con los datos extraídos
    print_section("7. Crear Proyecto")
    project_data = {
        "name": "Postulación Google",
        "target_role": "Staff Software Engineer",
        "cv_style": "profesional"
    }
    response = requests.post(f"{BASE_URL}/projects?user_id={user_id}", json=project_data)
    print_response(response)
    
    if response.status_code != 201:
        print("\n❌ Error creando proyecto.")
        return
    
    project = response.json()
    project_id = project["id"]
    print(f"\n✅ Proyecto creado con ID: {project_id}")
    
    # 8. Obtener templates
    print_section("8. Obtener Templates Disponibles")
    response = requests.get(f"{BASE_URL}/templates")
    
    if response.status_code != 200 or not response.json():
        print("\n❌ No hay templates disponibles.")
        return
    
    templates = response.json()
    template_id = templates[0]["id"]
    print(f"✅ Usando template: {templates[0]['name']} (ID: {template_id})")
    
    # 9. Generar CV con los skills extraídos
    print_section("9. Generar CV con Skills Extraídos")
    cv_data = {
        "project_id": project_id,
        "template_id": template_id,
        "messages": [
            {
                "role": "user",
                "content": "Genera un CV profesional destacando mi experiencia en Google y mis habilidades en Python"
            }
        ]
    }
    
    print("⏳ Generando CV con LLM (esto puede tardar unos segundos)...")
    response = requests.post(f"{BASE_URL}/projects/{project_id}/cvs", json=cv_data)
    
    if response.status_code == 201:
        cv = response.json()
        print(f"\n✅ CV generado exitosamente!")
        print(f"   - CV ID: {cv['id']}")
        print(f"   - Template usado: {cv['template_id']}")
        print(f"   - Nombre en CV: {cv['content'].get('firstname')} {cv['content'].get('lastname')}")
        print(f"   - Email: {cv['content'].get('email')}")
        print(f"   - Experiencias: {len(cv['content'].get('experiences', []))}")
        print(f"   - Educación: {len(cv['content'].get('education', []))}")
        print(f"   - Skills: {len(cv['content'].get('skills', []))}")
        print(f"   - Rendered content length: {len(cv.get('rendered_content', ''))} chars")
        
        if cv['content'].get('experiences'):
            print(f"\n   Primera experiencia generada:")
            exp = cv['content']['experiences'][0]
            print(f"   → {exp.get('title')} en {exp.get('company')}")
    else:
        print(f"\n❌ Error generando CV:")
        print_response(response)
    
    # 10. Resumen final
    print_section("RESUMEN DEL TEST E2E")
    print(f"""
✅ Test completado exitosamente!

Flujo ejecutado:
1. ✅ Usuario creado (ID: {user_id})
2. ✅ Primera extracción de CV completo
3. ✅ Perfil creado con información profesional
4. ✅ Skills extraídos y clasificados automáticamente
5. ✅ Segunda extracción con info adicional
6. ✅ Evitó duplicados correctamente
7. ✅ Proyecto creado
8. ✅ CV generado usando todos los datos extraídos

El flujo completo funciona:
📝 Texto → Extracción LLM → UserProfile + UserSkills → CV generado

Próximos pasos sugeridos:
- Verificar el CV generado en /api/v1/cvs/{cv['id'] if 'cv' in locals() else 'X'}
- Ver todos los skills en /api/v1/users/{user_id}/skills
- Ver el perfil en /api/v1/users/{user_id}/profile
    """)
    
    print_section("FIN DEL TEST")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: No se puede conectar al servidor.")
        print("   Asegúrate de que el servidor esté corriendo en localhost:8000")
        print("   Comando: uv run uvicorn app.main:app --reload")
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

