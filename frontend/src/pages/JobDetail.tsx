import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { ArrowLeft, MapPin, Clock, DollarSign, Briefcase, Edit, Send, FileDown } from 'lucide-react'
import { jobService, type Job } from '@/services'

export default function JobDetail() {
    const navigate = useNavigate()
    const { id } = useParams()
    const [job, setJob] = useState<Job | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function loadJob() {
            if (!id) return
            try {
                const data = await jobService.getById(id)
                setJob(data)
            } catch (error) {
                console.error('Failed to load job:', error)
            } finally {
                setLoading(false)
            }
        }
        loadJob()
    }, [id])

    if (loading) {
        return <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">Loading...</div>
    }

    if (!job) {
        return <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">Job not found</div>
    }

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            {/* Header */}
            <div className="bg-white dark:bg-gray-950 border-b border-gray-200 dark:border-gray-800">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <Button variant="ghost" onClick={() => navigate('/jobs')} className="mb-4">
                        <ArrowLeft className="mr-2 h-4 w-4" />
                        Back to Jobs
                    </Button>
                    <div className="flex items-start justify-between">
                        <div className="space-y-2">
                            <h1 className="text-3xl font-bold text-gray-900 dark:text-white tracking-tight">
                                {job.title}
                            </h1>
                            <p className="text-xl text-gray-600 dark:text-gray-400">{job.company}</p>
                            <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                                <div className="flex items-center">
                                    <MapPin className="mr-1.5 h-4 w-4" />
                                    {job.location}
                                </div>
                                <div className="flex items-center">
                                    <Clock className="mr-1.5 h-4 w-4" />
                                    {job.type}
                                </div>
                                <div className="flex items-center">
                                    <DollarSign className="mr-1.5 h-4 w-4" />
                                    {job.salary}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Job Details */}
                    <div className="lg:col-span-2 space-y-6">
                        <Card>
                            <CardHeader>
                                <CardTitle>About the Role</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <p className="text-gray-600 dark:text-gray-400">{job.description}</p>

                                <div>
                                    <h3 className="font-semibold text-gray-900 dark:text-white mb-3">Requirements</h3>
                                    <ul className="space-y-2">
                                        {job.requirements?.map((req: string, i: number) => (
                                            <li key={i} className="flex items-start">
                                                <span className="mr-2 text-blue-600">•</span>
                                                <span className="text-gray-600 dark:text-gray-400">{req}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </div>

                                <div>
                                    <h3 className="font-semibold text-gray-900 dark:text-white mb-3">Responsibilities</h3>
                                    <ul className="space-y-2">
                                        {job.responsibilities?.map((resp: string, i: number) => (
                                            <li key={i} className="flex items-start">
                                                <span className="mr-2 text-blue-600">•</span>
                                                <span className="text-gray-600 dark:text-gray-400">{resp}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </div>

                                <div className="flex flex-wrap gap-2 pt-4">
                                    {job.areas.map(area => (
                                        <Badge key={area} variant="secondary">
                                            {area}
                                        </Badge>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>
                    </div>

                    {/* CV Preview Sidebar */}
                    <div className="lg:col-span-1">
                        <div className="sticky top-4 space-y-4">
                            <Card className="border-2 border-blue-200 dark:border-blue-900">
                                <CardHeader className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950 dark:to-indigo-950">
                                    <CardTitle className="flex items-center">
                                        <Briefcase className="mr-2 h-5 w-5 text-blue-600" />
                                        Tailored CV Preview
                                    </CardTitle>
                                    <CardDescription>
                                        AI-generated CV optimized for this role
                                    </CardDescription>
                                </CardHeader>
                                <CardContent className="pt-6 space-y-4">
                                    <div className="bg-white dark:bg-gray-950 border border-gray-200 dark:border-gray-800 rounded-lg p-4 h-64 overflow-y-auto">
                                        <div className="space-y-3 text-sm">
                                            <div>
                                                <p className="font-bold text-gray-900 dark:text-white">John Doe</p>
                                                <p className="text-xs text-muted-foreground">Full Stack Developer</p>
                                            </div>
                                            <Separator />
                                            <div>
                                                <p className="font-semibold text-gray-900 dark:text-white mb-1">Summary</p>
                                                <p className="text-xs text-gray-600 dark:text-gray-400">
                                                    Experienced developer with 5+ years building scalable applications...
                                                </p>
                                            </div>
                                            <div>
                                                <p className="font-semibold text-gray-900 dark:text-white mb-1">Skills</p>
                                                <p className="text-xs text-gray-600 dark:text-gray-400">
                                                    React, Node.js, PostgreSQL, AWS...
                                                </p>
                                            </div>
                                        </div>
                                    </div>

                                    <div className="space-y-2">
                                        <Button
                                            className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"
                                            onClick={() => navigate(`/editor/${id}`)}
                                        >
                                            <Edit className="mr-2 h-4 w-4" />
                                            Customize CV
                                        </Button>
                                        <div className="grid grid-cols-2 gap-2">
                                            <Button variant="outline" size="sm">
                                                <FileDown className="mr-2 h-4 w-4" />
                                                Download
                                            </Button>
                                            <Button variant="outline" size="sm">
                                                <Send className="mr-2 h-4 w-4" />
                                                Submit
                                            </Button>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
