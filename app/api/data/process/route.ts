import { type NextRequest, NextResponse } from "next/server"
import { dataProcessor } from "@/lib/data-processor"
import { ErrorHandler, ValidationError, withErrorHandling } from "@/lib/error-handler"

async function handler(request: NextRequest): Promise<NextResponse> {
  const body = await request.json()

  // Validate request
  ErrorHandler.validateRequest(body, ["data", "operation"])

  const { data, operation, options } = body

  const validOperations = ["transform", "analyze", "validate", "process"]
  if (!validOperations.includes(operation)) {
    throw new ValidationError(`Invalid operation. Must be one of: ${validOperations.join(", ")}`)
  }

  let result: any

  switch (operation) {
    case "transform":
      if (!options?.transformationType) {
        throw new ValidationError("transformationType is required for transform operation")
      }
      result = await dataProcessor.transformData(data, options.transformationType)
      break

    case "analyze":
      if (!options?.analysisType) {
        throw new ValidationError("analysisType is required for analyze operation")
      }
      const { geminiService } = await import("@/lib/gemini")
      result = await geminiService.analyzeData(data, options.analysisType)
      break

    case "validate":
      result = await dataProcessor.validateData(data, options?.schema)
      break

    case "process":
      if (!options?.instructions) {
        throw new ValidationError("instructions are required for process operation")
      }
      const { geminiService: gemini } = await import("@/lib/gemini")
      result = await gemini.processStructuredData(data, options.instructions)
      break

    default:
      throw new ValidationError(`Unsupported operation: ${operation}`)
  }

  return NextResponse.json({
    success: true,
    data: {
      operation,
      input: data,
      result,
      timestamp: new Date().toISOString(),
    },
  })
}

export const POST = withErrorHandling(handler, "data-process")
