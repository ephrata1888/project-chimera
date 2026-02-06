import json
import os

import jsonschema


HERE = os.path.dirname(__file__)
SCHEMA_DIR = os.path.abspath(os.path.join(HERE, '..', '..', 'specs', 'schemas'))


def load_schema(name):
    path = os.path.join(SCHEMA_DIR, name)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def test_schemas_are_valid_jsonschema():
    # load each schema and validate it is itself a valid draft-07 schema
    names = [
        'fetch_trends.schema.json',
        'generate_content.schema.json',
        'validate_content.schema.json',
        'publish_content.schema.json',
        'agent_status.schema.json',
    ]
    for n in names:
        schema = load_schema(n)
        # jsonschema provides a Draft7Validator to check schema validity
        jsonschema.Draft7Validator.check_schema(schema)


def test_example_payloads_validate():
    # Basic example payloads that should validate against the schemas
    fetch_example = {
        "source": "twitter",
        "timestamp": "2026-02-06T12:00:00Z",
        "trends": [{"name": "topic1", "score": 0.9}]
    }
    generate_example = {"prompt": "Short explainer about AI", "style": "casual", "length_seconds": 30}
    validate_example = {"content_id": "c1", "content": "hello world", "checks": ["toxicity"], "status": "pending"}
    publish_example = {"content_id": "c1", "channels": ["twitter"]}
    agent_example = {"agent_id": "planner-1", "uptime_seconds": 3600, "last_heartbeat": "2026-02-06T12:00:00Z", "state": "idle"}

    jsonschema.validate(fetch_example, load_schema('fetch_trends.schema.json'))
    jsonschema.validate(generate_example, load_schema('generate_content.schema.json'))
    jsonschema.validate(validate_example, load_schema('validate_content.schema.json'))
    jsonschema.validate(publish_example, load_schema('publish_content.schema.json'))
    jsonschema.validate(agent_example, load_schema('agent_status.schema.json'))
