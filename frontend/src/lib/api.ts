const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ConversationRequest {
  topic_category: string;
  custom_topic?: string;
  audience_type: string;
  tone: string;
  context: string;
  location?: string;
  duration_minutes?: number;
  user_role?: string;
  audience_size?: number;
}

export interface Reactions {
  agreement: string[];
  disagreement: string[];
  silence: string[];
  confusion: string[];
}

export interface ConversationPlan {
  opening_lines: string[];
  topic_flow: string[];
  questions: string[];
  reactions: Reactions;
  engagement_strategies: string[];
  fun_elements: string[];
  facts: string[];
  recent_topics: string[];
  transition_phrases: string[];
  poll_ideas: string[];
}

export interface ConversationResponse {
  session_id: string;
  plan: ConversationPlan;
  metadata: Record<string, string>;
}

export async function generatePlan(request: ConversationRequest): Promise<ConversationResponse> {
  const resp = await fetch(`${API_BASE}/api/v1/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
  if (!resp.ok) {
    const err = await resp.text();
    throw new Error(`Generation failed: ${err}`);
  }
  return resp.json();
}

export async function refinePlan(sessionId: string, feedback: string, section?: string): Promise<ConversationResponse> {
  const resp = await fetch(`${API_BASE}/api/v1/refine`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, feedback, section }),
  });
  if (!resp.ok) {
    const err = await resp.text();
    throw new Error(`Refinement failed: ${err}`);
  }
  return resp.json();
}

export function getExportUrl(sessionId: string): string {
  return `${API_BASE}/api/v1/export/${sessionId}`;
}
