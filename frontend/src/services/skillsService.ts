import { API_ENDPOINTS, USE_MOCK_DATA, apiCall } from "./api";
import { mockSkillsList } from "./mockData";
import type {
  UserSkillsCreate,
  UserSkillsResponse,
  UserSkillsUpdate,
  UserSkillsGroupedResponse,
} from "./types";

export const skillsService = {
  async create(
    userId: number,
    data: UserSkillsCreate
  ): Promise<UserSkillsResponse> {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) => setTimeout(resolve, 500));
      return {
        id: Date.now(),
        user_id: userId,
        ...data,
        source: data.source || null,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
    }

    return apiCall<UserSkillsResponse>(API_ENDPOINTS.userSkills(userId), {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  async getByUserId(userId: number): Promise<UserSkillsResponse[]> {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) => setTimeout(resolve, 300));
      return mockSkillsList;
    }

    // Backend returns grouped response, flatten it to array
    const grouped = await apiCall<UserSkillsGroupedResponse>(
      API_ENDPOINTS.userSkills(userId)
    );
    return [
      ...grouped.experience,
      ...grouped.dev_skills,
      ...grouped.certificates,
      ...grouped.extra,
    ];
  },

  async getByUserIdGrouped(userId: number): Promise<UserSkillsGroupedResponse> {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) => setTimeout(resolve, 300));
      // Group mock skills by type
      return {
        experience: mockSkillsList.filter((s) => s.skill_type === "experience"),
        dev_skills: mockSkillsList.filter((s) => s.skill_type === "dev-skill"),
        certificates: mockSkillsList.filter(
          (s) => s.skill_type === "certificate"
        ),
        extra: mockSkillsList.filter((s) => s.skill_type === "extra"),
      };
    }

    return apiCall<UserSkillsGroupedResponse>(API_ENDPOINTS.userSkills(userId));
  },

  async getById(id: number): Promise<UserSkillsResponse> {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) => setTimeout(resolve, 300));
      const skill = mockSkillsList.find((s) => s.id === id);
      if (!skill) throw new Error(`Skill with id ${id} not found`);
      return skill;
    }

    return apiCall<UserSkillsResponse>(API_ENDPOINTS.skillsById(id));
  },

  async update(
    id: number,
    data: UserSkillsUpdate
  ): Promise<UserSkillsResponse> {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) => setTimeout(resolve, 500));
      const skill = mockSkillsList.find((s) => s.id === id);
      if (!skill) throw new Error(`Skill with id ${id} not found`);
      return {
        ...skill,
        ...data,
        skill_text: data.skill_text || skill.skill_text,
        skill_type: data.skill_type || skill.skill_type,
        raw_input:
          data.raw_input !== undefined ? data.raw_input : skill.raw_input,
        source: data.source !== undefined ? data.source : skill.source,
        updated_at: new Date().toISOString(),
      };
    }

    return apiCall<UserSkillsResponse>(API_ENDPOINTS.skillsById(id), {
      method: "PATCH",
      body: JSON.stringify(data),
    });
  },

  async delete(id: number): Promise<void> {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) => setTimeout(resolve, 500));
      return;
    }

    await apiCall<void>(API_ENDPOINTS.skillsById(id), {
      method: "DELETE",
    });
  },
};
