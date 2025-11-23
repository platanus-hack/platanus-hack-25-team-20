import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Checkbox } from '@/components/ui/checkbox'
import { ArrowRight, Briefcase, MapPin, Clock, DollarSign, Search } from 'lucide-react'
import { jobService, type Job } from '@/services'
import { cleanHtml } from "@/utils/htmlCleaner";
const jobAreas = [
    'Full Stack Development',
    'Frontend Development',
    'Backend Development',
    'Mobile Development',
    'DevOps',
    'Data Science',
    'Machine Learning',
    'UI/UX Design',
    'Product Management',
    'Security Engineering',
]

export default function Jobs() {
    const navigate = useNavigate()
    const [selectedAreas, setSelectedAreas] = useState<string[]>([])
    const [searchQuery, setSearchQuery] = useState('')
    const [jobs, setJobs] = useState<Job[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function loadJobs() {
            try {
                const data = await jobService.getAll()
                setJobs(data)
            } catch (error) {
                console.error('Failed to load jobs:', error)
            } finally {
                setLoading(false)
            }
        }
        loadJobs()
    }, [])

    const toggleArea = (area: string) => {
        setSelectedAreas(prev =>
            prev.includes(area) ? prev.filter(a => a !== area) : [...prev, area]
        )
    }

    const filteredJobs = jobs.filter(job => {
        const matchesArea = selectedAreas.length === 0 || job.areas.some(area => selectedAreas.includes(area))
        const matchesSearch = searchQuery === '' ||
            job.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
            job.company.toLowerCase().includes(searchQuery.toLowerCase())
        return matchesArea && matchesSearch
    })

    if (loading) {
        return <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">Loading...</div>
    }


    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        {/* Header */}
        <div className="bg-white dark:bg-gray-950 border-b border-gray-200 dark:border-gray-800">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white tracking-tight">
              Browse Job Opportunities
            </h1>
            <p className="mt-2 text-gray-600 dark:text-gray-400">
              Select job areas and find opportunities to apply with tailored CVs
            </p>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            {/* Filters Sidebar */}
            <div className="lg:col-span-1">
              <Card className="sticky top-4">
                <CardHeader>
                  <CardTitle className="text-lg">Job Areas</CardTitle>
                  <CardDescription>Select your interests</CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  {jobAreas.map((area) => (
                    <div key={area} className="flex items-center space-x-2">
                      <Checkbox
                        id={area}
                        checked={selectedAreas.includes(area)}
                        onCheckedChange={() => toggleArea(area)}
                      />
                      <label
                        htmlFor={area}
                        className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
                      >
                        {area}
                      </label>
                    </div>
                  ))}
                </CardContent>
                <CardFooter>
                  <Button
                    variant="outline"
                    className="w-full"
                    onClick={() => setSelectedAreas([])}
                    disabled={selectedAreas.length === 0}
                  >
                    Clear Filters
                  </Button>
                </CardFooter>
              </Card>
            </div>

            {/* Job Listings */}
            <div className="lg:col-span-3 space-y-6">
              {/* Search Bar */}
              <div className="relative">
                <Search className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                <Input
                  placeholder="Search jobs by title or company..."
                  className="pl-10 bg-white dark:bg-gray-950"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>

              {/* Results Count */}
              <div className="flex items-center justify-between">
                <p className="text-sm text-muted-foreground">
                  {filteredJobs.length}{" "}
                  {filteredJobs.length === 1 ? "job" : "jobs"} found
                </p>
                {selectedAreas.length > 0 && (
                  <div className="flex flex-wrap gap-2">
                    {selectedAreas.map((area) => (
                      <Badge key={area} variant="secondary" className="text-xs">
                        {area}
                      </Badge>
                    ))}
                  </div>
                )}
              </div>

              {/* Job Cards */}
              <div className="space-y-4">
                {filteredJobs.length === 0 ? (
                  <Card className="p-12 text-center">
                    <div className="flex flex-col items-center justify-center space-y-3">
                      <Briefcase className="h-12 w-12 text-gray-400" />
                      <p className="text-lg font-medium text-gray-900 dark:text-white">
                        No jobs found
                      </p>
                      <p className="text-sm text-muted-foreground">
                        Try adjusting your filters or search query
                      </p>
                    </div>
                  </Card>
                ) : (
                  filteredJobs.map((job) => (
                    <Card
                      key={job.id}
                      className="hover:shadow-lg transition-shadow cursor-pointer group"
                    >
                      <CardHeader>
                        <div className="flex items-start justify-between">
                          <div className="space-y-1 flex-1">
                            <CardTitle className="text-xl group-hover:text-blue-600 transition-colors">
                              {job.title}
                            </CardTitle>
                            <CardDescription className="text-base font-medium text-gray-900 dark:text-gray-100">
                              {job.company}
                            </CardDescription>
                          </div>
                          <Button
                            onClick={() => navigate(`/jobs/${job.id}`)}
                            className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"
                          >
                            View Details
                            <ArrowRight className="ml-2 h-4 w-4" />
                          </Button>
                        </div>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <p
                          className="text-sm text-gray-600 dark:text-gray-400"
                          dangerouslySetInnerHTML={cleanHtml(job.description)}
                        ></p>
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
                        {/* <div className="flex flex-wrap gap-2">
                                                {job.areas.map(area => (
                                                    <Badge key={area} variant="outline" className="text-xs">
                                                        {area}
                                                    </Badge>
                                                ))}
                                            </div> */}
                      </CardContent>
                    </Card>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
}
