"use client";

import { useState, useRef } from "react";
import toast from "react-hot-toast";
import InputForm from "@/components/InputForm";
import ResultsDashboard from "@/components/ResultsDashboard";
import RefinePanel from "@/components/RefinePanel";
import {
  ConversationRequest,
  ConversationResponse,
  generatePlan,
  refinePlan,
  getExportUrl,
} from "@/lib/api";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ConversationResponse | null>(null);
  const [lastRequest, setLastRequest] = useState<ConversationRequest | null>(null);
  const resultsRef = useRef<HTMLDivElement>(null);

  const handleGenerate = async (request: ConversationRequest) => {
    setLoading(true);
    setLastRequest(request);
    try {
      const data = await generatePlan(request);
      setResult(data);
      setTimeout(() => resultsRef.current?.scrollIntoView({ behavior: "smooth" }), 100);
      toast.success("Conversation strategy generated!");
    } catch (err: any) {
      toast.error(err.message || "Failed to generate plan");
    } finally {
      setLoading(false);
    }
  };

  const handleRefine = async (feedback: string, section?: string) => {
    if (!result) return;
    setLoading(true);
    try {
      const data = await refinePlan(result.session_id, feedback, section);
      setResult(data);
      toast.success("Plan refined successfully!");
    } catch (err: any) {
      toast.error(err.message || "Failed to refine plan");
    } finally {
      setLoading(false);
    }
  };

  const handleRegenerate = () => {
    if (lastRequest) handleGenerate(lastRequest);
  };

  const handleExport = () => {
    if (result) {
      window.open(getExportUrl(result.session_id), "_blank");
    }
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="border-b border-gray-200 bg-white">
        <div className="mx-auto max-w-6xl px-4 py-6">
          <h1 className="text-2xl font-bold text-gray-900 sm:text-3xl">
            Conversation Intelligence Agent
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            AI-powered conversation strategies for meetings, conferences, and gatherings
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="mx-auto max-w-6xl px-4 py-8 space-y-8">
        <InputForm onSubmit={handleGenerate} loading={loading} />

        {result && (
          <div ref={resultsRef} className="space-y-8 animate-fade-in">
            <div className="grid grid-cols-1 gap-8 lg:grid-cols-[1fr_320px]">
              <ResultsDashboard plan={result.plan} />
              <div className="lg:sticky lg:top-8 lg:self-start">
                <RefinePanel
                  onRefine={handleRefine}
                  onRegenerate={handleRegenerate}
                  onExport={handleExport}
                  loading={loading}
                />
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-white mt-12">
        <div className="mx-auto max-w-6xl px-4 py-6 text-center text-sm text-gray-500">
          Conversation Intelligence Agent &mdash; Powered by AI
        </div>
      </footer>
    </div>
  );
}
