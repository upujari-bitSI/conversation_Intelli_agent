"use client";

import { useState } from "react";

interface Props {
  onRefine: (feedback: string, section?: string) => void;
  onRegenerate: () => void;
  onExport: () => void;
  loading: boolean;
}

const SECTIONS = [
  { value: "", label: "Entire plan" },
  { value: "opening_lines", label: "Icebreakers" },
  { value: "topic_flow", label: "Topic Flow" },
  { value: "questions", label: "Questions" },
  { value: "engagement_strategies", label: "Engagement" },
  { value: "reactions", label: "Reactions" },
  { value: "fun_elements", label: "Fun Elements" },
];

export default function RefinePanel({ onRefine, onRegenerate, onExport, loading }: Props) {
  const [feedback, setFeedback] = useState("");
  const [section, setSection] = useState("");

  const handleRefine = (e: React.FormEvent) => {
    e.preventDefault();
    if (!feedback.trim()) return;
    onRefine(feedback, section || undefined);
    setFeedback("");
  };

  return (
    <div className="card space-y-4">
      <h3 className="text-lg font-semibold text-gray-900">Refine & Actions</h3>

      <form onSubmit={handleRefine} className="space-y-3">
        <div>
          <label className="label">Feedback</label>
          <textarea
            className="input-field min-h-[80px] resize-y"
            placeholder="e.g., Make the tone more humorous, add tech industry references..."
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
          />
        </div>
        <div>
          <label className="label">Focus Section</label>
          <select
            className="select-field"
            value={section}
            onChange={(e) => setSection(e.target.value)}
          >
            {SECTIONS.map((s) => (
              <option key={s.value} value={s.value}>{s.label}</option>
            ))}
          </select>
        </div>
        <button type="submit" className="btn-primary w-full" disabled={loading || !feedback.trim()}>
          {loading ? "Refining..." : "Refine Plan"}
        </button>
      </form>

      <div className="flex gap-3">
        <button onClick={onRegenerate} className="btn-secondary flex-1" disabled={loading}>
          Regenerate
        </button>
        <button onClick={onExport} className="btn-secondary flex-1">
          Export PDF
        </button>
      </div>
    </div>
  );
}
