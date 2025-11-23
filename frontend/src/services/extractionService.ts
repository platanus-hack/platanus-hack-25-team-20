import { USE_MOCK_DATA, apiCall, API_ENDPOINTS } from "./api";
import type { ExtractProfileRequest, ExtractProfileResponse } from "./types";

export const extractionService = {
  async extractProfile(
    userId: number,
    request: ExtractProfileRequest
  ): Promise<ExtractProfileResponse> {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) => setTimeout(resolve, 1000));
      return {
        message: "Profile extracted successfully (mock)",
        profile_updated: true,
        profile_created: false,
        skills_added: 5,
        details: [
          "Added 3 development skills",
          "Added 2 experiences",
          "Updated profile information",
        ],
      };
    }

    return apiCall<ExtractProfileResponse>(
      API_ENDPOINTS.extractProfile(userId),
      {
        method: "POST",
        body: JSON.stringify(request),
      }
    );
  },
};

