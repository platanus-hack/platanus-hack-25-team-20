// ============================================================================
// USER TYPES
// ============================================================================

export interface UserCreate {
  email: string;
  password: string;
  full_name: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface UserResponse {
  id: number;
  email: string;
  full_name: string;
  created_at: string;
  updated_at: string;
}

export interface UserUpdate {
  full_name?: string | null;
  password?: string | null;
}

// ============================================================================
// USER PROFILE TYPES
// ============================================================================

export interface UserProfileCreate {
  current_role?: string | null;
  years_of_experience?: number | null;
  salary_range?: string | null;
  spoken_languages?: string[];
}

export interface UserProfileResponse {
  id: number;
  user_id: number;
  current_role: string | null;
  years_of_experience: number | null;
  salary_range: string | null;
  spoken_languages: string[];
  created_at: string;
  updated_at: string;
}

export interface UserProfileUpdate {
  current_role?: string | null;
  years_of_experience?: number | null;
  salary_range?: string | null;
  spoken_languages?: string[] | null;
}

// ============================================================================
// PROJECT TYPES
// ============================================================================

export interface ProjectCreate {
  name: string;
  target_role?: string | null;
  cv_style?: string | null;
  preferences?: Record<string, unknown> | null;
}

export interface ProjectResponse {
  id: number;
  user_id: number;
  name: string;
  target_role: string | null;
  cv_style: string | null;
  preferences: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
}

export interface ProjectUpdate {
  name?: string | null;
  target_role?: string | null;
  cv_style?: string | null;
  preferences?: Record<string, unknown> | null;
}

// ============================================================================
// USER SKILLS TYPES
// ============================================================================

export type SkillType = "experience" | "dev-skill" | "certificate" | "extra";

export interface UserSkillsCreate {
  skill_text: string;
  skill_type: SkillType;
  raw_input?: string | null;
  source?: string | null;
}

export interface UserSkillsResponse {
  id: number;
  user_id: number;
  skill_text: string;
  skill_type: SkillType;
  raw_input: string | null;
  source: string | null;
  created_at: string;
  updated_at: string;
}

export interface UserSkillsUpdate {
  skill_text?: string | null;
  skill_type?: SkillType | null;
  raw_input?: string | null;
  source?: string | null;
}

export interface UserSkillsGroupedResponse {
  experience: UserSkillsResponse[];
  dev_skills: UserSkillsResponse[];
  certificates: UserSkillsResponse[];
  extra: UserSkillsResponse[];
}

// ============================================================================
// JOB OFFERING TYPES
// ============================================================================

export interface JobOfferingExtraData {
  requirements?: string[];
  responsibilities?: string[];
  [key: string]: unknown;
}

export interface JobOfferingCreate {
  id: string;
  keyword: string;
  company_name?: string | null;
  description?: string | null;
  url?: string | null;
  salary?: string | null;
  role_name?: string | null;
  location?: string | null;
  work_mode?: string | null;
  type?: string | null;
  post_date?: string | null;
  last_updated?: string | null;
  sectors?: string | null;
  extra_data?: JobOfferingExtraData | null;
  uid?: string | null;
  api_url?: string | null;
}

export interface JobOfferingResponse {
  id: string;
  keyword: string;
  company_name: string | null;
  description: string | null;
  url: string | null;
  salary: string | null;
  role_name: string | null;
  location: string | null;
  work_mode: string | null;
  type: string | null;
  post_date: string | null;
  last_updated: string | null;
  sectors: string | null;
  extra_data: JobOfferingExtraData | null;
  uid: string | null;
  created_at: string;
  updated_at: string;
  api_url: string | null;
}

export interface JobOfferingUpdate {
  keyword?: string | null;
  company_name?: string | null;
  description?: string | null;
  url?: string | null;
  salary?: string | null;
  role_name?: string | null;
  location?: string | null;
  work_mode?: string | null;
  type?: string | null;
  post_date?: string | null;
  last_updated?: string | null;
  sectors?: string | null;
  extra_data?: JobOfferingExtraData | null;
  uid?: string | null;
  api_url?: string | null;
}

// Frontend-friendly job type for display (maps from JobOfferingResponse)
export interface Job {
  id: string;
  title: string; // maps to role_name
  company: string; // maps to company_name
  location: string | null;
  type: string | null; // maps to work_mode
  salary: string | null;
  areas: string[]; // derived from sectors or extra_data
  description: string;
  url: string;
  requirements?: string[];
  responsibilities?: string[];
  post_date: string;
}

// ============================================================================
// APPLICATION TYPES (formerly Submission)
// ============================================================================

export interface ApplicationCreate {
  user_id: number;
  job_offering_id: string;
  status?: string;
  notes?: string | null;
}

export interface ApplicationResponse {
  id: number;
  user_id: number;
  job_offering_id: string;
  cv_id: number | null;
  status: string;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface ApplicationUpdate {
  status?: string | null;
  notes?: string | null;
  cv_id?: number | null;
}

// Legacy alias for backward compatibility
export type Submission = ApplicationResponse;
export type SubmissionCreate = ApplicationCreate;
export type SubmissionUpdate = ApplicationUpdate;

// ============================================================================
// CV TYPES
// ============================================================================

export interface ChatMessage {
  role: string; // "user" or "assistant"
  content: string;
  timestamp?: string | null;
}

export interface CVCreate {
  project_id: number;
  template_id: number;
  base_cv_id?: number | null;
  messages?: ChatMessage[];
}

export interface CVResponse {
  id: number;
  project_id: number;
  template_id: number;
  base_cv_id: number | null;
  content: Record<string, unknown>;
  rendered_content: string | null;
  compiled_path: string | null;
  conversation_history: Record<string, unknown>[] | null;
  created_at: string;
  updated_at: string;
}

export interface CVUpdate {
  content?: Record<string, unknown> | null;
  messages?: ChatMessage[] | null;
}

export interface CVRegenerateRequest {
  messages: ChatMessage[];
}

// ============================================================================
// TEMPLATE TYPES
// ============================================================================

export interface TemplateResponse {
  id: number;
  name: string;
  description: string | null;
  template_type: string;
  style: string | null;
  created_at: string;
}

export interface TemplateDetail extends TemplateResponse {
  template_content: string;
}

// ============================================================================
// EXTRACTION TYPES
// ============================================================================

export interface ExtractProfileRequest {
  text: string;
  source?: string;
}

export interface ExtractProfileResponse {
  message: string;
  profile_updated: boolean;
  profile_created: boolean;
  skills_added: number;
  details: string[];
}
