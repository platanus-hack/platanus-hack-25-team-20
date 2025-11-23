"""
Script to seed job offerings in the database.
"""
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from app.database.setup import SessionLocal
from app.database.models import JobOffering


def seed_job_offerings():
    """Seed job offerings with realistic Chilean tech job data."""
    db = SessionLocal()
    
    job_offerings = [
        JobOffering(
            id="job-1",
            keyword="frontend",
            company_name="Bruno Fritsch",
            role_name="Desarrollador Front-End Junior",
            description="Desarrollador Frontend Junior para nuestra área de Ecommerce & Marketing Digital. Trabajando con React.js y TypeScript.",
            url="https://cl.linkedin.com/jobs/view/desarrollador-front-end-junior-at-bruno-fritsch-4323246353",
            location="Gran Santiago, Región Metropolitana de Santiago, Chile",
            work_mode="Jornada completa",
            type="full-time",
            salary=None,
            sectors="frontend,react,typescript",
            post_date=datetime(2025, 11, 19),
            last_updated=datetime(2025, 11, 19),
            uid="bruno-fritsch-4323246353",
            api_url="https://cl.linkedin.com/jobs/view/desarrollador-front-end-junior-at-bruno-fritsch-4323246353",
            extra_data={
                "requirements": [
                    "Título en Ciencias de la Computación, Ingeniería de Software o campo relacionado",
                    "0 a 2 años de experiencia laboral previa",
                    "Experiencia demostrable en el uso de TypeScript",
                    "Conocimiento de acciones, componentes, suscriptores y fetchers en React",
                    "Conocimiento en herramientas de control de versiones (Git)"
                ],
                "responsibilities": [
                    "Diseñar, desarrollar y mantener componentes de frontend utilizando React.js y TypeScript",
                    "Implementar y gestionar actions y subscriber para el manejo eficiente del estado",
                    "Integrar y consumir endpoints utilizando fetchers",
                    "Diseñar y aplicar principios de Material Design utilizando Material-UI",
                    "Colaborar con diseñadores y desarrolladores backend"
                ]
            }
        ),
        JobOffering(
            id="job-2",
            keyword="python",
            company_name="BairesDev",
            role_name="Desarrollador Python Junior - Trabajo Remoto",
            description="Desarrollador Python Junior para trabajar de forma remota. Oportunidad de trabajar con equipo global en proyectos de vanguardia.",
            url="https://cl.linkedin.com/jobs/view/desarrollador-python-junior-trabajo-remoto-at-bairesdev-4323360135",
            location="Chile",
            work_mode="Remoto",
            type="full-time",
            salary=None,
            sectors="backend,python",
            post_date=datetime(2025, 11, 18),
            last_updated=datetime(2025, 11, 18),
            uid="bairesdev-4323360135",
            api_url="https://cl.linkedin.com/jobs/view/desarrollador-python-junior-trabajo-remoto-at-bairesdev-4323360135",
            extra_data={
                "requirements": [
                    "1 año de experiencia con Python",
                    "Buen conocimiento de algoritmos básicos y estructuras de datos",
                    "Conocimiento básico de sistemas de control de versiones, preferiblemente Git",
                    "Buen nivel de inglés"
                ],
                "responsibilities": [
                    "Desarrollar y mantener aplicaciones Python",
                    "Colaborar con equipos de desarrollo en diversos proyectos",
                    "Identificar y solucionar errores de software",
                    "Participar en revisiones de código",
                    "Mantenerse actualizado con nuevos frameworks y bibliotecas de Python"
                ]
            }
        ),
        JobOffering(
            id="job-3",
            keyword="fullstack",
            company_name="AgendaPro",
            role_name="Desarrollador Junior",
            description="Desarrollador Junior para unirse a nuestro equipo en crecimiento. Oportunidad de aprender y participar en mejora continua de plataformas.",
            url="https://cl.linkedin.com/jobs/view/desarrollador-junior-at-agendapro-4323576214",
            location="Chile",
            work_mode="Jornada completa",
            type="full-time",
            salary=None,
            sectors="backend,ruby,nodejs",
            post_date=datetime(2025, 11, 20),
            last_updated=datetime(2025, 11, 20),
            uid="agendapro-4323576214",
            api_url="https://cl.linkedin.com/jobs/view/desarrollador-junior-at-agendapro-4323576214",
            extra_data={
                "requirements": [
                    "0 a 2 años de experiencia en desarrollo backend",
                    "Conocimientos básicos en Ruby on Rails, Node.js o tecnologías similares",
                    "Comprensión inicial de conceptos de diseño y patrones de arquitectura (MVC, servicios)",
                    "Ganas de aprender, mejorar y trabajar en equipo"
                ],
                "responsibilities": [
                    "Apoyar en la estandarización de proyectos",
                    "Contribuir al mantenimiento y mejora de la arquitectura de software",
                    "Implementar pequeñas funcionalidades siguiendo los contratos técnicos definidos",
                    "Colaborar con otros desarrolladores",
                    "Participar activamente en revisiones de código"
                ]
            }
        ),
        JobOffering(
            id="job-4",
            keyword="backend",
            company_name="Uber",
            role_name="Graduate 2025 Software Engineer I Backend, Chile",
            description="Early career software engineer para trabajar en proyectos de delivery y backend development en Santiago, Chile.",
            url="https://cl.linkedin.com/jobs/view/graduate-2025-software-engineer-i-backend-chile-at-uber-4240382405",
            location="Gran Santiago, Región Metropolitana de Santiago, Chile",
            work_mode="Jornada completa",
            type="full-time",
            salary=None,
            sectors="backend,java,go,python",
            post_date=datetime(2025, 11, 14),
            last_updated=datetime(2025, 11, 14),
            uid="uber-4240382405",
            api_url="https://cl.linkedin.com/jobs/view/graduate-2025-software-engineer-i-backend-chile-at-uber-4240382405",
            extra_data={
                "requirements": [
                    "Bachelor's degree in Computer Science, Engineering, Mathematics, or a related field",
                    "Proficiency in at least one programming language (Go, Java, Python, C/C++)",
                    "Solid understanding of data structures, algorithms, and system design",
                    "Strong written and verbal communication skills in English"
                ],
                "responsibilities": [
                    "Design, develop, test, deploy, and maintain scalable backend systems",
                    "Collaborate with cross-functional teams to define and build new product features",
                    "Participate in code reviews",
                    "Work with modern backend and web technologies",
                    "Maintain production services and participate in on-call rotations"
                ]
            }
        ),
        JobOffering(
            id="job-5",
            keyword="fullstack",
            company_name="Coderhub",
            role_name="Fullstack Developer Junior",
            description="Full Stack Developer Junior para desarrollar proyectos innovadores con impacto real en el ecosistema digital.",
            url="https://cl.linkedin.com/jobs/view/fullstack-developer-junior-at-coderhub-4315872864",
            location="Gran Santiago, Región Metropolitana de Santiago, Chile",
            work_mode="Jornada completa",
            type="full-time",
            salary=None,
            sectors="fullstack,python,php,vue",
            post_date=datetime(2025, 10, 16),
            last_updated=datetime(2025, 10, 16),
            uid="coderhub-4315872864",
            api_url="https://cl.linkedin.com/jobs/view/fullstack-developer-junior-at-coderhub-4315872864",
            extra_data={
                "requirements": [
                    "Título en Ingeniería en Computación, Informática",
                    "0 a 2 años en roles similares o participación en proyectos de desarrollo",
                    "Lenguajes y frameworks: Python, PHP, Vue.js, SQL",
                    "Herramientas: Git/GitHub, Visual Studio Code",
                    "Marco de trabajo ágil: Scrum"
                ],
                "responsibilities": [
                    "Programar y mantener funcionalidades en aplicaciones web y móviles",
                    "Desarrollar scripts, módulos y mejoras en plataformas internas",
                    "Participar en revisiones de código y pruebas básicas",
                    "Colaborar con equipo interno",
                    "Documentar código y aportar mejoras"
                ]
            }
        ),
        JobOffering(
            id="job-6",
            keyword="fullstack",
            company_name="Grupo Falabella",
            role_name="Junior Full Stack Software Engineer",
            description="Full Stack Software Engineer para impulsar el crecimiento de Falabella Business Center con soluciones en planning y sourcing.",
            url="https://cl.linkedin.com/jobs/view/junior-full-stack-software-engineer-at-grupo-falabella-4312711285",
            location="Gran Santiago, Región Metropolitana de Santiago, Chile",
            work_mode="Jornada completa",
            type="full-time",
            salary=None,
            sectors="fullstack,react,nodejs,java",
            post_date=datetime(2025, 11, 20),
            last_updated=datetime(2025, 11, 20),
            uid="falabella-4312711285",
            api_url="https://cl.linkedin.com/jobs/view/junior-full-stack-software-engineer-at-grupo-falabella-4312711285",
            extra_data={
                "requirements": [
                    "Mínimo 2 años de experiencia en desarrollo de software, con enfoque en front-end y back-end",
                    "Manejo de frameworks modernos: React.js, Angular o Vue.js",
                    "Experiencia en diseño responsivo y accesibilidad (WCAG)",
                    "Desarrollo backend con Node.js, Java, Spring Boot o Python",
                    "Al menos 1 año de experiencia con bases de datos: PostgreSQL, MySQL o Cloud SQL",
                    "Conocimiento en infraestructura como código: Terraform y servicios en la nube GCP"
                ],
                "responsibilities": [
                    "Liderar el diseño y desarrollo de interfaces modernas y responsivas",
                    "Implementar soluciones backend escalables y seguras",
                    "Colaborar con equipos multidisciplinarios",
                    "Mejorar continuamente los procesos de desarrollo con prácticas de CI/CD",
                    "Brindar soporte técnico y mentoría a otros miembros del equipo"
                ]
            }
        ),
        JobOffering(
            id="job-7",
            keyword="frontend",
            company_name="NeuralWorks",
            role_name="Front-end Developer",
            description="Frontend Developer para crear e implementar la experiencia de usuario en proyectos de Analytics e IA",
            url="https://cl.linkedin.com/jobs/view/front-end-developer-at-neuralworks-4319282254",
            location="Gran Santiago, Región Metropolitana de Santiago, Chile",
            work_mode="Jornada completa",
            type="full-time",
            salary=None,
            sectors="frontend,react,javascript",
            post_date=datetime(2025, 10, 27),
            last_updated=datetime(2025, 10, 27),
            uid="neuralworks-4319282254",
            api_url="https://cl.linkedin.com/jobs/view/front-end-developer-at-neuralworks-4319282254",
            extra_data={
                "requirements": [
                    "Estudios de Ingeniería Civil en Computación o similar",
                    "Experiencia previa de al menos 2 años como Frontend Developer",
                    "Comprensión de las API RESTful",
                    "Habilidad para trabajar en equipo",
                    "Buen manejo de inglés, sobre todo en lectura"
                ],
                "responsibilities": [
                    "Diseñar e implementar módulos de software basados en IA/Datos",
                    "Trabajar bajo sprints con objetivos claros",
                    "Ser parte de reuniones de equipo",
                    "Documentar código y lecciones aprendidas",
                    "Colaborar en la creación de la base de conocimientos"
                ]
            }
        ),
        JobOffering(
            id="job-8",
            keyword="fullstack",
            company_name="BC Tecnología",
            role_name="Desarrollador/a Full-Stack",
            description="Desarrollador Full Stack para atender clientes de alto impacto en sectores como servicios financieros, seguros, retail y gobierno.",
            url="https://cl.linkedin.com/jobs/view/desarrollador-a-full-stack-at-bc-tecnología-4319212323",
            location="Gran Santiago, Región Metropolitana de Santiago, Chile",
            work_mode="Jornada completa",
            type="full-time",
            salary=None,
            sectors="fullstack,nodejs,angular",
            post_date=datetime(2025, 10, 27),
            last_updated=datetime(2025, 10, 27),
            uid="bc-tecnologia-4319212323",
            api_url="https://cl.linkedin.com/jobs/view/desarrollador-a-full-stack-at-bc-tecnología-4319212323",
            extra_data={
                "requirements": [
                    "Experiencia mínima de 2 años en desarrollo de software",
                    "Dominio experto de HTML, CSS, JavaScript y AJAX",
                    "Experiencia en diseño adaptativo y desarrollo web/móvil",
                    "Conocimiento práctico de APIs REST",
                    "Experiencia con frameworks JavaScript MVC (AngularJS, Backbone)"
                ],
                "responsibilities": [
                    "Crear o modificar componentes de software",
                    "Desarrollar y mantener componentes Backend y Frontend",
                    "Participar en certificaciones de pruebas",
                    "Diagnosticar y corregir defectos detectados",
                    "Aplicar buenas prácticas de programación"
                ]
            }
        ),
        JobOffering(
            id="job-9",
            keyword="fullstack",
            company_name="Deloitte",
            role_name="Desarrollador/a Full Stack Junior",
            description="Desarrollador Full Stack Junior para el equipo de Tecnología Tax, trabajando en soluciones tecnológicas de alta calidad.",
            url="https://cl.linkedin.com/jobs/view/desarrollador-a-full-stack-junior-at-deloitte-4305155698",
            location="Las Condes, Región Metropolitana de Santiago, Chile",
            work_mode="Jornada completa",
            type="full-time",
            salary=None,
            sectors="fullstack,dotnet,csharp",
            post_date=datetime(2025, 11, 15),
            last_updated=datetime(2025, 11, 15),
            uid="deloitte-4305155698",
            api_url="https://cl.linkedin.com/jobs/view/desarrollador-a-full-stack-junior-at-deloitte-4305155698",
            extra_data={
                "requirements": [
                    "Título profesional en carreras de Informática, Ingeniería de software o afines",
                    "Desde 1 año en gestión de proyectos de desarrollo de software",
                    "Manejo de stack tecnológico .NET 7.0, .Net Framework 4.X, C#",
                    "Conocimiento en arquitectura en la nube basada en servicios Azure, AWS",
                    "Dominio de inglés Conversacional Nivel Intermedio/Avanzado"
                ],
                "responsibilities": [
                    "Entregar avance semanal del desarrollo de proyectos",
                    "Desarrollo, mantenimiento, documentación y soporte de soluciones tecnológicas",
                    "Realizar mejora continua y aplicación de estándares",
                    "Documentación oportuna para el software y entregables"
                ]
            }
        ),
        JobOffering(
            id="job-10",
            keyword="backend",
            company_name="Sezzle",
            role_name="Junior Software Engineer (Chile)",
            description="Junior Software Engineer para empresa de fintech que revoluciona la experiencia de compras con planes de pago sin intereses.",
            url="https://cl.linkedin.com/jobs/view/junior-software-engineer-chile-at-sezzle-4271076854",
            location="Área metropolitana de Santiago",
            work_mode="Jornada completa",
            type="full-time",
            salary="$1,500 - $2,700 USD/month",
            sectors="backend,frontend,golang,react",
            post_date=datetime(2025, 11, 5),
            last_updated=datetime(2025, 11, 5),
            uid="sezzle-4271076854",
            api_url="https://cl.linkedin.com/jobs/view/junior-software-engineer-chile-at-sezzle-4271076854",
            extra_data={
                "requirements": [
                    "Experience working on single page web applications (SPA)",
                    "Experience with backend API development",
                    "Experience with relational database storage and retrieval",
                    "Familiarity with software engineering tools and release processes",
                    "BS degree in Computer Science or Engineering, or equivalent experience"
                ],
                "responsibilities": [
                    "Be an integral part of the software development lifecycle",
                    "Work as an integrated team member developing new features",
                    "Evaluate and deploy software tools, processes, and metrics",
                    "Provide support and consulting on software systems usage",
                    "Ensure compliance with project plans and industry standards"
                ]
            }
        ),
    ]
    
    try:
        # Add all job offerings
        for job in job_offerings:
            # Check if already exists
            existing = db.query(JobOffering).filter(JobOffering.id == job.id).first()
            if existing:
                print(f"⚠️  Job offering '{job.id}' already exists, skipping...")
                continue
            
            db.add(job)
            print(f"✅ Added job offering: {job.role_name} at {job.company_name}")
        
        db.commit()
        print(f"\n🎉 Successfully seeded {len(job_offerings)} job offerings!")
        
    except IntegrityError as e:
        db.rollback()
        print(f"❌ Error seeding job offerings: {e}")
    except Exception as e:
        db.rollback()
        print(f"❌ Unexpected error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Seeding job offerings...")
    seed_job_offerings()

