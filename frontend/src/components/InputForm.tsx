"use client";

import { useState } from "react";
import { ConversationRequest } from "@/lib/api";
import {
  TOPIC_CATEGORIES,
  AUDIENCE_TYPES,
  TONE_MODES,
  CONTEXT_TYPES,
  USER_ROLES,
} from "@/lib/constants";

interface Props {
  onSubmit: (request: ConversationRequest) => void;
  loading: boolean;
}

export default function InputForm({ onSubmit, loading }: Props) {
  const [form, setForm] = useState({
    topic_category: "technology",
    custom_topic: "",
    audience_type: "unknown",
    tone: "casual",
    context: "meeting",
    location: "",
    duration_minutes: "",
    user_role: "",
    audience_size: "",
  });

  const set = (key: string, value: string) =>
    setForm((prev) => ({ ...prev, [key]: value }));

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const req: ConversationRequest = {
      topic_category: form.topic_category,
      audience_type: form.audience_type,
      tone: form.tone,
      context: form.context,
    };
    if (form.topic_category === "custom" && form.custom_topic) {
      req.custom_topic = form.custom_topic;
    }
    if (form.location) req.location = form.location;
    if (form.duration_minutes) req.duration_minutes = parseInt(form.duration_minutes);
    if (form.user_role) req.user_role = form.user_role;
    if (form.audience_size) req.audience_size = parseInt(form.audience_size);
    onSubmit(req);
  };

  return (
    <form onSubmit={handleSubmit} className="card space-y-6">
      <h2 className="text-xl font-bold text-gray-900">Configure Your Conversation</h2>

      {/* Required fields */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
        <div>
          <label className="label">Topic Category *</label>
          <select
            className="select-field"
            value={form.topic_category}
            onChange={(e) => set("topic_category", e.target.value)}
          >
            {TOPIC_CATEGORIES.map((o) => (
              <option key={o.value} value={o.value}>{o.label}</option>
            ))}
          </select>
        </div>

        {form.topic_category === "custom" && (
          <div>
            <label className="label">Custom Topic</label>
            <input
              className="input-field"
              placeholder="e.g., AI in Healthcare"
              value={form.custom_topic}
              onChange={(e) => set("custom_topic", e.target.value)}
            />
          </div>
        )}

        <div>
          <label className="label">Audience Type *</label>
          <select
            className="select-field"
            value={form.audience_type}
            onChange={(e) => set("audience_type", e.target.value)}
          >
            {AUDIENCE_TYPES.map((o) => (
              <option key={o.value} value={o.value}>{o.label}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="label">Tone / Mode *</label>
          <select
            className="select-field"
            value={form.tone}
            onChange={(e) => set("tone", e.target.value)}
          >
            {TONE_MODES.map((o) => (
              <option key={o.value} value={o.value}>{o.label}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="label">Context *</label>
          <select
            className="select-field"
            value={form.context}
            onChange={(e) => set("context", e.target.value)}
          >
            {CONTEXT_TYPES.map((o) => (
              <option key={o.value} value={o.value}>{o.label}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Optional fields */}
      <details className="group">
        <summary className="cursor-pointer text-sm font-medium text-primary-600 hover:text-primary-700">
          Optional Settings
        </summary>
        <div className="mt-4 grid grid-cols-1 gap-5 sm:grid-cols-2 animate-fade-in">
          <div>
            <label className="label">Location</label>
            <input
              className="input-field"
              placeholder="e.g., New York"
              value={form.location}
              onChange={(e) => set("location", e.target.value)}
            />
          </div>
          <div>
            <label className="label">Duration (minutes)</label>
            <input
              className="input-field"
              type="number"
              min={5}
              max={480}
              placeholder="e.g., 30"
              value={form.duration_minutes}
              onChange={(e) => set("duration_minutes", e.target.value)}
            />
          </div>
          <div>
            <label className="label">Your Role</label>
            <select
              className="select-field"
              value={form.user_role}
              onChange={(e) => set("user_role", e.target.value)}
            >
              {USER_ROLES.map((o) => (
                <option key={o.value} value={o.value}>{o.label}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="label">Audience Size</label>
            <input
              className="input-field"
              type="number"
              min={1}
              placeholder="e.g., 50"
              value={form.audience_size}
              onChange={(e) => set("audience_size", e.target.value)}
            />
          </div>
        </div>
      </details>

      <button type="submit" className="btn-primary w-full" disabled={loading}>
        {loading ? (
          <span className="flex items-center gap-2">
            <span className="loading-dot" />
            <span className="loading-dot" />
            <span className="loading-dot" />
            <span className="ml-2">Generating Strategy...</span>
          </span>
        ) : (
          "Generate Conversation Strategy"
        )}
      </button>
    </form>
  );
}
