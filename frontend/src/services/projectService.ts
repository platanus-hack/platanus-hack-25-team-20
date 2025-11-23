import { API_ENDPOINTS, USE_MOCK_DATA, apiCall } from "./api";
import { mockProjects } from "./mockData";
import type { ProjectCreate, ProjectResponse, ProjectUpdate } from "./types";

export const projectService = {
  async create(
    data: ProjectCreate & { user_id: number }
  ): Promise<ProjectResponse> {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) => setTimeout(resolve, 500));
      return {
        id: Date.now(),
        user_id: data.user_id,
        name: data.name,
        target_role: data.target_role || null,
        cv_style: data.cv_style || null,
        preferences: data.preferences || null,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
    }

    const { user_id, ...projectData } = data;
    return apiCall<ProjectResponse>(
      `${API_ENDPOINTS.projects}?user_id=${user_id}`,
      {
        method: "POST",
        body: JSON.stringify(projectData),
      }
    );
  },

  async getById(id: number): Promise<ProjectResponse> {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) => setTimeout(resolve, 300));
      return mockProjects.find((p) => p.id === id) || mockProjects[0];
    }

    return apiCall<ProjectResponse>(API_ENDPOINTS.projectById(id));
  },

  async getUserProjects(userId: number): Promise<ProjectResponse[]> {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) => setTimeout(resolve, 300));
      return mockProjects;
    }

    return apiCall<ProjectResponse[]>(API_ENDPOINTS.userProjects(userId));
  },

  async update(id: number, data: ProjectUpdate): Promise<ProjectResponse> {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) => setTimeout(resolve, 500));
      const project = mockProjects.find((p) => p.id === id) || mockProjects[0];
      // Filter out undefined and null values from the update data
      const updates: Partial<ProjectResponse> = {};
      if (data.name !== undefined && data.name !== null)
        updates.name = data.name;
      if (data.target_role !== undefined)
        updates.target_role = data.target_role;
      if (data.cv_style !== undefined) updates.cv_style = data.cv_style;
      if (data.preferences !== undefined)
        updates.preferences = data.preferences;

      return {
        ...project,
        ...updates,
        updated_at: new Date().toISOString(),
      };
    }

    return apiCall<ProjectResponse>(API_ENDPOINTS.projectById(id), {
      method: "PATCH",
      body: JSON.stringify(data),
    });
  },

  async delete(id: number): Promise<void> {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) => setTimeout(resolve, 500));
      return;
    }

    await apiCall<void>(API_ENDPOINTS.projectById(id), {
      method: "DELETE",
    });
  },
};
