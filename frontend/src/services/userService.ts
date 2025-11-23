import { API_ENDPOINTS, USE_MOCK_DATA, apiCall } from './api'
import { mockUser } from './mockData'
import type { UserCreate, UserLogin, UserResponse, UserUpdate } from './types'

export const userService = {
    async create(data: UserCreate): Promise<UserResponse> {
        if (USE_MOCK_DATA) {
            // Simulate API delay
            await new Promise(resolve => setTimeout(resolve, 500))
            return {
                ...mockUser,
                email: data.email,
                full_name: data.full_name,
            }
        }

        return apiCall<UserResponse>(API_ENDPOINTS.users, {
            method: 'POST',
            body: JSON.stringify(data),
        })
    },

    async login(credentials: UserLogin): Promise<UserResponse> {
        if (USE_MOCK_DATA) {
            await new Promise(resolve => setTimeout(resolve, 500))
            // Store mock user in localStorage for session
            localStorage.setItem('user', JSON.stringify(mockUser))
            return mockUser
        }

        const user = await apiCall<UserResponse>(API_ENDPOINTS.login, {
            method: 'POST',
            body: JSON.stringify(credentials),
        })

        localStorage.setItem('user', JSON.stringify(user))
        return user
    },

    async getById(id: number): Promise<UserResponse> {
        if (USE_MOCK_DATA) {
            await new Promise(resolve => setTimeout(resolve, 300))
            return mockUser
        }

        return apiCall<UserResponse>(API_ENDPOINTS.userById(id))
    },

    async update(id: number, data: UserUpdate): Promise<UserResponse> {
        if (USE_MOCK_DATA) {
            await new Promise(resolve => setTimeout(resolve, 500))
            return {
                ...mockUser,
                ...data,
                updated_at: new Date().toISOString(),
            }
        }

        return apiCall<UserResponse>(API_ENDPOINTS.userById(id), {
            method: 'PATCH',
            body: JSON.stringify(data),
        })
    },

    getCurrentUser(): UserResponse | null {
        const userStr = localStorage.getItem('user')
        return userStr ? JSON.parse(userStr) : null
    },

    logout() {
        localStorage.removeItem('user')
    },
}
