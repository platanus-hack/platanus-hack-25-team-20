import { USE_MOCK_DATA, apiCall, API_ENDPOINTS } from './api'
import { mockSubmissions } from './mockData'
import type { Submission, SubmissionCreate, SubmissionUpdate } from './types'

export const submissionService = {
    async create(data: SubmissionCreate): Promise<Submission> {
        if (USE_MOCK_DATA) {
            await new Promise(resolve => setTimeout(resolve, 500))
            return {
                id: Date.now(),
                ...data,
                cv_id: null,
                job_title: 'Mock Job Title', // Would be filled from job data
                company: 'Mock Company',
                submitted_date: new Date().toISOString(),
                status: 'Draft',
                notes: data.notes || null,
                created_at: new Date().toISOString(),
                updated_at: new Date().toISOString(),
            }
        }

        return apiCall<Submission>(API_ENDPOINTS.applications, {
            method: 'POST',
            body: JSON.stringify(data),
        })
    },

    async getUserSubmissions(userId: number): Promise<Submission[]> {
        if (USE_MOCK_DATA) {
            await new Promise(resolve => setTimeout(resolve, 300))
            return mockSubmissions.filter((s: Submission) => s.user_id === userId)
        }

        return apiCall<Submission[]>(API_ENDPOINTS.userApplications(userId))
    },

    async getById(id: number): Promise<Submission> {
        if (USE_MOCK_DATA) {
            await new Promise(resolve => setTimeout(resolve, 300))
            const submission = mockSubmissions.find((s: Submission) => s.id === id)
            if (!submission) {
                throw new Error(`Submission with id ${id} not found`)
            }
            return submission
        }

        return apiCall<Submission>(API_ENDPOINTS.applicationById(id))
    },

    async update(id: number, data: SubmissionUpdate): Promise<Submission> {
        if (USE_MOCK_DATA) {
            await new Promise(resolve => setTimeout(resolve, 500))
            const submission = mockSubmissions.find((s: Submission) => s.id === id)
            if (!submission) {
                throw new Error(`Submission with id ${id} not found`)
            }
            return {
                ...submission,
                ...data,
                updated_at: new Date().toISOString(),
            }
        }

        return apiCall<Submission>(API_ENDPOINTS.applicationById(id), {
            method: 'PATCH',
            body: JSON.stringify(data),
        })
    },

    async delete(id: number): Promise<void> {
        if (USE_MOCK_DATA) {
            await new Promise(resolve => setTimeout(resolve, 500))
            return
        }

        await apiCall<void>(API_ENDPOINTS.applicationById(id), {
            method: 'DELETE',
        })
    },
}
