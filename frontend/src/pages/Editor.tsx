import { useState, useEffect } from 'react'
import { useNavigate, useParams, useLocation } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { ScrollArea } from '@/components/ui/scroll-area'
import { ArrowLeft, Send, FileDown, CheckCircle2, Loader2 } from 'lucide-react'
import TypstRenderer from '@/components/TypstRenderer'
import { cvService, submissionService } from '@/services'
import type { CVResponse } from '@/services'

export default function Editor() {
    const navigate = useNavigate()
    const location = useLocation()
    const { id } = useParams() // This is the CV ID
    const [message, setMessage] = useState('')
    const [cv, setCV] = useState<CVResponse | null>(null)
    const [loading, setLoading] = useState(true)
    const [regenerating, setRegenerating] = useState(false)
    const [submitting, setSubmitting] = useState(false)
    const jobOfferingId = location.state?.jobOfferingId as string | undefined // Get job_offering_id from navigation state
    const [chatHistory, setChatHistory] = useState<Array<{ role: string; content: string }>>([
        {
            role: 'ai',
            content: 'Hi! I can help you customize your CV for this position. What would you like to change?',
        },
    ])

    useEffect(() => {
        async function loadCV() {
            if (!id) return
            try {
                const cvId = parseInt(id)
                const cvData = await cvService.getById(cvId)
                setCV(cvData)
                
                // Load conversation history if exists
                if (cvData.conversation_history && Array.isArray(cvData.conversation_history)) {
                    const history = cvData.conversation_history.map((entry: any) => ({
                        role: entry.role === 'user' ? 'user' : 'ai',
                        content: entry.content || entry.instructions || '',
                    }))
                    setChatHistory([
                        {
                            role: 'ai',
                            content: 'Hi! I can help you customize your CV for this position. What would you like to change?',
                        },
                        ...history
                    ])
                }
            } catch (error) {
                console.error('Failed to load CV:', error)
            } finally {
                setLoading(false)
            }
        }
        loadCV()
    }, [id])

    const handleSendMessage = async () => {
        if (!message.trim() || !cv) return

        const userMessage = { role: 'user', content: message }
        setChatHistory([...chatHistory, userMessage])
        setMessage('')
        setRegenerating(true)

        try {
            const updatedCV = await cvService.regenerate(cv.id, {
                messages: [{
                    role: 'user',
                    content: message,
                    timestamp: new Date().toISOString(),
                }]
            })
            
            setCV(updatedCV)
            setChatHistory([
                ...chatHistory,
                userMessage,
                { role: 'ai', content: 'I\'ve updated your CV based on your request. Please review the changes on the right.' }
            ])
        } catch (error) {
            console.error('Failed to regenerate CV:', error)
            setChatHistory([
                ...chatHistory,
                userMessage,
                { role: 'ai', content: 'Sorry, I encountered an error while updating your CV. Please try again.' }
            ])
        } finally {
            setRegenerating(false)
        }
    }

    const handleSubmit = async () => {
        if (!cv || !jobOfferingId) {
            alert('Error: Missing CV or job information')
            return
        }

        setSubmitting(true)
        try {
            const userId = 1 // TODO: Get from auth context
            
            // Create the application
            const application = await submissionService.create({
                user_id: userId,
                job_offering_id: jobOfferingId,
                status: 'Sent',
                notes: null,
            })
            
            // Update the application with the CV ID
            await submissionService.update(application.id, {
                cv_id: cv.id,
            })
            
            alert('Application submitted successfully!')
            navigate('/submissions')
        } catch (error) {
            console.error('Failed to submit application:', error)
            alert('Failed to submit application. Please try again.')
        } finally {
            setSubmitting(false)
        }
    }

    return (
        <>
            {/* Header */}
            <div className="bg-white dark:bg-gray-950 border-b border-gray-200 dark:border-gray-800 px-6 py-4">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                        <Button variant="ghost" size="icon" onClick={() => navigate(`/jobs/${id}`)}>
                            <ArrowLeft className="h-5 w-5" />
                        </Button>
                        <div>
                            <h1 className="text-xl font-bold text-gray-900 dark:text-white">CV Editor</h1>
                            <p className="text-sm text-muted-foreground">Customize your CV with AI assistance</p>
                        </div>
                    </div>
                    <div className="flex items-center space-x-2">
                        <Button variant="outline">
                            <FileDown className="mr-2 h-4 w-4" />
                            Download PDF
                        </Button>
                        <Button
                            className="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700"
                            onClick={handleSubmit}
                            disabled={submitting || !jobOfferingId}
                        >
                            {submitting ? (
                                <>
                                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                    Submitting...
                                </>
                            ) : (
                                <>
                                    <CheckCircle2 className="mr-2 h-4 w-4" />
                                    Submit Application
                                </>
                            )}
                        </Button>
                    </div>
                </div>
            </div>

            {/* Split View */}
            <div className="flex-1 grid grid-cols-2 gap-0 overflow-hidden">
                {/* Chat Panel */}
                <div className="border-r border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-950 flex flex-col">
                    <div className="p-4 border-b border-gray-200 dark:border-gray-800">
                        <h2 className="font-semibold text-gray-900 dark:text-white">AI Assistant</h2>
                        <p className="text-sm text-muted-foreground">Chat to customize your CV</p>
                    </div>

                    <ScrollArea className="flex-1 p-4">
                        <div className="space-y-4 max-w-2xl">
                            {chatHistory.map((msg, idx) => (
                                <div key={idx} className={`flex items-start gap-3 ${msg.role === 'user' ? 'justify-end' : ''}`}>
                                    {msg.role === 'ai' && (
                                        <div className="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center text-white text-xs font-bold flex-shrink-0">
                                            AI
                                        </div>
                                    )}
                                    <div className={`p-3 rounded-lg max-w-[80%] ${msg.role === 'ai'
                                        ? 'bg-gray-100 dark:bg-gray-800 rounded-tl-none'
                                        : 'bg-blue-600 text-white rounded-tr-none'
                                        }`}>
                                        <p className="text-sm">{msg.content}</p>
                                    </div>
                                    {msg.role === 'user' && (
                                        <div className="h-8 w-8 rounded-full bg-gray-400 flex items-center justify-center text-white text-xs font-bold flex-shrink-0">
                                            Me
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    </ScrollArea>

                    <div className="p-4 border-t border-gray-200 dark:border-gray-800">
                        <div className="flex gap-2">
                            <Textarea
                                placeholder={regenerating ? "Generating..." : "Ask AI to modify your CV..."}
                                className="resize-none"
                                rows={3}
                                value={message}
                                onChange={(e) => setMessage(e.target.value)}
                                onKeyDown={(e) => {
                                    if (e.key === 'Enter' && !e.shiftKey && !regenerating) {
                                        e.preventDefault()
                                        handleSendMessage()
                                    }
                                }}
                                disabled={regenerating}
                            />
                            <Button
                                size="icon"
                                className="h-auto aspect-square"
                                onClick={handleSendMessage}
                                disabled={!message.trim() || regenerating}
                            >
                                <Send className="h-5 w-5" />
                            </Button>
                        </div>
                        <p className="text-xs text-muted-foreground mt-2">
                            Press Enter to send, Shift+Enter for new line
                        </p>
                    </div>
                </div>

                {/* CV Preview Panel with Typst Renderer */}
                <div className="bg-gray-100 dark:bg-gray-900 overflow-y-auto flex items-start justify-center p-8">
                    <div className="w-full max-w-3xl bg-white dark:bg-gray-950 shadow-lg rounded-lg overflow-hidden">
                        {loading ? (
                            <div className="flex items-center justify-center h-96">
                                <p className="text-muted-foreground">Loading CV...</p>
                            </div>
                        ) : cv?.rendered_content ? (
                            <TypstRenderer content={cv.rendered_content} className="p-4" />
                        ) : (
                            <div className="flex items-center justify-center h-96">
                                <p className="text-muted-foreground">No CV content available</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </>
    )
}
