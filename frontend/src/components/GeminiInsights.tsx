import React, { useState, useEffect } from 'react';
import { getGeminiInsights } from '../utils/api';

interface GeminiInsightsProps {
  simulationData: any;
}

export const GeminiInsights: React.FC<GeminiInsightsProps> = ({ simulationData }) => {
  const [activeTab, setActiveTab] = useState<'technical' | 'patient'>('technical');
  const [insights, setInsights] = useState<{ technical: string; patient: string } | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(null);

  useEffect(() => {
    if (simulationData) {
      fetchInsights();
    }
  }, [simulationData]);

  const fetchInsights = async () => {
    if (!simulationData) return;

    setIsLoading(true);
    setError(null);

    try {
      const response = await getGeminiInsights(
        simulationData,
        undefined,
        conversationId || undefined
      );
      setInsights({
        technical: response.technical_summary,
        patient: response.patient_summary,
      });
      setConversationId(response.conversation_id);
    } catch (err: any) {
      setError(err.message || 'Failed to generate insights');
    } finally {
      setIsLoading(false);
    }
  };

  if (!simulationData) {
    return (
      <div className="h-full flex items-center justify-center p-6">
        <div className="text-center">
          <svg
            className="w-16 h-16 mx-auto text-gray-300 mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
            />
          </svg>
          <p className="text-sm text-gray-500">
            Run a simulation to see AI-generated insights
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      <div className="border-b border-gray-200 px-4 py-3">
        <h3 className="text-sm font-semibold text-gray-800 mb-2">AI Insights</h3>
        <div className="flex space-x-1">
          <button
            onClick={() => setActiveTab('technical')}
            className={`px-3 py-1.5 text-xs font-medium rounded transition-colors ${
              activeTab === 'technical'
                ? 'bg-medical-blue text-white'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            Technical
          </button>
          <button
            onClick={() => setActiveTab('patient')}
            className={`px-3 py-1.5 text-xs font-medium rounded transition-colors ${
              activeTab === 'patient'
                ? 'bg-medical-blue text-white'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            Patient
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        {isLoading ? (
          <div className="flex flex-col items-center justify-center h-full space-y-3">
            <div className="w-8 h-8 border-2 border-medical-blue border-t-transparent rounded-full animate-spin"></div>
            <p className="text-sm text-gray-600">Generating insights...</p>
          </div>
        ) : error ? (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3">
            <p className="text-sm text-red-700">{error}</p>
            <button
              onClick={fetchInsights}
              className="mt-2 text-sm text-red-600 hover:underline"
            >
              Try again
            </button>
          </div>
        ) : insights ? (
          <div className="prose prose-sm max-w-none">
            <p className="text-sm text-gray-700 whitespace-pre-wrap leading-relaxed">
              {activeTab === 'technical' ? insights.technical : insights.patient}
            </p>
          </div>
        ) : null}
      </div>

      {insights && (
        <div className="border-t border-gray-200 px-4 py-3">
          <button
            onClick={fetchInsights}
            disabled={isLoading}
            className="w-full text-xs text-medical-blue hover:underline disabled:opacity-50"
          >
            Regenerate Insights
          </button>
        </div>
      )}
    </div>
  );
};
