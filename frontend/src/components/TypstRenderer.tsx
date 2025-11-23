import { useEffect, useRef, useState } from 'react'
import { $typst } from '@myriaddreamin/typst.ts/dist/esm/contrib/snippet.mjs'
import compilerWasmUrl from '@myriaddreamin/typst-ts-web-compiler/pkg/typst_ts_web_compiler_bg.wasm?url'
import rendererWasmUrl from '@myriaddreamin/typst-ts-renderer/pkg/typst_ts_renderer_bg.wasm?url'

interface TypstRendererProps {
    content: string
    className?: string
}

let isInitialized = false

export default function TypstRenderer({ content, className = '' }: TypstRendererProps) {
    const containerRef = useRef<HTMLDivElement>(null)
    const [error, setError] = useState<string | null>(null)
    const [loading, setLoading] = useState(true)
    const [svgContent, setSvgContent] = useState<string>('')

    useEffect(() => {
        const initAndRender = async () => {
            try {
                setLoading(true)
                setError(null)

                // Initialize Typst WASM modules (only once)
                if (!isInitialized) {
                    await $typst.setCompilerInitOptions({
                        getModule: () => compilerWasmUrl
                    })
                    await $typst.setRendererInitOptions({
                        getModule: () => rendererWasmUrl
                    })
                    isInitialized = true
                }

                // Render the Typst content to SVG
                const svg = await $typst.svg({
                    mainContent: content,
                })

                if (svg) {
                    setSvgContent(svg)
                    setError(null)
                } else {
                    throw new Error('Failed to generate SVG from Typst content')
                }

                setLoading(false)
            } catch (err) {
                console.error('Error rendering Typst:', err)
                setError(err instanceof Error ? err.message : 'Unknown error occurred')
                setLoading(false)
            }
        }

        if (content) {
            initAndRender()
        }
    }, [content])

    useEffect(() => {
        if (containerRef.current && svgContent) {
            containerRef.current.innerHTML = svgContent
        }
    }, [svgContent])

    if (error) {
        return (
            <div className={`p-8 text-center ${className}`}>
                <p className="text-red-500 font-semibold mb-2">Error rendering CV</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">{error}</p>
                <details className="mt-4 text-left">
                    <summary className="cursor-pointer text-sm text-blue-600">View Typst Source</summary>
                    <pre className="mt-2 bg-gray-50 dark:bg-gray-900 p-4 rounded overflow-x-auto text-xs font-mono">
                        {content}
                    </pre>
                </details>
            </div>
        )
    }

    if (loading) {
        return (
            <div className={`flex flex-col items-center justify-center p-8 ${className}`}>
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
                <p className="text-muted-foreground">Rendering CV...</p>
            </div>
        )
    }

    return (
        <div
            ref={containerRef}
            className={`typst-container ${className}`}
            style={{
                width: '100%',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'flex-start',
            }}
        />
    )
}
