import type { UserResponse, ProjectResponse, UserSkillsResponse } from './types'

export const mockUser: UserResponse = {
    id: 1,
    email: 'john.doe@example.com',
    full_name: 'John Doe',
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
}

// Extended user profile data (NOT YET IN BACKEND - mocked for UI development)
export const mockUserProfile = {
    languages: ['English (Native)', 'Spanish (Fluent)'], // TODO: Add to backend UserResponse
    estimatedSalary: '$120k - $150k', // TODO: Add to backend UserResponse
    experience: [ // TODO: Add experience tracking to backend
        { company: 'Tech Company Inc.', position: 'Senior Developer', period: '2021 - Present' },
        { company: 'StartupXYZ', position: 'Full Stack Developer', period: '2019 - 2021' },
    ],
}

export const mockProjects: ProjectResponse[] = [
    {
        id: 1,
        user_id: 1,
        name: 'Senior Full Stack Developer Application',
        target_role: 'Senior Full Stack Developer',
        cv_style: 'modern',
        preferences: {
            color_scheme: 'blue',
            font: 'professional',
            sections: ['experience', 'education', 'skills', 'projects'],
            emphasis: 'technical',
        },
        created_at: '2024-01-15T00:00:00Z',
        updated_at: '2024-01-15T00:00:00Z',
    },
    {
        id: 2,
        user_id: 1,
        name: 'Frontend Engineer at StartupXYZ',
        target_role: 'Frontend Engineer',
        cv_style: 'creative',
        preferences: {
            color_scheme: 'purple',
            font: 'modern',
            sections: ['experience', 'skills', 'projects', 'certifications'],
            emphasis: 'design',
        },
        created_at: '2024-01-10T00:00:00Z',
        updated_at: '2024-01-10T00:00:00Z',
    },
    {
        id: 3,
        user_id: 1,
        name: 'Backend Developer - FinTech',
        target_role: 'Backend Developer',
        cv_style: 'professional',
        preferences: {
            color_scheme: 'green',
            font: 'classic',
            sections: ['experience', 'education', 'skills', 'achievements'],
            emphasis: 'backend',
        },
        created_at: '2024-01-05T00:00:00Z',
        updated_at: '2024-01-08T00:00:00Z',
    },
]

// Mock skills list (using new schema with skill_text and skill_type)
export const mockSkillsList: UserSkillsResponse[] = [
    {
        id: 1,
        user_id: 1,
        skill_text: 'Senior Software Engineer at Tech Company Inc. - Led development of microservices architecture',
        skill_type: 'experience',
        raw_input: 'CV Upload',
        source: 'cv_upload',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
    },
    {
        id: 2,
        user_id: 1,
        skill_text: 'TypeScript',
        skill_type: 'dev-skill',
        raw_input: 'Programming languages from CV',
        source: 'cv_upload',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
    },
    {
        id: 3,
        user_id: 1,
        skill_text: 'React',
        skill_type: 'dev-skill',
        raw_input: 'Frameworks from CV',
        source: 'cv_upload',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
    },
    {
        id: 4,
        user_id: 1,
        skill_text: 'Python',
        skill_type: 'dev-skill',
        raw_input: 'Programming languages from CV',
        source: 'cv_upload',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
    },
    {
        id: 5,
        user_id: 1,
        skill_text: 'AWS Certified Solutions Architect',
        skill_type: 'certificate',
        raw_input: 'Certifications section',
        source: 'cv_upload',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
    },
    {
        id: 6,
        user_id: 1,
        skill_text: 'Docker',
        skill_type: 'dev-skill',
        raw_input: 'Tools from CV',
        source: 'cv_upload',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
    },
    {
        id: 7,
        user_id: 1,
        skill_text: 'English (Fluent), Spanish (Native)',
        skill_type: 'extra',
        raw_input: 'Languages',
        source: 'cv_upload',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
    },
]

// Backward compatibility - single skills object
export const mockSkills: UserSkillsResponse = mockSkillsList[0]

// Mock job listings - Real data from LinkedIn Chile
export const mockJobs: import('./types').Job[] = [
    {
        id: 'job-1',
        title: 'Desarrollador Front-End Junior',
        company: 'Bruno Fritsch',
        location: 'Gran Santiago, Región Metropolitana de Santiago, Chile',
        type: 'Jornada completa',
        salary: null,
        areas: ['Frontend', 'React', 'TypeScript'],
        description: 'Desarrollador Frontend Junior para nuestra área de Ecommerce & Marketing Digital. Trabajando con React.js y TypeScript.',
        url: 'https://cl.linkedin.com/jobs/view/desarrollador-front-end-junior-at-bruno-fritsch-4323246353',
        requirements: [
            'Título en Ciencias de la Computación, Ingeniería de Software o campo relacionado',
            '0 a 2 años de experiencia laboral previa',
            'Experiencia demostrable en el uso de TypeScript',
            'Conocimiento de acciones, componentes, suscriptores y fetchers en React',
            'Conocimiento en herramientas de control de versiones (Git)'
        ],
        responsibilities: [
            'Diseñar, desarrollar y mantener componentes de frontend utilizando React.js y TypeScript',
            'Implementar y gestionar actions y subscriber para el manejo eficiente del estado',
            'Integrar y consumir endpoints utilizando fetchers',
            'Diseñar y aplicar principios de Material Design utilizando Material-UI',
            'Colaborar con diseñadores y desarrolladores backend'
        ],
        post_date: '2025-11-19T00:00:00.000Z',
    },
    {
        id: 'job-2',
        title: 'Desarrollador Python Junior - Trabajo Remoto',
        company: 'BairesDev',
        location: 'Chile',
        type: 'Jornada completa',
        salary: null,
        areas: ['Backend', 'Python'],
        description: 'Desarrollador Python Junior para trabajar de forma remota. Oportunidad de trabajar con equipo global en proyectos de vanguardia.',
        url: 'https://cl.linkedin.com/jobs/view/desarrollador-python-junior-trabajo-remoto-at-bairesdev-4323360135',
        requirements: [
            '1 año de experiencia con Python',
            'Buen conocimiento de algoritmos básicos y estructuras de datos',
            'Conocimiento básico de sistemas de control de versiones, preferiblemente Git',
            'Buen nivel de inglés'
        ],
        responsibilities: [
            'Desarrollar y mantener aplicaciones Python',
            'Colaborar con equipos de desarrollo en diversos proyectos',
            'Identificar y solucionar errores de software',
            'Participar en revisiones de código',
            'Mantenerse actualizado con nuevos frameworks y bibliotecas de Python'
        ],
        post_date: '2025-11-18T00:00:00.000Z',
    },
    {
        id: 'job-3',
        title: 'Desarrollador Junior',
        company: 'AgendaPro',
        location: 'Chile',
        type: 'Jornada completa',
        salary: null,
        areas: ['Backend', 'Ruby on Rails', 'Node.js'],
        description: 'Desarrollador Junior para unirse a nuestro equipo en crecimiento. Oportunidad de aprender y participar en mejora continua de plataformas.',
        url: 'https://cl.linkedin.com/jobs/view/desarrollador-junior-at-agendapro-4323576214',
        requirements: [
            '0 a 2 años de experiencia en desarrollo backend',
            'Conocimientos básicos en Ruby on Rails, Node.js o tecnologías similares',
            'Comprensión inicial de conceptos de diseño y patrones de arquitectura (MVC, servicios)',
            'Ganas de aprender, mejorar y trabajar en equipo'
        ],
        responsibilities: [
            'Apoyar en la estandarización de proyectos',
            'Contribuir al mantenimiento y mejora de la arquitectura de software',
            'Implementar pequeñas funcionalidades siguiendo los contratos técnicos definidos',
            'Colaborar con otros desarrolladores',
            'Participar activamente en revisiones de código'
        ],
        post_date: '2025-11-20T00:00:00.000Z',
    },
    {
        id: 'job-4',
        title: 'Graduate 2025 Software Engineer I Backend, Chile',
        company: 'Uber',
        location: 'Gran Santiago, Región Metropolitana de Santiago, Chile',
        type: 'Jornada completa',
        salary: null,
        areas: ['Backend', 'Java', 'Go', 'Python'],
        description: 'Early career software engineer para trabajar en proyectos de delivery y backend development en Santiago, Chile.',
        url: 'https://cl.linkedin.com/jobs/view/graduate-2025-software-engineer-i-backend-chile-at-uber-4240382405',
        requirements: [
            'Bachelor\'s degree in Computer Science, Engineering, Mathematics, or a related field',
            'Proficiency in at least one programming language (Go, Java, Python, C/C++)',
            'Solid understanding of data structures, algorithms, and system design',
            'Strong written and verbal communication skills in English'
        ],
        responsibilities: [
            'Design, develop, test, deploy, and maintain scalable backend systems',
            'Collaborate with cross-functional teams to define and build new product features',
            'Participate in code reviews',
            'Work with modern backend and web technologies',
            'Maintain production services and participate in on-call rotations'
        ],
        post_date: '2025-11-14T00:00:00.000Z',
    },
    {
        id: 'job-5',
        title: 'Fullstack Developer Junior',
        company: 'Coderhub',
        location: 'Gran Santiago, Región Metropolitana de Santiago, Chile',
        type: 'Jornada completa',
        salary: null,
        areas: ['Full Stack', 'Python', 'PHP', 'Vue.js'],
        description: 'Full Stack Developer Junior para desarrollar proyectos innovadores con impacto real en el ecosistema digital.',
        url: 'https://cl.linkedin.com/jobs/view/fullstack-developer-junior-at-coderhub-4315872864',
        requirements: [
            'Título en Ingeniería en Computación, Informática',
            '0 a 2 años en roles similares o participación en proyectos de desarrollo',
            'Lenguajes y frameworks: Python, PHP, Vue.js, SQL',
            'Herramientas: Git/GitHub, Visual Studio Code',
            'Marco de trabajo ágil: Scrum'
        ],
        responsibilities: [
            'Programar y mantener funcionalidades en aplicaciones web y móviles',
            'Desarrollar scripts, módulos y mejoras en plataformas internas',
            'Participar en revisiones de código y pruebas básicas',
            'Colaborar con equipo interno',
            'Documentar código y aportar mejoras'
        ],
        post_date: '2025-10-16T00:00:00.000Z',
    },
    {
        id: 'job-6',
        title: 'Junior Full Stack Software Engineer',
        company: 'Grupo Falabella',
        location: 'Gran Santiago, Región Metropolitana de Santiago, Chile',
        type: 'Jornada completa',
        salary: null,
        areas: ['Full Stack', 'React', 'Node.js', 'Java'],
        description: 'Full Stack Software Engineer para impulsar el crecimiento de Falabella Business Center con soluciones en planning y sourcing.',
        url: 'https://cl.linkedin.com/jobs/view/junior-full-stack-software-engineer-at-grupo-falabella-4312711285',
        requirements: [
            'Mínimo 2 años de experiencia en desarrollo de software, con enfoque en front-end y back-end',
            'Manejo de frameworks modernos: React.js, Angular o Vue.js',
            'Experiencia en diseño responsivo y accesibilidad (WCAG)',
            'Desarrollo backend con Node.js, Java, Spring Boot o Python',
            'Al menos 1 año de experiencia con bases de datos: PostgreSQL, MySQL o Cloud SQL',
            'Conocimiento en infraestructura como código: Terraform y servicios en la nube GCP'
        ],
        responsibilities: [
            'Liderar el diseño y desarrollo de interfaces modernas y responsivas',
            'Implementar soluciones backend escalables y seguras',
            'Colaborar con equipos multidisciplinarios',
            'Mejorar continuamente los procesos de desarrollo con prácticas de CI/CD',
            'Brindar soporte técnico y mentoría a otros miembros del equipo'
        ],
        post_date: '2025-11-20T00:00:00.000Z',
    },
    {
        id: 'job-7',
        title: 'Front-end Developer',
        company: 'NeuralWorks',
        location: 'Gran Santiago, Región Metropolitana de Santiago, Chile',
        type: 'Jornada completa',
        salary: null,
        areas: ['Frontend', 'React', 'JavaScript'],
        description: 'Frontend Developer para crear e implementar la experiencia de usuario en proyectos de Analytics e IA',
        url: 'https://cl.linkedin.com/jobs/view/front-end-developer-at-neuralworks-4319282254',
        requirements: [
            'Estudios de Ingeniería Civil en Computación o similar',
            'Experiencia previa de al menos 2 años como Frontend Developer',
            'Comprensión de las API RESTful',
            'Habilidad para trabajar en equipo',
            'Buen manejo de inglés, sobre todo en lectura'
        ],
        responsibilities: [
            'Diseñar e implementar módulos de software basados en IA/Datos',
            'Trabajar bajo sprints con objetivos claros',
            'Ser parte de reuniones de equipo',
            'Documentar código y lecciones aprendidas',
            'Colaborar en la creación de la base de conocimientos'
        ],
        post_date: '2025-10-27T00:00:00.000Z',
    },
    {
        id: 'job-8',
        title: 'Desarrollador/a Full-Stack',
        company: 'BC Tecnología',
        location: 'Gran Santiago, Región Metropolitana de Santiago, Chile',
        type: 'Jornada completa',
        salary: null,
        areas: ['Full Stack', 'Node.js', 'AngularJS'],
        description: 'Desarrollador Full Stack para atender clientes de alto impacto en sectores como servicios financieros, seguros, retail y gobierno.',
        url: 'https://cl.linkedin.com/jobs/view/desarrollador-a-full-stack-at-bc-tecnología-4319212323',
        requirements: [
            'Experiencia mínima de 2 años en desarrollo de software',
            'Dominio experto de HTML, CSS, JavaScript y AJAX',
            'Experiencia en diseño adaptativo y desarrollo web/móvil',
            'Conocimiento práctico de APIs REST',
            'Experiencia con frameworks JavaScript MVC (AngularJS, Backbone)'
        ],
        responsibilities: [
            'Crear o modificar componentes de software',
            'Desarrollar y mantener componentes Backend y Frontend',
            'Participar en certificaciones de pruebas',
            'Diagnosticar y corregir defectos detectados',
            'Aplicar buenas prácticas de programación'
        ],
        post_date: '2025-10-27T00:00:00.000Z',
    },
    {
        id: 'job-9',
        title: 'Desarrollador/a Full Stack Junior',
        company: 'Deloitte',
        location: 'Las Condes, Región Metropolitana de Santiago, Chile',
        type: 'Jornada completa',
        salary: null,
        areas: ['Full Stack', '.NET', 'C#'],
        description: 'Desarrollador Full Stack Junior para el equipo de Tecnología Tax, trabajando en soluciones tecnológicas de alta calidad.',
        url: 'https://cl.linkedin.com/jobs/view/desarrollador-a-full-stack-junior-at-deloitte-4305155698',
        requirements: [
            'Título profesional en carreras de Informática, Ingeniería de software o afines',
            'Desde 1 año en gestión de proyectos de desarrollo de software',
            'Manejo de stack tecnológico .NET 7.0, .Net Framework 4.X, C#',
            'Conocimiento en arquitectura en la nube basada en servicios Azure, AWS',
            'Dominio de inglés Conversacional Nivel Intermedio/Avanzado'
        ],
        responsibilities: [
            'Entregar avance semanal del desarrollo de proyectos',
            'Desarrollo, mantenimiento, documentación y soporte de soluciones tecnológicas',
            'Realizar mejora continua y aplicación de estándares',
            'Documentación oportuna para el software y entregables'
        ],
        post_date: '2025-11-15T00:00:00.000Z',
    },
    {
        id: 'job-10',
        title: 'Junior Software Engineer (Chile)',
        company: 'Sezzle',
        location: 'Área metropolitana de Santiago',
        type: 'Jornada completa',
        salary: '$1,500 - $2,700 USD/month',
        areas: ['Backend', 'Frontend', 'Golang', 'React'],
        description: 'Junior Software Engineer para empresa de fintech que revoluciona la experiencia de compras con planes de pago sin intereses.',
        url: 'https://cl.linkedin.com/jobs/view/junior-software-engineer-chile-at-sezzle-4271076854',
        requirements: [
            'Experience working on single page web applications (SPA)',
            'Experience with backend API development',
            'Experience with relational database storage and retrieval',
            'Familiarity with software engineering tools and release processes',
            'BS degree in Computer Science or Engineering, or equivalent experience'
        ],
        responsibilities: [
            'Be an integral part of the software development lifecycle',
            'Work as an integrated team member developing new features',
            'Evaluate and deploy software tools, processes, and metrics',
            'Provide support and consulting on software systems usage',
            'Ensure compliance with project plans and industry standards'
        ],
        post_date: '2025-11-05T00:00:00.000Z',
    },
]

// Mock submissions/applications (using new ApplicationResponse schema)
export const mockSubmissions: import('./types').ApplicationResponse[] = [
    {
        id: 1,
        user_id: 1,
        job_offering_id: 'job-1',
        cv_id: 1,
        status: 'under_review',
        notes: null,
        created_at: '2025-11-19T00:00:00Z',
        updated_at: '2025-11-19T00:00:00Z',
    },
    {
        id: 2,
        user_id: 1,
        job_offering_id: 'job-3',
        cv_id: 2,
        status: 'interview_scheduled',
        notes: 'Primera entrevista técnica programada',
        created_at: '2025-11-20T00:00:00Z',
        updated_at: '2025-11-20T00:00:00Z',
    },
    {
        id: 3,
        user_id: 1,
        job_offering_id: 'job-2',
        cv_id: 1,
        status: 'rejected',
        notes: 'No seleccionado para esta posición',
        created_at: '2025-11-18T00:00:00Z',
        updated_at: '2025-11-20T00:00:00Z',
    },
]
