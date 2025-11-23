import type { UserSkillsResponse, ProjectResponse } from '@/services/types'

/**
 * Checks if user has any profile data (skills or projects)
 */
export const hasProfileData = (
    skills: UserSkillsResponse[] | null | undefined,
    projects: ProjectResponse[] | null | undefined
): boolean => {
    const hasSkills = skills != null && skills.length > 0
    const hasProjects = projects != null && projects.length > 0
    return hasSkills || hasProjects
}

/**
 * Calculates onboarding progress based on upload states
 */
export interface UploadStates {
    cv: { uploaded: boolean; loading: boolean; success: boolean }
    github: { connected: boolean; loading: boolean; success: boolean }
    linkedin: { connected: boolean; loading: boolean; success: boolean }
}

export const getOnboardingProgress = (uploadStates: UploadStates) => {
    const completed = [
        uploadStates.cv.success,
        uploadStates.github.success,
        uploadStates.linkedin.success,
    ].filter(Boolean).length

    return {
        completed,
        total: 3,
        hasAnyData: completed > 0,
        percentage: Math.round((completed / 3) * 100),
    }
}

/**
 * Checks if user is visiting for the first time (no profile data)
 */
export const isFirstTimeUser = (
    skills: UserSkillsResponse | null | undefined,
    projects: ProjectResponse[] | null | undefined
): boolean => {
    return !hasProfileData(skills, projects)
}
