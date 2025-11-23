import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Checkbox } from '@/components/ui/checkbox'
import {
    Github,
    CheckCircle2,
    Eye,
    EyeOff,
    Zap,
    Target,
    TrendingUp
} from 'lucide-react'
import { userService } from '@/services'

export default function Login() {
    const navigate = useNavigate()
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [showPassword, setShowPassword] = useState(false)
    const [rememberMe, setRememberMe] = useState(false)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')
    const [emailValid, setEmailValid] = useState(false)

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

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        setError('')

        try {
            await userService.login({ email, password })
            navigate('/dashboard')
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Login failed. Please try again.')
        } finally {
            setLoading(false)
        }
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
                            Welcome to CV Tailor
                        </h1>
                        <p className="text-xl text-white/90 leading-relaxed">
                            Transform your job applications with AI-powered CV customization
                        </p>
                    </div>

                    {/* Why CV Tailor bullets */}
                    <div className="space-y-4 pt-4">
                        <h2 className="text-lg font-semibold text-white/80 uppercase tracking-wider">
                            Why CV Tailor?
                        </h2>
                        <div className="space-y-3">
                            <div className="flex items-start gap-3">
                                <div className="mt-1 rounded-full bg-white/20 p-2">
                                    <Zap className="h-5 w-5 text-white" />
                                </div>
                                <div>
                                    <h3 className="font-semibold">AI-Powered Optimization</h3>
                                    <p className="text-sm text-white/80">Automatically tailor your CV to match job requirements</p>
                                </div>
                            </div>
                            <div className="flex items-start gap-3">
                                <div className="mt-1 rounded-full bg-white/20 p-2">
                                    <Target className="h-5 w-5 text-white" />
                                </div>
                                <div>
                                    <h3 className="font-semibold">Higher Match Rates</h3>
                                    <p className="text-sm text-white/80">Beat ATS systems and get more interview calls</p>
                                </div>
                            </div>
                            <div className="flex items-start gap-3">
                                <div className="mt-1 rounded-full bg-white/20 p-2">
                                    <TrendingUp className="h-5 w-5 text-white" />
                                </div>
                                <div>
                                    <h3 className="font-semibold">Track Your Success</h3>
                                    <p className="text-sm text-white/80">Monitor applications and optimize your strategy</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Social Proof */}
                    <div className="pt-6 border-t border-white/20">
                        <p className="text-sm text-white/70">
                            Trusted by <span className="font-semibold text-white">10,000+</span> job seekers worldwide
                        </p>
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
                            Welcome back
                        </h2>
                        <p className="text-muted-foreground">
                            Sign in to your account to continue
                        </p>
                    </div>

                    {/* Form */}
                    <form onSubmit={handleLogin} className="space-y-5">
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
                            <div className="flex items-center justify-between">
                                <Label htmlFor="password" className="text-sm font-medium">
                                    Password
                                </Label>
                                <Link
                                    to="/forgot-password"
                                    className="text-xs text-primary hover:text-primary-hover transition-fast"
                                >
                                    Forgot password?
                                </Link>
                            </div>
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
                        </div>

                        {/* Remember Me */}
                        <div className="flex items-center space-x-2">
                            <Checkbox
                                id="remember"
                                checked={rememberMe}
                                onCheckedChange={(checked) => setRememberMe(checked as boolean)}
                            />
                            <Label
                                htmlFor="remember"
                                className="text-sm text-muted-foreground cursor-pointer"
                            >
                                Remember me for 30 days
                            </Label>
                        </div>

                        {/* Error Message */}
                        {error && (
                            <div className="p-3 rounded-lg bg-destructive/10 border border-destructive/20">
                                <p className="text-sm text-destructive">{error}</p>
                            </div>
                        )}

                        {/* Submit Button */}
                        <div className="space-y-2">
                            <Button
                                type="submit"
                                disabled={loading}
                                className="w-full gradient-primary hover:shadow-lg transition-smooth h-11 font-semibold"
                            >
                                {loading ? (
                                    <span className="flex items-center gap-2">
                                        <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                        Signing in...
                                    </span>
                                ) : (
                                    'Sign In'
                                )}
                            </Button>
                            <p className="text-xs text-center text-muted-foreground">
                                Takes ~30 seconds to set up your profile
                            </p>
                        </div>
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
                        >
                            <Github className="mr-2 h-4 w-4" />
                            Github
                        </Button>
                        <Button
                            variant="outline"
                            className="h-11 transition-smooth hover:bg-muted"
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

                    {/* Sign Up Link */}
                    <p className="text-center text-sm text-muted-foreground">
                        Don't have an account?{' '}
                        <Link
                            to="/signup"
                            className="text-primary hover:text-primary-hover font-semibold transition-fast"
                        >
                            Sign up for free
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    )
}
