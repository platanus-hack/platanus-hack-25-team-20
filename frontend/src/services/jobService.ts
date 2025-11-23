import { USE_MOCK_DATA, apiCall, API_ENDPOINTS } from "./api";
import { mockJobs } from "./mockData";
import type { Job, JobOfferingResponse } from "./types";

// Helper function to map JobOfferingResponse to Job
function mapJobOfferingToJob(jobOffering: JobOfferingResponse): Job {
  return {
    id: jobOffering.id,
    title: jobOffering.role_name || "N/A",
    company: jobOffering.company_name || "N/A",
    location: jobOffering.location || null,
    type: jobOffering.work_mode || null,
    salary: jobOffering.salary || null,
    areas: jobOffering.sectors
      ? jobOffering.sectors.split(",").map((s) => s.trim())
      : [],
    description: jobOffering.description || "",
    url: jobOffering.url || "",
    requirements: jobOffering.extra_data?.requirements || [],
    responsibilities: jobOffering.extra_data?.responsibilities || [],
    post_date: jobOffering.post_date || new Date().toISOString(),
  };
}

export const jobService = {
  async getAll(): Promise<Job[]> {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) => setTimeout(resolve, 300));
      return mockJobs;
    }

    const jobOfferings = await apiCall<JobOfferingResponse[]>(
      API_ENDPOINTS.jobOfferings
    );
    return jobOfferings.map(mapJobOfferingToJob);
  },

  async getById(id: string): Promise<Job> {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) => setTimeout(resolve, 300));
      const job = mockJobs.find((j: Job) => j.id === id);
      if (!job) {
        throw new Error(`Job with id ${id} not found`);
      }
      return job;
    }

    const jobOffering = await apiCall<JobOfferingResponse>(
      API_ENDPOINTS.jobOfferingById(id)
    );
    return mapJobOfferingToJob(jobOffering);
  },

  async searchJobs(query: string, keyword?: string): Promise<Job[]> {
    if (USE_MOCK_DATA) {
      await new Promise((resolve) => setTimeout(resolve, 300));
      return mockJobs.filter((job: Job) => {
        const matchesQuery =
          query === "" ||
          job.title.toLowerCase().includes(query.toLowerCase()) ||
          job.company.toLowerCase().includes(query.toLowerCase());
        return matchesQuery;
      });
    }

    // El backend soporta 'search' (búsqueda general) y 'keyword' (filtro exacto)
    const params = new URLSearchParams();
    if (query) params.append("search", query);
    if (keyword) params.append("keyword", keyword);

    const jobOfferings = await apiCall<JobOfferingResponse[]>(
      `${API_ENDPOINTS.jobOfferings}?${params}`
    );
    return jobOfferings.map(mapJobOfferingToJob);
  },
};
