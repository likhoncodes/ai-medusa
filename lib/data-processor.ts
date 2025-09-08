import { geminiService } from "./gemini"

/**
 * Data Processing Service
 * Handles various data transformation and processing operations
 */
export class DataProcessor {
  /**
   * Transform data based on specified transformation type
   * @param data - Input data to transform
   * @param transformationType - Type of transformation to apply
   * @returns Transformed data
   */
  async transformData(data: any, transformationType: "normalize" | "aggregate" | "filter" | "enrich"): Promise<any> {
    try {
      switch (transformationType) {
        case "normalize":
          return this.normalizeData(data)
        case "aggregate":
          return this.aggregateData(data)
        case "filter":
          return this.filterData(data)
        case "enrich":
          return this.enrichData(data)
        default:
          throw new Error(`Unknown transformation type: ${transformationType}`)
      }
    } catch (error) {
      throw new Error(`Data transformation failed: ${error instanceof Error ? error.message : "Unknown error"}`)
    }
  }

  /**
   * Normalize data structure and format
   */
  private async normalizeData(data: any): Promise<any> {
    if (Array.isArray(data)) {
      return data.map((item) => this.normalizeObject(item))
    } else if (typeof data === "object" && data !== null) {
      return this.normalizeObject(data)
    }
    return data
  }

  /**
   * Normalize individual object
   */
  private normalizeObject(obj: any): any {
    const normalized: any = {}

    for (const [key, value] of Object.entries(obj)) {
      // Convert keys to camelCase
      const normalizedKey = key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase())

      // Handle different value types
      if (typeof value === "string") {
        normalized[normalizedKey] = value.trim()
      } else if (typeof value === "number") {
        normalized[normalizedKey] = Number(value)
      } else if (value instanceof Date) {
        normalized[normalizedKey] = value.toISOString()
      } else {
        normalized[normalizedKey] = value
      }
    }

    return normalized
  }

  /**
   * Aggregate data based on common patterns
   */
  private async aggregateData(data: any): Promise<any> {
    if (!Array.isArray(data)) {
      throw new Error("Aggregation requires array input")
    }

    const aggregated = {
      count: data.length,
      summary: await geminiService.analyzeData(data, "summary"),
      statistics: this.calculateStatistics(data),
      timestamp: new Date().toISOString(),
    }

    return aggregated
  }

  /**
   * Filter data based on AI-powered analysis
   */
  private async filterData(data: any): Promise<any> {
    const instructions = "Filter out any irrelevant, duplicate, or low-quality data entries"
    return await geminiService.processStructuredData(data, instructions)
  }

  /**
   * Enrich data with additional context using AI
   */
  private async enrichData(data: any): Promise<any> {
    const instructions = "Enrich this data with additional context, insights, and relevant information"
    return await geminiService.processStructuredData(data, instructions)
  }

  /**
   * Calculate basic statistics for numerical data
   */
  private calculateStatistics(data: any[]): any {
    const numericalFields: { [key: string]: number[] } = {}

    // Extract numerical fields
    data.forEach((item) => {
      if (typeof item === "object" && item !== null) {
        Object.entries(item).forEach(([key, value]) => {
          if (typeof value === "number") {
            if (!numericalFields[key]) {
              numericalFields[key] = []
            }
            numericalFields[key].push(value)
          }
        })
      }
    })

    // Calculate statistics for each numerical field
    const statistics: any = {}
    Object.entries(numericalFields).forEach(([field, values]) => {
      statistics[field] = {
        count: values.length,
        sum: values.reduce((a, b) => a + b, 0),
        average: values.reduce((a, b) => a + b, 0) / values.length,
        min: Math.min(...values),
        max: Math.max(...values),
      }
    })

    return statistics
  }

  /**
   * Validate data structure and content
   * @param data - Data to validate
   * @param schema - Optional validation schema
   * @returns Validation result
   */
  async validateData(data: any, schema?: any): Promise<{ isValid: boolean; errors: string[]; warnings: string[] }> {
    const errors: string[] = []
    const warnings: string[] = []

    try {
      // Basic validation
      if (data === null || data === undefined) {
        errors.push("Data is null or undefined")
      }

      // Use AI for advanced validation if no schema provided
      if (!schema && data) {
        const validationPrompt = `
          Analyze the following data for potential issues, inconsistencies, or quality problems:
          ${JSON.stringify(data, null, 2)}
          
          Please identify any:
          1. Data quality issues
          2. Inconsistent formats
          3. Missing required fields
          4. Invalid values
          5. Potential security concerns
        `

        const aiValidation = await geminiService.generateText(validationPrompt)

        // Parse AI response for issues (simplified approach)
        if (aiValidation.toLowerCase().includes("issue") || aiValidation.toLowerCase().includes("problem")) {
          warnings.push(`AI detected potential issues: ${aiValidation}`)
        }
      }

      return {
        isValid: errors.length === 0,
        errors,
        warnings,
      }
    } catch (error) {
      errors.push(`Validation failed: ${error instanceof Error ? error.message : "Unknown error"}`)
      return { isValid: false, errors, warnings }
    }
  }
}

// Export singleton instance
export const dataProcessor = new DataProcessor()
