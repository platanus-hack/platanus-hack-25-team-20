import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { PlusCircle, User, Briefcase, Languages, DollarSign, Calendar, Edit } from 'lucide-react'
import { userService, skillsService, projectService, apiCall, API_ENDPOINTS, type UserResponse, type UserSkillsResponse, type ProjectResponse, type UserProfileResponse } from '@/services'
import { mockUserProfile } from '@/services/mockData'
import { hasProfileData } from '@/utils/profileUtils'

export default function Dashboard() {
    const navigate = useNavigate()
    const [user, setUser] = useState<UserResponse | null>(null)
    const [userProfile, setUserProfile] = useState<UserProfileResponse | null>(null)
    const [skills, setSkills] = useState<UserSkillsResponse[]>([])
    const [projects, setProjects] = useState<ProjectResponse[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        async function loadData() {
            try {
                // In a real app, get user ID from auth context
                const userId = 1
                const [userData, skillsData, projectsData, profileData] = await Promise.all([
                    userService.getById(userId),
                    skillsService.getByUserId(userId).catch(() => []),
                    projectService.getUserProjects(userId).catch(() => []),
                    apiCall<UserProfileResponse>(API_ENDPOINTS.userProfile(userId)).catch(() => null),
                ])
                setUser(userData)
                setSkills(skillsData)
                setProjects(projectsData)
                setUserProfile(profileData)
            } catch (error) {
                console.error('Failed to load dashboard data:', error)
                setError('Failed to load your profile data. Please check if the backend is running.')
            } finally {
                setLoading(false)
            }
        }
        loadData()
    }, [])

    // Redirect first-time users to onboarding (only if no error occurred)
    useEffect(() => {
        if (!loading && !error && !hasProfileData(skills, projects)) {
            navigate('/onboarding', { state: { isFirstTime: true } })
        }
    }, [loading, error, skills, projects, navigate])

    if (loading) {
        return <div className="p-8">Loading...</div>
    }

    // Handle error state
    if (error) {
        return (
            <div className="p-8">
                <Card className="border-red-200 dark:border-red-900">
                    <CardHeader>
                        <CardTitle className="text-red-600 dark:text-red-400">Connection Error</CardTitle>
                        <CardDescription>{error}</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                            Make sure the backend server is running at http://localhost:8000
                        </p>
                        <div className="flex gap-2">
                            <Button onClick={() => window.location.reload()}>
                                Try Again
                            </Button>
                            <Button variant="outline" asChild>
                                <Link to="/onboarding">
                                    Go to Onboarding
                                </Link>
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            </div>
        )
    }

    // Handle case where user has no data yet (redirects to onboarding)
    if (!user) {
        return <div className="p-8">Loading profile...</div>
    }

    // Ensure skills is always an array
    const skillsArray = Array.isArray(skills) ? skills : []
    
    // Extract display data from skills list - filter by type
    const devSkills = skillsArray.filter(s => s.skill_type === 'dev-skill').map(s => s.skill_text)
    const allSkills = devSkills.slice(0, 10)
    
    // Extract experiences
    const experiences = skillsArray
        .filter(s => s.skill_type === 'experience')
        .map(s => {
            // Try to parse experience text into company/position/period
            const text = s.skill_text
            return { company: '', position: text, period: '' }
        })

    // Extract languages from extra skills
    const languageSkill = skillsArray.find(s => s.skill_type === 'extra' && s.skill_text.toLowerCase().includes('english'))
    const languages = languageSkill ? languageSkill.skill_text.split(',').map(l => l.trim()) : mockUserProfile.languages

    // Use real data from backend, no fallbacks
    const yearsExperience = userProfile?.years_of_experience ?? null
    const estimatedSalary = userProfile?.salary_range || 'No se sabe'
    const lastPosition = projects?.[0]?.target_role ?? experiences[0]?.position ?? 'Full Stack Developer'
    const experience = experiences.length > 0 ? experiences : mockUserProfile.experience

    return (
        <div className="p-8">
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white">Dashboard</h2>
                    <p className="text-muted-foreground mt-1">Manage your CVs and job applications.</p>
                </div>
                <div className="flex gap-2">
                    <Button asChild variant="outline">
                        <Link to="/onboarding">
                            <Edit className="mr-2 h-4 w-4" />
                            Build Your Profile
                        </Link>
                    </Button>
                    <Button asChild className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white shadow-md">
                        <Link to="/jobs">
                            <PlusCircle className="mr-2 h-4 w-4" />
                            New Application
                        </Link>
                    </Button>
                </div>
            </div>

            {/* User Profile Section */}
            <div className="mb-8">
                <Card>
                    <CardHeader>
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-4">
                                <div className="h-16 w-16 rounded-full bg-gradient-to-r from-blue-600 to-indigo-600 flex items-center justify-center text-white text-2xl font-bold">
                                    {user?.full_name?.split(' ').map((n: string) => n[0]).join('') ?? 'U'}
                                </div>
                                <div>
                                    <CardTitle className="text-2xl">{user?.full_name ?? 'User'}</CardTitle>
                                    <CardDescription className="text-base">{user?.email ?? ''}</CardDescription>
                                </div>
                            </div>
                            <Button variant="outline" asChild>
                                <Link to="/onboarding">
                                    <Edit className="mr-2 h-4 w-4" />
                                    Edit Profile
                                </Link>
                            </Button>
                        </div>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        {/* Quick Stats */}
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            <div className="space-y-1">
                                <div className="flex items-center text-sm text-muted-foreground">
                                    <Briefcase className="mr-2 h-4 w-4" />
                                    Current Role
                                </div>
                                <p className="font-medium text-gray-900 dark:text-white">{lastPosition}</p>
                            </div>
                            <div className="space-y-1">
                                <div className="flex items-center text-sm text-muted-foreground">
                                    <Calendar className="mr-2 h-4 w-4" />
                                    Experience
                                </div>
                                <p className="font-medium text-gray-900 dark:text-white">
                                    {yearsExperience !== null ? `${yearsExperience} years` : 'No se sabe'}
                                </p>
                            </div>
                            <div className="space-y-1">
                                <div className="flex items-center text-sm text-muted-foreground">
                                    <DollarSign className="mr-2 h-4 w-4" />
                                    Salary Range
                                </div>
                                <p className="font-medium text-gray-900 dark:text-white">{estimatedSalary}</p>
                            </div>
                            <div className="space-y-1">
                                <div className="flex items-center text-sm text-muted-foreground">
                                    <Languages className="mr-2 h-4 w-4" />
                                    Languages
                                </div>
                                <p className="font-medium text-gray-900 dark:text-white">{languages.length}</p>
                            </div>
                        </div>

                        <Separator />

                        {/* Skills */}
                        <div>
                            <h3 className="font-semibold text-gray-900 dark:text-white mb-3 flex items-center">
                                <User className="mr-2 h-4 w-4" />
                                Skills
                            </h3>
                            <div className="flex flex-wrap gap-2">
                                {allSkills.map((skill: string) => (
                                    <Badge key={skill} variant="secondary" className="text-xs">
                                        {skill}
                                    </Badge>
                                ))}
                            </div>
                        </div>

                        <Separator />

                        {/* Languages */}
                        <div>
                            <h3 className="font-semibold text-gray-900 dark:text-white mb-3 flex items-center">
                                <Languages className="mr-2 h-4 w-4" />
                                Languages
                            </h3>
                            <div className="flex flex-wrap gap-2">
                                {languages.map((language: string) => (
                                    <Badge key={language} variant="outline" className="text-xs">
                                        {language}
                                    </Badge>
                                ))}
                            </div>
                        </div>

                        <Separator />

                        {/* Recent Experience */}
                        <div>
                            <h3 className="font-semibold text-gray-900 dark:text-white mb-3 flex items-center">
                                <Briefcase className="mr-2 h-4 w-4" />
                                Recent Experience
                            </h3>
                            <div className="space-y-3">
                                {experience.map((exp: typeof experience[0], idx: number) => (
                                    <div key={idx} className="flex justify-between items-start">
                                        <div>
                                            <p className="font-medium text-gray-900 dark:text-white">{exp.position}</p>
                                            <p className="text-sm text-muted-foreground">{exp.company}</p>
                                        </div>
                                        <span className="text-sm text-muted-foreground">{exp.period}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
