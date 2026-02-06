-- Initial schema for Project Chimera
-- Compatible with PostgreSQL; adapt types if using another DB

CREATE TABLE agents (
  agent_id UUID PRIMARY KEY,
  name TEXT NOT NULL,
  role TEXT NOT NULL,
  state TEXT NOT NULL,
  last_heartbeat TIMESTAMPTZ,
  metrics JSONB
);

CREATE TABLE content (
  id UUID PRIMARY KEY,
  title TEXT,
  body TEXT NOT NULL,
  metadata JSONB,
  status TEXT NOT NULL,
  agent_id UUID REFERENCES agents(agent_id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE validation (
  id UUID PRIMARY KEY,
  content_id UUID REFERENCES content(id) ON DELETE CASCADE,
  checker TEXT NOT NULL,
  status TEXT NOT NULL,
  issues JSONB,
  checked_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE publish_log (
  id UUID PRIMARY KEY,
  content_id UUID REFERENCES content(id) ON DELETE CASCADE,
  channel TEXT NOT NULL,
  scheduled_at TIMESTAMPTZ,
  published_at TIMESTAMPTZ,
  status TEXT NOT NULL,
  response JSONB
);

-- Indexes
CREATE INDEX idx_content_status ON content(status);
CREATE INDEX idx_agent_state ON agents(state);
