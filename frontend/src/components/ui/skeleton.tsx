import { cn } from "@/lib/utils"

interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
    variant?: 'default' | 'card' | 'row' | 'chat' | 'preview'
}

function Skeleton({ className, variant = 'default', ...props }: SkeletonProps) {
    const variantClasses = {
        default: 'h-4 w-full',
        card: 'h-32 w-full rounded-card',
        row: 'h-16 w-full rounded-md',
        chat: 'h-20 w-3/4 rounded-2xl',
        preview: 'h-96 w-full rounded-card-lg'
    }

    return (
        <div
            className={cn(
                'shimmer rounded-md bg-muted',
                variantClasses[variant],
                className
            )}
            {...props}
        />
    )
}

export { Skeleton }
