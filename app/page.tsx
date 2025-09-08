import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { CheckCircle, Database, Zap, Shield, Code, FileText } from "lucide-react"

export default function HomePage() {
  const features = [
    {
      icon: <Zap className="h-6 w-6" />,
      title: "Gemini AI Integration",
      description: "Powered by Google's advanced Gemini model for intelligent processing",
    },
    {
      icon: <Database className="h-6 w-6" />,
      title: "Data Processing",
      description: "Advanced data transformation and analysis capabilities",
    },
    {
      icon: <Code className="h-6 w-6" />,
      title: "API Integration",
      description: "RESTful APIs for seamless front-end communication",
    },
    {
      icon: <Shield className="h-6 w-6" />,
      title: "Error Handling",
      description: "Robust error handling and validation mechanisms",
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-muted/20">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <Badge variant="secondary" className="mb-4">
            Gemini-Powered Backend System
          </Badge>
          <h1 className="text-4xl font-bold mb-4 text-balance">Advanced Backend System</h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto text-pretty">
            A scalable, maintainable backend system utilizing Google's Gemini AI model with comprehensive data
            processing and API integration capabilities.
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
              <CardDescription>Current backend system status and health</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between items-center">
                <span>API Endpoints</span>
                <Badge variant="outline" className="text-green-600">
                  Active
                </Badge>
              </div>
              <div className="flex justify-between items-center">
                <span>Gemini Integration</span>
                <Badge variant="outline" className="text-green-600">
                  Ready
                </Badge>
              </div>
              <div className="flex justify-between items-center">
                <span>Error Handling</span>
                <Badge variant="outline" className="text-green-600">
                  Enabled
                </Badge>
              </div>
              <div className="flex justify-between items-center">
                <span>Data Processing</span>
                <Badge variant="outline" className="text-green-600">
                  Operational
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
              <CardDescription>Get started with the backend system</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <p className="text-sm text-muted-foreground">1. Set up your GEMINI_API_KEY environment variable</p>
                <p className="text-sm text-muted-foreground">2. Use the /api endpoints for data processing</p>
                <p className="text-sm text-muted-foreground">3. Check the documentation for detailed API usage</p>
              </div>
              <Button className="w-full">View Documentation</Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
