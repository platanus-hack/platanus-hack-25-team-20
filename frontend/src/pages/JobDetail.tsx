import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { ArrowLeft, MapPin, Clock, DollarSign, Briefcase, Edit, Send, FileDown } from 'lucide-react'
import {
  jobService,
  cvService,
  projectService,
  userService,
  submissionService,
  type Job,
  type UserResponse,
} from "@/services";
import { cleanHtml, stripHtml } from "@/utils/htmlCleaner";
import { useToast } from "@/hooks/use-toast";

export default function JobDetail() {
  const navigate = useNavigate();
  const { id } = useParams();
  const { toast } = useToast();
  const [job, setJob] = useState<Job | null>(null);
  const [user, setUser] = useState<UserResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [creatingCV, setCreatingCV] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    async function loadData() {
      if (!id) return;
      try {
        // TODO: Get actual user ID from auth context
        const userId = 1;
        const [jobData, userData] = await Promise.all([
          jobService.getById(id),
          userService.getById(userId),
        ]);
        setJob(jobData);
        setUser(userData);
      } catch (error) {
        console.error("Failed to load data:", error);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [id]);

  const handleCustomizeCV = async () => {
    if (!id || !job) return;

    setCreatingCV(true);
    try {
      // TODO: Get actual user ID from auth context
      const userId = 1;

      // Get user's projects
      const projects = await projectService.getUserProjects(userId);
      let projectId = projects[0]?.id;

      // If no projects, create a default one
      if (!projectId) {
        const newProject = await projectService.create({
          user_id: userId,
          name: `Application for ${job.company}`,
          target_role: job.title,
        });
        projectId = newProject.id;
      }

      // Create CV with the job offering information
      // TODO: Get template_id from user preference or use default (1)
      // Strip HTML from description for cleaner prompt
      const cleanDescription = stripHtml(job.description);
      const cv = await cvService.create(projectId, {
        project_id: projectId,
        template_id: 1, // Default template
        messages: [
          {
            role: "user",
            content: `Create a CV optimized for the position: ${job.title} at ${job.company}. ${cleanDescription}`,
            timestamp: new Date().toISOString(),
          },
        ],
      });

      // Navigate to editor with the CV ID and job offering ID
      navigate(`/editor/${cv.id}`, { state: { jobOfferingId: id } });
    } catch (error) {
      console.error("Failed to create CV:", error);
      alert("Failed to create CV. Please try again.");
    } finally {
      setCreatingCV(false);
    }
  };

  const handleSubmitApplication = async () => {
    if (!id || !job) return;

    setSubmitting(true);
    try {
      // TODO: Get actual user ID from auth context
      const userId = 1;

      // Create the application submission
      await submissionService.create({
        user_id: userId,
        job_offering_id: id,
        status: "sent",
        notes: `Applied to ${job.title} at ${job.company}`,
      });

      // Show success message
      toast({
        title: "Application Submitted!",
        description: `Your application for ${job.title} at ${job.company} has been recorded.`,
      });

      // Open the job URL in a new tab
      if (job.url) {
        window.open(job.url, "_blank");
      }
    } catch (error) {
      console.error("Failed to submit application:", error);
      toast({
        title: "Error",
        description: "Failed to submit application. Please try again.",
        variant: "destructive",
      });
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">
        Loading...
      </div>
    );
  }

  if (!job) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">
        Job not found
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <div className="bg-white dark:bg-gray-950 border-b border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <Button
            variant="ghost"
            onClick={() => navigate("/jobs")}
            className="mb-4"
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Jobs
          </Button>
          <div className="flex items-start justify-between">
            <div className="space-y-2">
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white tracking-tight">
                {job.title}
              </h1>
              <p className="text-xl text-gray-600 dark:text-gray-400">
                {job.company}
              </p>
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
                <p
                  className="text-gray-600 dark:text-gray-400"
                  dangerouslySetInnerHTML={cleanHtml(job.description)}
                ></p>

                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-3">
                    Requirements
                  </h3>
                  <ul className="space-y-2">
                    {job.requirements?.map((req: string, i: number) => (
                      <li key={i} className="flex items-start">
                        <span className="mr-2 text-blue-600">•</span>
                        <span className="text-gray-600 dark:text-gray-400">
                          {req}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-3">
                    Responsibilities
                  </h3>
                  <ul className="space-y-2">
                    {job.responsibilities?.map((resp: string, i: number) => (
                      <li key={i} className="flex items-start">
                        <span className="mr-2 text-blue-600">•</span>
                        <span className="text-gray-600 dark:text-gray-400">
                          {resp}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="flex flex-wrap gap-2 pt-4">
                  {job.areas.map((area) => (
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
                        <p className="font-bold text-gray-900 dark:text-white">
                          {user?.full_name || "Loading..."}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {user?.email || ""}
                        </p>
                      </div>
                      <Separator />
                      <div>
                        <p className="font-semibold text-gray-900 dark:text-white mb-1">
                          Summary
                        </p>
                        <p className="text-xs text-gray-600 dark:text-gray-400">
                          CV will be generated with AI when you click "Customize
                          CV"
                        </p>
                      </div>
                      <div>
                        <p className="font-semibold text-gray-900 dark:text-white mb-1">
                          Skills
                        </p>
                        <p className="text-xs text-gray-600 dark:text-gray-400">
                          Your skills will be automatically included...
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Button
                      className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"
                      onClick={handleCustomizeCV}
                      disabled={creatingCV}
                    >
                      <Edit className="mr-2 h-4 w-4" />
                      {creatingCV ? "Creating CV..." : "Customize CV"}
                    </Button>
                    <div className="grid grid-cols-2 gap-2">
                      <Button variant="outline" size="sm">
                        <FileDown className="mr-2 h-4 w-4" />
                        Download
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={handleSubmitApplication}
                        disabled={!job.url || submitting}
                      >
                        <Send className="mr-2 h-4 w-4" />
                        {submitting ? "Submitting..." : "Submit"}
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
  );
}
