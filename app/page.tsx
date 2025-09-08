import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { CheckCircle, Database, Zap, Shield, Code, FileText, Bot, Globe, Cpu } from "lucide-react"

export default function HomePage() {
  const features = [
    {
      icon: <Bot className="h-6 w-6" />,
      title: "Multi-Agent AI",
      description: "Parallel execution with intelligent task distribution and coordination",
    },
    {
      icon: <Globe className="h-6 w-6" />,
      title: "Browser Automation",
      description: "Advanced Playwright integration for web scraping and form automation",
    },
    {
      icon: <Zap className="h-6 w-6" />,
      title: "Gemini AI Integration",
      description: "Powered by Google's advanced Gemini model for intelligent processing",
    },
    {
      icon: <Cpu className="h-6 w-6" />,
      title: "FastAPI Backend",
      description: "High-performance API with modular architecture and real-time processing",
    },
    {
      icon: <Database className="h-6 w-6" />,
      title: "Data Processing",
      description: "Advanced data transformation and analysis capabilities",
    },
    {
      icon: <Code className="h-6 w-6" />,
      title: "CDP Integration",
      description: "Chrome DevTools Protocol for debugging and performance monitoring",
    },
    {
      icon: <Shield className="h-6 w-6" />,
      title: "Secure Sandbox",
      description: "Docker containerization with isolated execution environments",
    },
    {
      icon: <FileText className="h-6 w-6" />,
      title: "OpenAPI Docs",
      description: "Comprehensive API documentation with interactive testing",
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-muted/20">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <Badge variant="secondary" className="mb-4">
            🐍 AI Medusa Platform
          </Badge>
          <h1 className="text-4xl font-bold mb-4 text-balance">AI-Powered Automation Platform</h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto text-pretty">
            Unleash the power of multi-agent AI automation with browser control, intelligent task processing, and
            scalable execution environments. Built with Gemini AI, FastAPI, and modern web technologies.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          {features.map((feature, index) => (
            <Card key={index} className="text-center">
              <CardHeader>
                <div className="mx-auto mb-4 p-3 bg-primary/10 rounded-full w-fit">{feature.icon}</div>
                <CardTitle className="text-lg">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>{feature.description}</CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle className="h-5 w-5 text-green-500" />
                System Status
              </CardTitle>
              <CardDescription>Current AI Medusa platform status and health</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between items-center">
                <span>Multi-Agent System</span>
                <Badge variant="outline" className="text-green-600">
                  Active
                </Badge>
              </div>
              <div className="flex justify-between items-center">
                <span>Browser Automation</span>
                <Badge variant="outline" className="text-green-600">
                  Ready
                </Badge>
              </div>
              <div className="flex justify-between items-center">
                <span>Gemini AI</span>
                <Badge variant="outline" className="text-green-600">
                  Connected
                </Badge>
              </div>
              <div className="flex justify-between items-center">
                <span>FastAPI Backend</span>
                <Badge variant="outline" className="text-green-600">
                  Operational
                </Badge>
              </div>
              <div className="flex justify-between items-center">
                <span>Docker Sandbox</span>
                <Badge variant="outline" className="text-green-600">
                  Available
                </Badge>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5" />
                Quick Start
              </CardTitle>
              <CardDescription>Get started with AI Medusa automation platform</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <p className="text-sm text-muted-foreground">1. Clone the ai-medusa repository</p>
                <p className="text-sm text-muted-foreground">
                  2. Set up GEMINI_API_KEY and other environment variables
                </p>
                <p className="text-sm text-muted-foreground">3. Run docker-compose up for full stack deployment</p>
                <p className="text-sm text-muted-foreground">4. Access the API documentation at /docs</p>
              </div>
              <Button className="w-full">View GitHub Repository</Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
