export const TOPIC_CATEGORIES = [
  { value: "technology", label: "Technology" },
  { value: "current_affairs", label: "Current Affairs" },
  { value: "business", label: "Business" },
  { value: "personal_social", label: "Personal / Social" },
  { value: "entertainment", label: "Entertainment" },
  { value: "custom", label: "Custom" },
] as const;

export const AUDIENCE_TYPES = [
  { value: "friends", label: "Friends" },
  { value: "unknown", label: "Unknown People" },
  { value: "new_group", label: "New Group" },
  { value: "public", label: "Public Audience" },
  { value: "formal", label: "Restrictive / Formal" },
  { value: "technical", label: "Technical Audience" },
  { value: "family", label: "Family" },
] as const;

export const TONE_MODES = [
  { value: "serious", label: "Serious" },
  { value: "technical", label: "Technical" },
  { value: "funny", label: "Funny" },
  { value: "casual", label: "Casual" },
  { value: "informative", label: "Informative" },
  { value: "ice_breaker", label: "Ice-breaker" },
  { value: "networking", label: "Networking" },
] as const;

export const CONTEXT_TYPES = [
  { value: "meeting", label: "Meeting" },
  { value: "conference", label: "Conference" },
  { value: "party", label: "Party / Gathering" },
  { value: "interview", label: "Interview" },
  { value: "panel", label: "Panel Discussion" },
  { value: "workshop", label: "Workshop" },
] as const;

export const USER_ROLES = [
  { value: "", label: "Not specified" },
  { value: "speaker", label: "Speaker" },
  { value: "attendee", label: "Attendee" },
  { value: "host", label: "Host" },
] as const;
