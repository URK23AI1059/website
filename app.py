import OpenAI from "openai";
import { type GrammarError, type GrammarCheckResult } from "@shared/schema";
import { randomUUID } from "crypto";

// the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
const openai = new OpenAI({ 
  apiKey: process.env.OPENAI_API_KEY || process.env.OPENAI_API_KEY_ENV_VAR || "default_key"
});

export async function checkGrammar(text: string): Promise<GrammarCheckResult> {
  const startTime = Date.now();
  
  try {
    const response = await openai.chat.completions.create({
      model: "gpt-4o",
      messages: [
        {
          role: "system",
          content: `You are a professional grammar, spelling, and punctuation checker. Analyze the provided text and identify all errors. For each error, provide:
          - type: "grammar", "spelling", or "punctuation"
          - message: A clear explanation of the error
          - suggestion: The corrected text
          - startIndex: Character position where error starts (0-based)
          - endIndex: Character position where error ends (0-based)
          - originalText: The original incorrect text

          Respond with JSON in this exact format:
          {
            "errors": [
              {
                "type": "grammar|spelling|punctuation",
                "message": "explanation of error",
                "suggestion": "corrected text",
                "startIndex": number,
                "endIndex": number,
                "originalText": "incorrect text"
              }
            ]
          }

          Be thorough but only identify genuine errors. Provide accurate character indices.`
        },
        {
          role: "user",
          content: `Please check this text for grammar, spelling, and punctuation errors: "${text}"`
        }
      ],
      response_format: { type: "json_object" },
    });

    const result = JSON.parse(response.choices[0].message.content || "{}");
    const errors: GrammarError[] = (result.errors || []).map((error: any) => ({
      id: randomUUID(),
      type: error.type,
      message: error.message,
      suggestion: error.suggestion,
      startIndex: error.startIndex,
      endIndex: error.endIndex,
      originalText: error.originalText,
    }));

    const processingTime = (Date.now() - startTime) / 1000;
    
    // Calculate error counts
    const grammarErrors = errors.filter(e => e.type === "grammar").length;
    const spellingErrors = errors.filter(e => e.type === "spelling").length;
    const punctuationErrors = errors.filter(e => e.type === "punctuation").length;
    const totalErrors = errors.length;
    
    // Calculate accuracy score (percentage of text without errors)
    const errorCharacters = errors.reduce((sum, error) => sum + (error.endIndex - error.startIndex), 0);
    const accuracyScore = Math.max(0, Math.round(((text.length - errorCharacters) / text.length) * 100));

    return {
      text,
      errors,
      summary: {
        totalErrors,
        grammarErrors,
        spellingErrors,
        punctuationErrors,
        accuracyScore,
        processingTime,
      },
    };
  } catch (error) {
    throw new Error("Failed to check grammar: " + (error as Error).message);
  }
}
