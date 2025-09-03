import { useState } from "react";
import { type GrammarError } from "@shared/schema";
import { cn } from "@/lib/utils";

interface ErrorHighlightProps {
  error: GrammarError;
  children: React.ReactNode;
  onAcceptSuggestion: (errorId: string, suggestion: string) => void;
}

export function ErrorHighlight({ error, children, onAcceptSuggestion }: ErrorHighlightProps) {
  const [showTooltip, setShowTooltip] = useState(false);

  const getErrorColor = (type: string) => {
    switch (type) {
      case "grammar":
        return "bg-red-100 border-b-2 border-red-500";
      case "spelling":
        return "bg-yellow-100 border-b-2 border-yellow-500";
      case "punctuation":
        return "bg-blue-100 border-b-2 border-blue-500";
      default:
        return "bg-gray-100 border-b-2 border-gray-500";
    }
  };

  const getErrorIcon = (type: string) => {
    switch (type) {
      case "grammar":
        return "fas fa-exclamation-circle text-red-500";
      case "spelling":
        return "fas fa-spell-check text-yellow-500";
      case "punctuation":
        return "fas fa-question-circle text-blue-500";
      default:
        return "fas fa-info-circle text-gray-500";
    }
  };

  return (
    <span
      className={cn(
        "relative cursor-pointer",
        getErrorColor(error.type)
      )}
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
    >
      {children}
      {showTooltip && (
        <div className="absolute bottom-full left-0 mb-2 p-3 bg-white border border-slate-200 rounded-lg shadow-lg z-50 min-w-[200px]">
          <div className="flex items-start gap-2 mb-2">
            <i className={cn("text-sm", getErrorIcon(error.type))} />
            <div className="flex-1">
              <div className="font-semibold text-slate-800 text-sm capitalize">
                {error.type} Error
              </div>
              <div className="text-xs text-slate-600 mt-1">
                {error.message}
              </div>
            </div>
          </div>
          {error.suggestion && (
            <div className="mt-3 pt-3 border-t border-slate-100">
              <div className="text-xs font-medium text-slate-700 mb-2">
                Suggestion:
              </div>
              <button
                onClick={() => onAcceptSuggestion(error.id, error.suggestion)}
                className="text-blue-600 hover:bg-blue-50 px-2 py-1 rounded text-sm border border-blue-200 hover:border-blue-300 transition-colors"
              >
                {error.suggestion}
              </button>
            </div>
          )}
        </div>
      )}
    </span>
  );
}
