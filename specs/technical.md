# Project Chimera — Technical Specification

## Agent API Contracts

### Generate Content — Request

```json
{
  "agent_id": "string",
  "persona": "string",
  "trend": {
    "topic": "string",
    "source": "string"
  }
}
```

### Generate Content — Response

```json
{
  "content_id": "string",
  "caption": "string",
  "confidence_score": 0.0,
  "flags": ["string"]
}
```

---

## Database Schema — Video Metadata

```mermaid
erDiagram
    AGENT ||--o{ CONTENT : creates
    CONTENT ||--o{ PUBLISH_LOG : publishes

    AGENT {
        string agent_id
        string role
        string persona
    }

    CONTENT {
        string content_id
        string caption
        float confidence_score
        string status
    }

    PUBLISH_LOG {
        string publish_id
        datetime timestamp
        string platform
        string result
    }
```

---

## Data Rules

* All content must have a confidence score
* Status transitions must be logged
* Publishing results must be auditable
