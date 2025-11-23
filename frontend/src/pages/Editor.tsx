import { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { ScrollArea } from '@/components/ui/scroll-area'
import { ArrowLeft, Send, FileDown, CheckCircle2 } from 'lucide-react'
import TypstRenderer from '@/components/TypstRenderer'
import renderedTestTyp from '@/media/rendered_test.typ?raw'

export default function Editor() {
    const navigate = useNavigate()
    const { id } = useParams()
    const [message, setMessage] = useState('')
    const [typstContent] = useState(renderedTestTyp)
    const [chatHistory, setChatHistory] = useState([
        {
            role: 'ai',
            content: 'Hi! I can help you customize your CV for this position. What would you like to change?',
        },
    ])

    const handleSendMessage = () => {
        if (!message.trim()) return

        setChatHistory([
            ...chatHistory,
            { role: 'user', content: message },
            { role: 'ai', content: 'I\'ve updated your CV based on your request. Please review the changes on the right.' },
        ])
        setMessage('')
    }

    const handleSubmit = () => {
        // TODO: Implement submission logic
        alert('CV submitted successfully!')
        navigate('/submissions')
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
                        >
                            <CheckCircle2 className="mr-2 h-4 w-4" />
                            Submit Application
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
                                placeholder="Ask AI to modify your CV..."
                                className="resize-none"
                                rows={3}
                                value={message}
                                onChange={(e) => setMessage(e.target.value)}
                                onKeyDown={(e) => {
                                    if (e.key === 'Enter' && !e.shiftKey) {
                                        e.preventDefault()
                                        handleSendMessage()
                                    }
                                }}
                            />
                            <Button
                                size="icon"
                                className="h-auto aspect-square"
                                onClick={handleSendMessage}
                                disabled={!message.trim()}
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
                        {typstContent ? (
                            <TypstRenderer content={typstContent} className="p-4" />
                        ) : (
                            <div className="flex items-center justify-center h-96">
                                <p className="text-muted-foreground">Loading CV...</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </>
    )
}
