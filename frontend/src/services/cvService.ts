import { USE_MOCK_DATA, apiCall, API_ENDPOINTS } from "./api";
import type {
  CVCreate,
  CVResponse,
  CVUpdate,
  CVRegenerateRequest,
} from "./types";

export const cvService = {
  async create(projectId: number, cv: CVCreate): Promise<CVResponse> {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) => setTimeout(resolve, 500));
      return {
        id: Date.now(),
        project_id: cv.project_id,
        template_id: cv.template_id,
        base_cv_id: cv.base_cv_id || null,
        content: {},
        rendered_content: null,
        compiled_path: null,
        conversation_history: null,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
    }

    return apiCall<CVResponse>(API_ENDPOINTS.projectCVs(projectId), {
      method: "POST",
      body: JSON.stringify(cv),
    });
  },

  async getById(cvId: number): Promise<CVResponse> {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) => setTimeout(resolve, 300));
      throw new Error("Mock CV not implemented");
    }

    return apiCall<CVResponse>(API_ENDPOINTS.cvById(cvId));
  },

  async getProjectCVs(projectId: number): Promise<CVResponse[]> {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) => setTimeout(resolve, 300));
      return [];
    }

    return apiCall<CVResponse[]>(API_ENDPOINTS.projectCVs(projectId));
  },

  async update(cvId: number, cv: CVUpdate): Promise<CVResponse> {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) => setTimeout(resolve, 500));
      throw new Error("Mock CV update not implemented");
    }

    return apiCall<CVResponse>(API_ENDPOINTS.cvById(cvId), {
      method: "PATCH",
      body: JSON.stringify(cv),
    });
  },

  async regenerate(
    cvId: number,
    request: CVRegenerateRequest
  ): Promise<CVResponse> {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) => setTimeout(resolve, 1000));
      throw new Error("Mock CV regenerate not implemented");
    }

    return apiCall<CVResponse>(API_ENDPOINTS.cvRegenerate(cvId), {
      method: "POST",
      body: JSON.stringify(request),
    });
  },

  async delete(cvId: number): Promise<void> {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) => setTimeout(resolve, 500));
      return;
    }

    await apiCall<void>(API_ENDPOINTS.cvById(cvId), {
      method: "DELETE",
    });
  },
};
