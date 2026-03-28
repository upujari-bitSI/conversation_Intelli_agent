"use client";

import { useState } from "react";
import { ConversationPlan } from "@/lib/api";
import {
  FiMessageCircle,
  FiList,
  FiHelpCircle,
  FiZap,
  FiSmile,
  FiBookOpen,
  FiTrendingUp,
  FiArrowRight,
  FiBarChart2,
  FiMessageSquare,
} from "react-icons/fi";

interface Props {
  plan: ConversationPlan;
}

interface SectionProps {
  title: string;
  icon: React.ReactNode;
  items: string[];
  color: string;
}

function Section({ title, icon, items, color }: SectionProps) {
  if (!items || items.length === 0) return null;
  return (
    <div className="card animate-fade-in">
      <div className="flex items-center gap-2 mb-4">
        <span className={`flex h-8 w-8 items-center justify-center rounded-lg ${color} text-white`}>
          {icon}
        </span>
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
      </div>
      <ul className="space-y-2">
        {items.map((item, i) => (
          <li key={i} className="flex items-start gap-2 text-sm text-gray-700">
            <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-gray-400" />
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

function ReactionsSection({ reactions }: { reactions: ConversationPlan["reactions"] }) {
  const types = [
    { key: "agreement" as const, label: "Agreement", color: "text-green-600" },
    { key: "disagreement" as const, label: "Disagreement", color: "text-red-500" },
    { key: "silence" as const, label: "Silence", color: "text-yellow-600" },
    { key: "confusion" as const, label: "Confusion", color: "text-blue-500" },
  ];

  const hasAny = types.some((t) => reactions[t.key]?.length > 0);
  if (!hasAny) return null;

  return (
    <div className="card animate-fade-in">
      <div className="flex items-center gap-2 mb-4">
        <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-purple-500 text-white">
          <FiMessageSquare size={16} />
        </span>
        <h3 className="text-lg font-semibold text-gray-900">Reactions</h3>
      </div>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        {types.map(({ key, label, color }) =>
          reactions[key]?.length > 0 ? (
            <div key={key}>
              <h4 className={`text-sm font-semibold ${color} mb-2`}>{label}</h4>
              <ul className="space-y-1.5">
                {reactions[key].map((item, i) => (
                  <li key={i} className="text-sm text-gray-600">&ldquo;{item}&rdquo;</li>
                ))}
              </ul>
            </div>
          ) : null
        )}
      </div>
    </div>
  );
}

export default function ResultsDashboard({ plan }: Props) {
  const [copied, setCopied] = useState(false);

  const copyAll = () => {
    const text = JSON.stringify(plan, null, 2);
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-gray-900">Your Conversation Strategy</h2>
        <button onClick={copyAll} className="btn-secondary text-xs">
          {copied ? "Copied!" : "Copy JSON"}
        </button>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Section
          title="Icebreakers"
          icon={<FiMessageCircle size={16} />}
          items={plan.opening_lines}
          color="bg-primary-500"
        />
        <Section
          title="Topic Flow"
          icon={<FiList size={16} />}
          items={plan.topic_flow}
          color="bg-emerald-500"
        />
        <Section
          title="Questions"
          icon={<FiHelpCircle size={16} />}
          items={plan.questions}
          color="bg-amber-500"
        />
        <Section
          title="Engagement Strategies"
          icon={<FiZap size={16} />}
          items={plan.engagement_strategies}
          color="bg-rose-500"
        />
        <Section
          title="Fun Elements"
          icon={<FiSmile size={16} />}
          items={plan.fun_elements}
          color="bg-pink-500"
        />
        <Section
          title="Facts"
          icon={<FiBookOpen size={16} />}
          items={plan.facts}
          color="bg-cyan-500"
        />
        <Section
          title="Recent Topics"
          icon={<FiTrendingUp size={16} />}
          items={plan.recent_topics}
          color="bg-indigo-500"
        />
        <Section
          title="Transition Phrases"
          icon={<FiArrowRight size={16} />}
          items={plan.transition_phrases}
          color="bg-teal-500"
        />
        <Section
          title="Poll Ideas"
          icon={<FiBarChart2 size={16} />}
          items={plan.poll_ideas}
          color="bg-orange-500"
        />
        <ReactionsSection reactions={plan.reactions} />
      </div>
    </div>
  );
}
