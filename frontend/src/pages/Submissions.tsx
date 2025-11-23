import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { PlusCircle, FileText, ExternalLink, Download } from 'lucide-react'
import { submissionService, type Submission } from '@/services'

const getStatusColor = (status: Submission['status']) => {
    switch (status) {
        case 'Under Review':
            return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
        case 'Interview Scheduled':
            return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
        case 'Rejected':
            return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
        case 'Accepted':
            return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
        default:
            return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
    }
}

export default function Submissions() {
    const [submissions, setSubmissions] = useState<Submission[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function loadSubmissions() {
            try {
                // In a real app, get user ID from auth context
                const userId = 1
                const data = await submissionService.getUserSubmissions(userId)
                setSubmissions(data)
            } catch (error) {
                console.error('Failed to load submissions:', error)
            } finally {
                setLoading(false)
            }
        }
        loadSubmissions()
    }, [])

    if (loading) {
        return <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">Loading...</div>
    }

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            {/* Header */}
            <div className="bg-white dark:bg-gray-950 border-b border-gray-200 dark:border-gray-800">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900 dark:text-white tracking-tight">
                                My Applications
                            </h1>
                            <p className="mt-2 text-gray-600 dark:text-gray-400">
                                Track and manage your job applications
                            </p>
                        </div>
                        <Button asChild className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700">
                            <Link to="/jobs">
                                <PlusCircle className="mr-2 h-4 w-4" />
                                New Application
                            </Link>
                        </Button>
                    </div>
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <Card>
                        <CardHeader className="pb-2">
                            <CardDescription>Total Applications</CardDescription>
                            <CardTitle className="text-3xl">{submissions.length}</CardTitle>
                        </CardHeader>
                    </Card>
                    <Card>
                        <CardHeader className="pb-2">
                            <CardDescription>Under Review</CardDescription>
                            <CardTitle className="text-3xl">
                                {submissions.filter((s: Submission) => s.status === 'Under Review').length}
                            </CardTitle>
                        </CardHeader>
                    </Card>
                    <Card>
                        <CardHeader className="pb-2">
                            <CardDescription>Interviews</CardDescription>
                            <CardTitle className="text-3xl">
                                {submissions.filter((s: Submission) => s.status === 'Interview Scheduled').length}
                            </CardTitle>
                        </CardHeader>
                    </Card>
                    <Card>
                        <CardHeader className="pb-2">
                            <CardDescription>Success Rate</CardDescription>
                            <CardTitle className="text-3xl">33%</CardTitle>
                        </CardHeader>
                    </Card>
                </div>

                {/* Submissions Table */}
                <Card>
                    <CardHeader>
                        <CardTitle>Application History</CardTitle>
                        <CardDescription>View all your submitted applications</CardDescription>
                    </CardHeader>
                    <CardContent>
                        {submissions.length === 0 ? (
                            <div className="text-center py-12">
                                <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                                <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                                    No applications yet
                                </h3>
                                <p className="text-sm text-muted-foreground mb-6">
                                    Start by browsing job opportunities and submitting your first application.
                                </p>
                                <Button asChild>
                                    <Link to="/jobs">Browse Jobs</Link>
                                </Button>
                            </div>
                        ) : (
                            <div className="overflow-x-auto">
                                <Table>
                                    <TableHeader>
                                        <TableRow>
                                            <TableHead>Job Title</TableHead>
                                            <TableHead>Company</TableHead>
                                            <TableHead>Submitted Date</TableHead>
                                            <TableHead>Status</TableHead>
                                            <TableHead className="text-right">Actions</TableHead>
                                        </TableRow>
                                    </TableHeader>
                                    <TableBody>
                                        {submissions.map((submission: Submission) => (
                                            <TableRow key={submission.id}>
                                                <TableCell className="font-medium">{submission.job_title}</TableCell>
                                                <TableCell>{submission.company}</TableCell>
                                                <TableCell>{new Date(submission.submitted_date).toLocaleDateString()}</TableCell>
                                                <TableCell>
                                                    <Badge variant="secondary" className={getStatusColor(submission.status)}>
                                                        {submission.status}
                                                    </Badge>
                                                </TableCell>
                                                <TableCell className="text-right space-x-2">
                                                    <Button variant="ghost" size="sm" asChild>
                                                        <Link to={`/jobs/${submission.id}`}>
                                                            <ExternalLink className="h-4 w-4" />
                                                        </Link>
                                                    </Button>
                                                    <Button variant="ghost" size="sm">
                                                        <Download className="h-4 w-4" />
                                                    </Button>
                                                </TableCell>
                                            </TableRow>
                                        ))}
                                    </TableBody>
                                </Table>
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
