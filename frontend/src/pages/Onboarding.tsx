import { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Badge } from '@/components/ui/badge'
import { Upload, Github, Linkedin, MessageSquare, ArrowRight, CheckCircle2, Loader2, X, AlertCircle } from 'lucide-react'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import type { UploadStates } from '@/utils/profileUtils'
import { getOnboardingProgress } from '@/utils/profileUtils'
import { extractionService } from '@/services'

interface ChatMessage {
    role: 'user' | 'assistant'
    content: string
}

export default function Onboarding() {
    const navigate = useNavigate()
    const location = useLocation()
    const isFirstTime = location.state?.isFirstTime ?? false

    // Upload states
    const [uploadStates, setUploadStates] = useState<UploadStates>({
        cv: { uploaded: false, loading: false, success: false },
        github: { connected: false, loading: false, success: false },
        linkedin: { connected: false, loading: false, success: false },
    })

    // Form data
    const [file, setFile] = useState<File | null>(null)
    const [githubUrl, setGithubUrl] = useState('')
    const [linkedinUrl, setLinkedinUrl] = useState('')

    // Error state
    const [error, setError] = useState<string | null>(null)

    // Chat state
    const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
        {
            role: 'assistant',
            content: "Hi! I can help you build your CV. Tell me about your recent work experience or paste your resume text here.",
        },
    ])
    const [chatInput, setChatInput] = useState('')

    const progress = getOnboardingProgress(uploadStates)

    // CV Upload handler
    const handleCVUpload = async (selectedFile: File) => {
        setFile(selectedFile)
        setError(null)
        setUploadStates(prev => ({
            ...prev,
            cv: { ...prev.cv, loading: true },
        }))

        try {
            // Read file as text (PDF parsing would need a library in production)
            const text = await selectedFile.text()
            
            // Call extraction endpoint
            const userId = 1 // In a real app, get from auth context
            await extractionService.extractProfile(userId, {
                text: text.substring(0, 10000), // Limit text size
                source: 'cv_upload',
            })

            setUploadStates(prev => ({
                ...prev,
                cv: { uploaded: true, loading: false, success: true },
            }))
        } catch (error) {
            console.error('Failed to upload CV:', error)
            setError('Failed to process CV. Make sure the backend is running.')
            setUploadStates(prev => ({
                ...prev,
                cv: { ...prev.cv, loading: false, success: false },
            }))
        }
    }

    // GitHub connect handler
    const handleGitHubConnect = async () => {
        if (!githubUrl) return

        setUploadStates(prev => ({
            ...prev,
            github: { ...prev.github, loading: true },
        }))

        // Simulate connection
        setTimeout(() => {
            setUploadStates(prev => ({
                ...prev,
                github: { connected: true, loading: false, success: true },
            }))
        }, 1500)

        // TODO: Actually connect to backend
        // await fetch('/api/v1/users/1/import/github', { method: 'POST', body: JSON.stringify({ url: githubUrl }) })
    }

    // LinkedIn connect handler
    const handleLinkedInConnect = async () => {
        if (!linkedinUrl) return

        setUploadStates(prev => ({
            ...prev,
            linkedin: { ...prev.linkedin, loading: true },
        }))

        // Simulate connection
        setTimeout(() => {
            setUploadStates(prev => ({
                ...prev,
                linkedin: { connected: true, loading: false, success: true },
            }))
        }, 1500)

        // TODO: Actually connect to backend
        // await fetch('/api/v1/users/1/import/linkedin', { method: 'POST', body: JSON.stringify({ url: linkedinUrl }) })
    }

    // Chat message handler
    const handleSendMessage = async () => {
        if (!chatInput.trim()) return

        const userMessage = chatInput
        setChatInput('')
        setError(null)

        // Add user message
        setChatMessages(prev => [
            ...prev,
            { role: 'user', content: userMessage },
        ])

        try {
            // Call extraction endpoint with chat text
            const userId = 1 // In a real app, get from auth context
            const response = await extractionService.extractProfile(userId, {
                text: userMessage,
                source: 'chat',
            })

            // Add AI response
            setChatMessages(prev => [
                ...prev,
                {
                    role: 'assistant',
                    content: response.message || "Thanks for sharing! I've updated your profile. Is there anything else you'd like to add?",
                },
            ])
        } catch (error) {
            console.error('Failed to process message:', error)
            setError('Failed to process your message. Make sure the backend is running.')
            setChatMessages(prev => [
                ...prev,
                {
                    role: 'assistant',
                    content: "I'm having trouble connecting to the server. Please make sure the backend is running.",
                },
            ])
        }
    }

    const handleContinue = () => {
        navigate('/dashboard')
    }

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto">
                {/* Header */}
                <div className="text-center mb-8">
                    <div className="flex items-center justify-between mb-4">
                        <div className="flex-1" />
                        <h1 className="text-4xl font-extrabold text-gray-900 dark:text-white tracking-tight sm:text-5xl">
                            Build Your Profile
                        </h1>
                        <div className="flex-1 flex justify-end">
                            <Button
                                variant="ghost"
                                size="icon"
                                onClick={() => navigate('/dashboard')}
                                className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                            >
                                <X className="h-5 w-5" />
                            </Button>
                        </div>
                    </div>
                    <p className="text-lg text-gray-600 dark:text-gray-400">
                        {isFirstTime
                            ? "Welcome! Import your professional information to get started."
                            : "Update your professional information and enhance your profile."
                        }
                    </p>
                    {error && (
                        <Alert className="mt-4 bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-900">
                            <AlertCircle className="h-4 w-4 text-red-600 dark:text-red-400" />
                            <AlertTitle>Error</AlertTitle>
                            <AlertDescription>{error}</AlertDescription>
                        </Alert>
                    )}
                    {progress.hasAnyData && (
                        <div className="mt-4">
                            <Badge variant="secondary" className="gap-2">
                                <CheckCircle2 className="h-4 w-4" />
                                {progress.completed} of {progress.total} sources connected
                            </Badge>
                        </div>
                    )}
                </div>

                <Tabs defaultValue="upload" className="w-full">
                    <TabsList className="grid w-full grid-cols-3 mb-8 h-auto p-1 bg-gray-200 dark:bg-gray-800 rounded-xl">
                        <TabsTrigger value="upload" className="py-3 rounded-lg data-[state=active]:bg-white dark:data-[state=active]:bg-gray-950 data-[state=active]:shadow-sm transition-all">
                            <Upload className="mr-2 h-5 w-5" />
                            Upload CV
                            {uploadStates.cv.success && <CheckCircle2 className="ml-2 h-4 w-4 text-green-600" />}
                        </TabsTrigger>
                        <TabsTrigger value="import" className="py-3 rounded-lg data-[state=active]:bg-white dark:data-[state=active]:bg-gray-950 data-[state=active]:shadow-sm transition-all">
                            <Github className="mr-2 h-5 w-5" />
                            Import Links
                            {(uploadStates.github.success || uploadStates.linkedin.success) && <CheckCircle2 className="ml-2 h-4 w-4 text-green-600" />}
                        </TabsTrigger>
                        <TabsTrigger value="chat" className="py-3 rounded-lg data-[state=active]:bg-white dark:data-[state=active]:bg-gray-950 data-[state=active]:shadow-sm transition-all">
                            <MessageSquare className="mr-2 h-5 w-5" />
                            AI Assistant
                        </TabsTrigger>
                    </TabsList>

                    {/* Upload CV Tab */}
                    <TabsContent value="upload">
                        <Card>
                            <CardHeader>
                                <CardTitle>Upload your existing CV</CardTitle>
                                <CardDescription>
                                    We'll parse your PDF to extract your skills and experience.
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-xl p-12 text-center hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors cursor-pointer relative">
                                    <input
                                        type="file"
                                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                                        accept=".pdf"
                                        onChange={(e) => {
                                            const selectedFile = e.target.files?.[0]
                                            if (selectedFile) handleCVUpload(selectedFile)
                                        }}
                                        disabled={uploadStates.cv.loading}
                                    />
                                    <div className="flex flex-col items-center justify-center space-y-4">
                                        <div className="p-4 bg-blue-100 dark:bg-blue-900/30 rounded-full">
                                            {uploadStates.cv.loading ? (
                                                <Loader2 className="h-8 w-8 text-blue-600 dark:text-blue-400 animate-spin" />
                                            ) : uploadStates.cv.success ? (
                                                <CheckCircle2 className="h-8 w-8 text-green-600 dark:text-green-400" />
                                            ) : (
                                                <Upload className="h-8 w-8 text-blue-600 dark:text-blue-400" />
                                            )}
                                        </div>
                                        <div className="space-y-1">
                                            <p className="text-lg font-medium text-gray-900 dark:text-white">
                                                {uploadStates.cv.loading
                                                    ? "Uploading..."
                                                    : file
                                                        ? file.name
                                                        : "Drop your PDF here or click to upload"}
                                            </p>
                                            <p className="text-sm text-gray-500 dark:text-gray-400">
                                                PDF files up to 10MB
                                            </p>
                                        </div>
                                    </div>
                                </div>
                                {uploadStates.cv.success && (
                                    <Alert className="bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-900">
                                        <CheckCircle2 className="h-4 w-4 text-green-600 dark:text-green-400" />
                                        <AlertTitle>Success!</AlertTitle>
                                        <AlertDescription>
                                            Your CV has been uploaded successfully and is being processed.
                                        </AlertDescription>
                                    </Alert>
                                )}
                            </CardContent>
                        </Card>
                    </TabsContent>

                    {/* Import Links Tab */}
                    <TabsContent value="import">
                        <Card>
                            <CardHeader>
                                <CardTitle>Import from Social Profiles</CardTitle>
                                <CardDescription>
                                    Connect your professional accounts to auto-fill your profile.
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-6">
                                {/* GitHub */}
                                <div className="space-y-3">
                                    <Label htmlFor="github">GitHub Profile</Label>
                                    <div className="flex gap-2">
                                        <div className="relative flex-1">
                                            <Github className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                                            <Input
                                                id="github"
                                                placeholder="https://github.com/username"
                                                className="pl-10"
                                                value={githubUrl}
                                                onChange={(e) => setGithubUrl(e.target.value)}
                                                disabled={uploadStates.github.loading || uploadStates.github.success}
                                            />
                                        </div>
                                        <Button
                                            onClick={handleGitHubConnect}
                                            disabled={!githubUrl || uploadStates.github.loading || uploadStates.github.success}
                                        >
                                            {uploadStates.github.loading ? (
                                                <Loader2 className="h-4 w-4 animate-spin" />
                                            ) : uploadStates.github.success ? (
                                                <>
                                                    <CheckCircle2 className="mr-2 h-4 w-4" />
                                                    Connected
                                                </>
                                            ) : (
                                                'Connect'
                                            )}
                                        </Button>
                                    </div>
                                    {uploadStates.github.success && (
                                        <Alert className="bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-900">
                                            <CheckCircle2 className="h-4 w-4 text-green-600 dark:text-green-400" />
                                            <AlertDescription>
                                                GitHub profile connected successfully!
                                            </AlertDescription>
                                        </Alert>
                                    )}
                                </div>

                                {/* LinkedIn */}
                                <div className="space-y-3">
                                    <Label htmlFor="linkedin">LinkedIn Profile</Label>
                                    <div className="flex gap-2">
                                        <div className="relative flex-1">
                                            <Linkedin className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                                            <Input
                                                id="linkedin"
                                                placeholder="https://linkedin.com/in/username"
                                                className="pl-10"
                                                value={linkedinUrl}
                                                onChange={(e) => setLinkedinUrl(e.target.value)}
                                                disabled={uploadStates.linkedin.loading || uploadStates.linkedin.success}
                                            />
                                        </div>
                                        <Button
                                            onClick={handleLinkedInConnect}
                                            disabled={!linkedinUrl || uploadStates.linkedin.loading || uploadStates.linkedin.success}
                                        >
                                            {uploadStates.linkedin.loading ? (
                                                <Loader2 className="h-4 w-4 animate-spin" />
                                            ) : uploadStates.linkedin.success ? (
                                                <>
                                                    <CheckCircle2 className="mr-2 h-4 w-4" />
                                                    Connected
                                                </>
                                            ) : (
                                                'Connect'
                                            )}
                                        </Button>
                                    </div>
                                    {uploadStates.linkedin.success && (
                                        <Alert className="bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-900">
                                            <CheckCircle2 className="h-4 w-4 text-green-600 dark:text-green-400" />
                                            <AlertDescription>
                                                LinkedIn profile connected successfully!
                                            </AlertDescription>
                                        </Alert>
                                    )}
                                </div>
                            </CardContent>
                        </Card>
                    </TabsContent>

                    {/* AI Chat Tab - Always Open */}
                    <TabsContent value="chat">
                        <Card>
                            <CardHeader>
                                <CardTitle>Chat with AI Assistant</CardTitle>
                                <CardDescription>
                                    Tell us about your experience and we'll build your profile.
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                {/* Chat messages */}
                                <div className="bg-gray-100 dark:bg-gray-800 rounded-lg p-4 h-96 overflow-y-auto space-y-4">
                                    {chatMessages.map((message, idx) => (
                                        <div
                                            key={idx}
                                            className={`flex items-start gap-3 ${message.role === 'user' ? 'justify-end' : ''
                                                }`}
                                        >
                                            {message.role === 'assistant' && (
                                                <div className="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center text-white text-xs font-bold shrink-0">
                                                    AI
                                                </div>
                                            )}
                                            <div
                                                className={`p-3 rounded-lg shadow-sm max-w-[80%] ${message.role === 'assistant'
                                                    ? 'bg-white dark:bg-gray-900 rounded-tl-none'
                                                    : 'bg-blue-600 text-white rounded-tr-none'
                                                    }`}
                                            >
                                                <p className="text-sm">{message.content}</p>
                                            </div>
                                            {message.role === 'user' && (
                                                <div className="h-8 w-8 rounded-full bg-gray-400 flex items-center justify-center text-white text-xs font-bold shrink-0">
                                                    You
                                                </div>
                                            )}
                                        </div>
                                    ))}
                                </div>
                                {/* Chat input */}
                                <div className="flex gap-2">
                                    <Textarea
                                        placeholder="Type your message..."
                                        className="min-h-[80px] resize-none"
                                        value={chatInput}
                                        onChange={(e) => setChatInput(e.target.value)}
                                        onKeyDown={(e) => {
                                            if (e.key === 'Enter' && !e.shiftKey) {
                                                e.preventDefault()
                                                handleSendMessage()
                                            }
                                        }}
                                    />
                                    <Button
                                        className="h-auto"
                                        size="icon"
                                        onClick={handleSendMessage}
                                        disabled={!chatInput.trim()}
                                    >
                                        <ArrowRight className="h-5 w-5" />
                                    </Button>
                                </div>
                            </CardContent>
                        </Card>
                    </TabsContent>
                </Tabs>

                {/* Navigation Button - Outside of tabs */}
                <div className="mt-8 flex justify-center">
                    <Button
                        size="lg"
                        onClick={handleContinue}
                        className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white shadow-lg px-8"
                    >
                        {progress.hasAnyData ? 'Continue to Dashboard' : 'Skip for Now'}
                        <ArrowRight className="ml-2 h-5 w-5" />
                    </Button>
                </div>
            </div>
        </div>
    )
}
