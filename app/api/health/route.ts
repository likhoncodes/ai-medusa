import { NextResponse } from "next/server"
import { withErrorHandling } from "@/lib/error-handler"

async function handler(): Promise<NextResponse> {
  const healthCheck = {
    status: "healthy",
    timestamp: new Date().toISOString(),
    version: "1.0.0",
    services: {
      gemini: {
        status: process.env.GEMINI_API_KEY ? "configured" : "not_configured",
        model: "gemini-1.5-flash",
      },
      dataProcessor: {
        status: "operational",
      },
      errorHandler: {
        status: "operational",
      },
    },
    environment: {
      nodeVersion: process.version,
      platform: process.platform,
    },
  }

  return NextResponse.json(healthCheck)
}

export const GET = withErrorHandling(handler, "health-check")
