## ERD — Project Chimera (Mermaid)

```mermaid
erDiagram
    CONTENT {
      UUID id PK "content id"
      string title
      text body
      json metadata
      string status
      timestamptz created_at
      timestamptz updated_at
      UUID agent_id FK "creator/owner agent"
    }

    AGENT {
      UUID agent_id PK
      string name
      string role
      string state
      timestamptz last_heartbeat
      json metrics
    }

    VALIDATION {
      UUID id PK
      UUID content_id FK
      string checker
      string status
      json issues
      timestamptz checked_at
    }

    PUBLISH_LOG {
      UUID id PK
      UUID content_id FK
      string channel
      timestamptz scheduled_at
      timestamptz published_at
      string status
      json response
    }

    AGENT ||--o{ CONTENT : creates
    CONTENT ||--o{ VALIDATION : has
    CONTENT ||--o{ PUBLISH_LOG : publishes
```

Notes:
- `UUID` denotes a stable unique identifier (GUID/UUID).
- `json` fields are for extensible metadata and integration payloads.
- `status` fields should use a finite set of states (e.g., draft/pending/approved/published/rejected).
