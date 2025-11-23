import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Progress } from '@/components/ui/progress'
import {
    Github,
    CheckCircle2,
    Eye,
    EyeOff,
    Shield,
    Users,
    Clock
} from 'lucide-react'

export default function Signup() {
    const navigate = useNavigate()
    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [showPassword, setShowPassword] = useState(false)
    const [loading, setLoading] = useState(false)
    const [emailValid, setEmailValid] = useState(false)

    // Password strength calculation
    const getPasswordStrength = (pwd: string): { score: number; label: string; color: string } => {
        if (!pwd) return { score: 0, label: '', color: '' }

        let score = 0
        if (pwd.length >= 8) score += 25
        if (pwd.length >= 12) score += 15
        if (/[a-z]/.test(pwd)) score += 15
        if (/[A-Z]/.test(pwd)) score += 15
        if (/[0-9]/.test(pwd)) score += 15
        if (/[^a-zA-Z0-9]/.test(pwd)) score += 15

        if (score < 40) return { score, label: 'Weak', color: 'text-destructive' }
        if (score < 70) return { score, label: 'Fair', color: 'text-accent-amber' }
        if (score < 90) return { score, label: 'Good', color: 'text-accent-mint' }
        return { score, label: 'Strong', color: 'text-accent-mint' }
    }

    const passwordStrength = getPasswordStrength(password)

    const validateEmail = (value: string) => {
        const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
        setEmailValid(isValid && value.length > 0)
        return isValid
    }

    const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value
        setEmail(value)
        validateEmail(value)
    }

    const handleSignup = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)

        // Simulate signup
        setTimeout(() => {
            navigate('/onboarding')
        }, 1000)
    }

    return (
        <div className="min-h-screen flex bg-background">
            {/* Left Column - Hero/Pitch */}
            <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden bg-gradient-to-br from-primary via-primary-hover to-primary-gradient-end p-12 items-center justify-center">
                {/* Animated gradient overlay */}
                <div className="absolute inset-0 bg-gradient-to-br from-primary/90 via-primary-hover/80 to-primary-gradient-end/90 animate-pulse-slow" />

                {/* Content */}
                <div className="relative z-10 max-w-lg text-white space-y-8">
                    <div className="space-y-4">
                        <h1 className="text-5xl font-display font-bold leading-tight">
                            Start Your Journey
                        </h1>
                        <p className="text-xl text-white/90 leading-relaxed">
                            Join thousands of professionals landing their dream jobs
                        </p>
                    </div>

                    {/* Benefits */}
                    <div className="space-y-4 pt-4">
                        <h2 className="text-lg font-semibold text-white/80 uppercase tracking-wider">
                            What you'll get
                        </h2>
                        <div className="space-y-3">
                            <div className="flex items-start gap-3">
                                <div className="mt-1 rounded-full bg-white/20 p-2">
                                    <Shield className="h-5 w-5 text-white" />
                                </div>
                                <div>
                                    <h3 className="font-semibold">Free Forever</h3>
                                    <p className="text-sm text-white/80">No credit card required. Full access to core features.</p>
                                </div>
                            </div>
                            <div className="flex items-start gap-3">
                                <div className="mt-1 rounded-full bg-white/20 p-2">
                                    <Clock className="h-5 w-5 text-white" />
                                </div>
                                <div>
                                    <h3 className="font-semibold">Quick Setup</h3>
                                    <p className="text-sm text-white/80">Get started in under 2 minutes with our smart onboarding</p>
                                </div>
                            </div>
                            <div className="flex items-start gap-3">
                                <div className="mt-1 rounded-full bg-white/20 p-2">
                                    <Users className="h-5 w-5 text-white" />
                                </div>
                                <div>
                                    <h3 className="font-semibold">Join the Community</h3>
                                    <p className="text-sm text-white/80">Connect with other job seekers and share insights</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Testimonial */}
                    <div className="pt-6 border-t border-white/20 space-y-3">
                        <p className="text-sm italic text-white/90">
                            "CV Tailor helped me land 3x more interviews. The AI suggestions are spot-on!"
                        </p>
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center">
                                <span className="text-sm font-semibold">AS</span>
                            </div>
                            <div>
                                <p className="text-sm font-medium">Alex Sullivan</p>
                                <p className="text-xs text-white/70">Software Engineer at Google</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Right Column - Form */}
            <div className="flex-1 flex items-center justify-center p-6 lg:p-12">
                <div className="w-full max-w-md space-y-8">
                    {/* Mobile Logo */}
                    <div className="lg:hidden text-center mb-8">
                        <div className="inline-flex items-center gap-2 mb-4">
                            <div className="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center shadow-lg">
                                <span className="text-white font-display font-bold text-lg">CV</span>
                            </div>
                            <h1 className="text-2xl font-display font-bold gradient-text">CV Tailor</h1>
                        </div>
                    </div>

                    {/* Form Header */}
                    <div className="space-y-2 text-center lg:text-left">
                        <h2 className="text-3xl font-display font-bold tracking-tight">
                            Create your account
                        </h2>
                        <p className="text-muted-foreground">
                            Get started for free. No credit card needed.
                        </p>
                    </div>

                    {/* Form */}
                    <form onSubmit={handleSignup} className="space-y-5">
                        {/* Name Field */}
                        <div className="space-y-2">
                            <Label htmlFor="name" className="text-sm font-medium">
                                Full name
                            </Label>
                            <Input
                                id="name"
                                type="text"
                                placeholder="John Doe"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                required
                            />
                        </div>

                        {/* Email Field */}
                        <div className="space-y-2">
                            <Label htmlFor="email" className="text-sm font-medium">
                                Email address
                            </Label>
                            <div className="relative">
                                <Input
                                    id="email"
                                    type="email"
                                    placeholder="you@example.com"
                                    value={email}
                                    onChange={handleEmailChange}
                                    required
                                    className={`pr-10 transition-fast ${emailValid ? 'border-accent-mint focus:ring-accent-mint' : ''
                                        }`}
                                />
                                {emailValid && (
                                    <CheckCircle2 className="absolute right-3 top-1/2 -translate-y-1/2 h-5 w-5 text-accent-mint" />
                                )}
                            </div>
                        </div>

                        {/* Password Field */}
                        <div className="space-y-2">
                            <Label htmlFor="password" className="text-sm font-medium">
                                Password
                            </Label>
                            <div className="relative">
                                <Input
                                    id="password"
                                    type={showPassword ? 'text' : 'password'}
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                    className="pr-10"
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-fast"
                                >
                                    {showPassword ? (
                                        <EyeOff className="h-5 w-5" />
                                    ) : (
                                        <Eye className="h-5 w-5" />
                                    )}
                                </button>
                            </div>

                            {/* Password Strength Meter */}
                            {password && (
                                <div className="space-y-1">
                                    <div className="flex items-center justify-between text-xs">
                                        <span className="text-muted-foreground">Password strength:</span>
                                        <span className={`font-medium ${passwordStrength.color}`}>
                                            {passwordStrength.label}
                                        </span>
                                    </div>
                                    <Progress
                                        value={passwordStrength.score}
                                        className="h-1.5"
                                    />
                                    <p className="text-xs text-muted-foreground mt-1">
                                        Use 8+ characters with letters, numbers & symbols
                                    </p>
                                </div>
                            )}
                        </div>

                        {/* Submit Button */}
                        <div className="space-y-2">
                            <Button
                                type="submit"
                                disabled={loading || !emailValid || passwordStrength.score < 40}
                                className="w-full gradient-primary hover:shadow-lg transition-smooth h-11 font-semibold"
                            >
                                {loading ? (
                                    <span className="flex items-center gap-2">
                                        <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                        Creating account...
                                    </span>
                                ) : (
                                    'Create Account'
                                )}
                            </Button>
                            <p className="text-xs text-center text-muted-foreground">
                                Takes ~30 seconds • Start tailoring CVs immediately
                            </p>
                        </div>

                        {/* Terms */}
                        <p className="text-xs text-center text-muted-foreground">
                            By signing up, you agree to our{' '}
                            <Link to="/terms" className="text-primary hover:underline">
                                Terms of Service
                            </Link>{' '}
                            and{' '}
                            <Link to="/privacy" className="text-primary hover:underline">
                                Privacy Policy
                            </Link>
                        </p>
                    </form>

                    {/* Divider */}
                    <div className="relative">
                        <div className="absolute inset-0 flex items-center">
                            <span className="w-full border-t border-border" />
                        </div>
                        <div className="relative flex justify-center text-xs uppercase">
                            <span className="bg-background px-2 text-muted-foreground">
                                Or continue with
                            </span>
                        </div>
                    </div>

                    {/* OAuth Buttons */}
                    <div className="grid grid-cols-2 gap-3">
                        <Button
                            variant="outline"
                            className="h-11 transition-smooth hover:bg-muted"
                            type="button"
                        >
                            <Github className="mr-2 h-4 w-4" />
                            Github
                        </Button>
                        <Button
                            variant="outline"
                            className="h-11 transition-smooth hover:bg-muted"
                            type="button"
                        >
                            <svg className="mr-2 h-4 w-4" viewBox="0 0 24 24">
                                <path
                                    d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                                    fill="#4285F4"
                                />
                                <path
                                    d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                                    fill="#34A853"
                                />
                                <path
                                    d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                                    fill="#FBBC05"
                                />
                                <path
                                    d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                                    fill="#EA4335"
                                />
                            </svg>
                            Google
                        </Button>
                    </div>

                    {/* Sign In Link */}
                    <p className="text-center text-sm text-muted-foreground">
                        Already have an account?{' '}
                        <Link
                            to="/login"
                            className="text-primary hover:text-primary-hover font-semibold transition-fast"
                        >
                            Sign in
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    )
}
