import { GoogleGenerativeAI } from "@google/generative-ai"

// Initialize Gemini AI client
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || "")

/**
 * Gemini AI Service
 * Provides methods for interacting with Google's Gemini AI model
 */
export class GeminiService {
  private model: any

  constructor(modelName = "gemini-1.5-flash") {
    this.model = genAI.getGenerativeModel({ model: modelName })
  }

  /**
   * Generate text content using Gemini AI
   * @param prompt - The input prompt for text generation
   * @param options - Additional generation options
   * @returns Generated text response
   */
  async generateText(
    prompt: string,
    options?: {
      temperature?: number
      maxOutputTokens?: number
      topP?: number
      topK?: number
    },
  ): Promise<string> {
    try {
      const generationConfig = {
        temperature: options?.temperature ?? 0.7,
        maxOutputTokens: options?.maxOutputTokens ?? 1000,
        topP: options?.topP ?? 0.8,
        topK: options?.topK ?? 40,
      }

      const result = await this.model.generateContent({
        contents: [{ role: "user", parts: [{ text: prompt }] }],
        generationConfig,
      })

      const response = await result.response
      return response.text()
    } catch (error) {
      throw new Error(`Gemini AI generation failed: ${error instanceof Error ? error.message : "Unknown error"}`)
    }
  }

  /**
   * Analyze and process data using Gemini AI
   * @param data - Data to be analyzed
   * @param analysisType - Type of analysis to perform
   * @returns Analysis results
   */
  async analyzeData(data: any, analysisType: "summary" | "sentiment" | "classification" | "extraction"): Promise<any> {
    try {
      const dataString = typeof data === "string" ? data : JSON.stringify(data)

      const prompts = {
        summary: `Please provide a comprehensive summary of the following data:\n\n${dataString}`,
        sentiment: `Analyze the sentiment of the following content and provide a detailed sentiment analysis:\n\n${dataString}`,
        classification: `Classify and categorize the following data into relevant categories:\n\n${dataString}`,
        extraction: `Extract key information, entities, and important details from the following data:\n\n${dataString}`,
      }

      const result = await this.generateText(prompts[analysisType])

      return {
        type: analysisType,
        input: data,
        analysis: result,
        timestamp: new Date().toISOString(),
      }
    } catch (error) {
      throw new Error(`Data analysis failed: ${error instanceof Error ? error.message : "Unknown error"}`)
    }
  }

  /**
   * Process structured data with custom instructions
   * @param data - Input data to process
   * @param instructions - Processing instructions
   * @returns Processed data
   */
  async processStructuredData(data: any, instructions: string): Promise<any> {
    try {
      const prompt = `
        Process the following data according to these instructions: ${instructions}
        
        Data:
        ${JSON.stringify(data, null, 2)}
        
        Please return the processed result in a structured format.
      `

      const result = await this.generateText(prompt)

      return {
        originalData: data,
        instructions,
        processedResult: result,
        timestamp: new Date().toISOString(),
      }
    } catch (error) {
      throw new Error(`Structured data processing failed: ${error instanceof Error ? error.message : "Unknown error"}`)
    }
  }
}

// Export singleton instance
export const geminiService = new GeminiService()
