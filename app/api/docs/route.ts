import { NextResponse } from "next/server"
import { withErrorHandling } from "@/lib/error-handler"

async function handler(): Promise<NextResponse> {
  const documentation = {
    title: "Gemini Backend System API Documentation",
    version: "1.0.0",
    description: "A comprehensive backend system utilizing Google Gemini AI for data processing and analysis",
    baseUrl: process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000/api",
    endpoints: {
      "/api/health": {
        method: "GET",
        description: "Health check endpoint",
        response: "System health status and service information",
      },
      "/api/gemini/generate": {
        method: "POST",
        description: "Generate text using Gemini AI",
        parameters: {
          prompt: "string (required) - The input prompt for text generation",
          options: "object (optional) - Generation options (temperature, maxOutputTokens, etc.)",
        },
        example: {
          prompt: "Explain quantum computing in simple terms",
          options: {
            temperature: 0.7,
            maxOutputTokens: 500,
          },
        },
      },
      "/api/data/process": {
        method: "POST",
        description: "Process data using various operations",
        parameters: {
          data: "any (required) - The data to process",
          operation: "string (required) - Operation type: transform, analyze, validate, process",
          options: "object (optional) - Operation-specific options",
        },
        examples: {
          transform: {
            data: [{ name: "John", age: 30 }],
            operation: "transform",
            options: { transformationType: "normalize" },
          },
          analyze: {
            data: "Sample text for sentiment analysis",
            operation: "analyze",
            options: { analysisType: "sentiment" },
          },
        },
      },
    },
    errorHandling: {
      description: "All endpoints return structured error responses",
      format: {
        error: {
          message: "string - Human readable error message",
          code: "string - Error code for programmatic handling",
          statusCode: "number - HTTP status code",
          timestamp: "string - ISO timestamp",
          context: "string - Additional context about the error",
        },
      },
    },
    authentication: {
      description: "API requires GEMINI_API_KEY environment variable to be set",
      setup: "Get your API key from Google AI Studio and set it as GEMINI_API_KEY",
    },
  }

  return NextResponse.json(documentation)
}

export const GET = withErrorHandling(handler, "api-docs")
