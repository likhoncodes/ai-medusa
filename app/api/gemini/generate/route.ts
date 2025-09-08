import { type NextRequest, NextResponse } from "next/server"
import { geminiService } from "@/lib/gemini"
import { ErrorHandler, ValidationError, withErrorHandling } from "@/lib/error-handler"

async function handler(request: NextRequest): Promise<NextResponse> {
  // Validate environment
  ErrorHandler.validateEnvironment(["GEMINI_API_KEY"])

  const body = await request.json()

  // Validate request
  ErrorHandler.validateRequest(body, ["prompt"])

  const { prompt, options } = body

  if (typeof prompt !== "string" || prompt.trim().length === 0) {
    throw new ValidationError("Prompt must be a non-empty string")
  }

  // Generate text using Gemini
  const result = await geminiService.generateText(prompt, options)

  return NextResponse.json({
    success: true,
    data: {
      prompt,
      response: result,
      timestamp: new Date().toISOString(),
      model: "gemini-1.5-flash",
    },
  })
}

export const POST = withErrorHandling(handler, "gemini-generate")
