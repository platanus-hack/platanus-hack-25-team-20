const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const API_ENDPOINTS = {
    // Health
    health: `${API_BASE_URL}/health`,

    // Users
    users: `${API_BASE_URL}/api/v1/users`,
    userById: (id: number) => `${API_BASE_URL}/api/v1/users/${id}`,
    login: `${API_BASE_URL}/api/v1/users/login`,
    
    // User Profile
    userProfile: (userId: number) => `${API_BASE_URL}/api/v1/users/${userId}/profile`,
    userProfileById: (profileId: number) => `${API_BASE_URL}/api/v1/profiles/${profileId}`,
    
    // Projects
    projects: `${API_BASE_URL}/api/v1/projects`,
    projectById: (id: number) => `${API_BASE_URL}/api/v1/projects/${id}`,
    userProjects: (userId: number) => `${API_BASE_URL}/api/v1/users/${userId}/projects`,
    
    // Skills
    userSkills: (userId: number) => `${API_BASE_URL}/api/v1/users/${userId}/skills`,
    skillsById: (id: number) => `${API_BASE_URL}/api/v1/skills/${id}`,
    
    // CVs
    projectCVs: (projectId: number) => `${API_BASE_URL}/api/v1/projects/${projectId}/cvs`,
    cvById: (cvId: number) => `${API_BASE_URL}/api/v1/cvs/${cvId}`,
    cvRegenerate: (cvId: number) => `${API_BASE_URL}/api/v1/cvs/${cvId}/regenerate`,
    
    // Templates
    templates: `${API_BASE_URL}/api/v1/templates`,
    templateById: (id: number) => `${API_BASE_URL}/api/v1/templates/${id}`,
    
    // Job Offerings (cambio de jobs a job-offerings)
    jobOfferings: `${API_BASE_URL}/api/v1/job-offerings`,
    jobOfferingById: (id: string) => `${API_BASE_URL}/api/v1/job-offerings/${id}`,
    
    // Applications (cambio de submissions a applications)
    applications: `${API_BASE_URL}/api/v1/applications`,
    applicationById: (id: number) => `${API_BASE_URL}/api/v1/applications/${id}`,
    userApplications: (userId: number) => `${API_BASE_URL}/api/v1/users/${userId}/applications`,
    
    // Extraction
    extractProfile: (userId: number) => `${API_BASE_URL}/api/v1/users/${userId}/extract-profile`,
}

// Use mock data for development (set to false when backend is ready)
export const USE_MOCK_DATA = false

export async function apiCall<T>(
    url: string,
    options?: RequestInit
): Promise<T> {
    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options?.headers,
            },
        })

        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`)
        }

        return await response.json()
    } catch (error) {
        console.error('API call failed:', error)
        throw error
    }
}
