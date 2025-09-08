import { NextResponse } from "next/server"

/**
 * Custom error classes for different types of errors
 */
export class APIError extends Error {
  constructor(
    message: string,
    public statusCode = 500,
    public code?: string,
  ) {
    super(message)
    this.name = "APIError"
  }
}

export class ValidationError extends APIError {
  constructor(
    message: string,
    public field?: string,
  ) {
    super(message, 400, "VALIDATION_ERROR")
    this.name = "ValidationError"
  }
}

export class GeminiError extends APIError {
  constructor(message: string) {
    super(message, 503, "GEMINI_ERROR")
    this.name = "GeminiError"
  }
}

export class DataProcessingError extends APIError {
  constructor(message: string) {
    super(message, 422, "DATA_PROCESSING_ERROR")
    this.name = "DataProcessingError"
  }
}

/**
 * Error Handler Service
 * Provides centralized error handling and logging
 */
export class ErrorHandler {
  /**
   * Handle API errors and return appropriate response
   * @param error - The error to handle
   * @param context - Additional context about where the error occurred
   * @returns NextResponse with error details
   */
  static handleAPIError(error: unknown, context?: string): NextResponse {
    console.error(`[ERROR${context ? ` - ${context}` : ""}]:`, error)

    if (error instanceof APIError) {
      return NextResponse.json(
        {
          error: {
            message: error.message,
            code: error.code,
            statusCode: error.statusCode,
            timestamp: new Date().toISOString(),
            context,
          },
        },
        { status: error.statusCode },
      )
    }

    if (error instanceof Error) {
      return NextResponse.json(
        {
          error: {
            message: error.message,
            code: "INTERNAL_ERROR",
            statusCode: 500,
            timestamp: new Date().toISOString(),
            context,
          },
        },
        { status: 500 },
      )
    }

    return NextResponse.json(
      {
        error: {
          message: "An unknown error occurred",
          code: "UNKNOWN_ERROR",
          statusCode: 500,
          timestamp: new Date().toISOString(),
          context,
        },
      },
      { status: 500 },
    )
  }

  /**
   * Validate request data
   * @param data - Data to validate
   * @param requiredFields - Array of required field names
   * @throws ValidationError if validation fails
   */
  static validateRequest(data: any, requiredFields: string[]): void {
    if (!data || typeof data !== "object") {
      throw new ValidationError("Request body must be a valid object")
    }

    for (const field of requiredFields) {
      if (!(field in data) || data[field] === null || data[field] === undefined) {
        throw new ValidationError(`Missing required field: ${field}`, field)
      }
    }
  }

  /**
   * Validate environment variables
   * @param requiredEnvVars - Array of required environment variable names
   * @throws APIError if validation fails
   */
  static validateEnvironment(requiredEnvVars: string[]): void {
    const missing = requiredEnvVars.filter((envVar) => !process.env[envVar])

    if (missing.length > 0) {
      throw new APIError(`Missing required environment variables: ${missing.join(", ")}`, 500, "MISSING_ENV_VARS")
    }
  }

  /**
   * Log error with structured format
   * @param error - Error to log
   * @param context - Additional context
   * @param level - Log level
   */
  static logError(error: unknown, context?: string, level: "error" | "warn" | "info" = "error"): void {
    const logData = {
      timestamp: new Date().toISOString(),
      level,
      context,
      error:
        error instanceof Error
          ? {
              name: error.name,
              message: error.message,
              stack: error.stack,
            }
          : error,
    }

    console[level]("[STRUCTURED_LOG]:", JSON.stringify(logData, null, 2))
  }

  /**
   * Wrap async functions with error handling
   * @param fn - Async function to wrap
   * @param context - Context for error logging
   * @returns Wrapped function
   */
  static wrapAsync<T extends any[], R>(fn: (...args: T) => Promise<R>, context?: string) {
    return async (...args: T): Promise<R> => {
      try {
        return await fn(...args)
      } catch (error) {
        ErrorHandler.logError(error, context)
        throw error
      }
    }
  }
}

/**
 * Middleware function for API route error handling
 */
export function withErrorHandling(handler: (request: Request) => Promise<NextResponse>, context?: string) {
  return async (request: Request): Promise<NextResponse> => {
    try {
      return await handler(request)
    } catch (error) {
      return ErrorHandler.handleAPIError(error, context)
    }
  }
}
