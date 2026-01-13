# Glocal Policy Guardrail

An automated Policy-as-Code (PaC) framework for Smart TV/OTT platforms to manage global legal and cultural compliance risks.

## Overview

The Glocal Policy Guardrail framework provides automated pre-deployment validation of content against country-specific policies. It helps ensure that your Smart TV/OTT platform content complies with local regulations, cultural norms, and advertising restrictions before deployment.

## Features

### 1. Rule Engine
Python-based validator for country-specific content rules:
- Validates content metadata against policy configurations
- Checks forbidden content, categories, and keywords
- Enforces rating requirements
- Validates language availability (subtitles and audio)
- Returns PASS/REJECT status with detailed violation reports

### 2. Policy Configuration
YAML-based policy files for localized rules:
- **Korea**: Korean broadcast standards, KMRB ratings, Korean subtitle requirements
- **Saudi Arabia**: Islamic cultural guidelines, GCAM ratings, Arabic subtitle requirements
- Easily extensible for additional countries

### 3. Pre-deployment Checks
Automated validation returning clear PASS/REJECT status:
- Forbidden content detection
- Rating compliance verification
- Advertisement window restrictions
- Language requirement validation
- Cultural sensitivity warnings

### 4. FastAPI Integration
RESTful API for CI/CD pipeline integration:
- `/validate` - Validate content against a specific country policy
- `/validate/batch` - Validate against multiple countries simultaneously
- `/policies` - List available country policies
- `/health` - Health check endpoint

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/deokhwajeong/Glocal-Policy-Guardrail.git
cd Glocal-Policy-Guardrail
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. For development and testing:
```bash
pip install -r requirements-test.txt
```

## Quick Start

### Using the Python API

```python
from src.guardrail.rule_engine import RuleEngine

# Initialize the rule engine
engine = RuleEngine()

# Define your content metadata
content = {
    "title": "Family Adventure Movie",
    "description": "A heartwarming family adventure",
    "categories": ["family", "adventure"],
    "rating": "ALL",
    "duration_minutes": 90,
    "subtitle_languages": ["ko", "en"],
    "audio_languages": ["en"],
    "ad_breaks": [
        {"timestamp_seconds": 1800, "duration_seconds": 60}
    ]
}

# Validate against Korea policy
result = engine.validate_content(content, "korea")

if result.status.value == "PASS":
    print("✓ Content approved for deployment")
else:
    print("✗ Content rejected:")
    for violation in result.violations:
        print(f"  - {violation}")
```

### Using the FastAPI Server

1. Start the server:
```bash
python src/api.py
```

Or using uvicorn:
```bash
uvicorn src.api:app --reload
```

2. Access the API documentation:
```
http://localhost:8000/docs
```

3. Validate content via HTTP POST:
```bash
curl -X POST "http://localhost:8000/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "title": "Test Movie",
      "categories": ["action"],
      "rating": "15",
      "subtitle_languages": ["ko"],
      "ad_breaks": []
    },
    "country": "korea"
  }'
```

## Policy Configuration

Policies are defined in YAML files in the `policies/` directory. Each country has its own policy file.

### Korea Policy (`policies/korea.yaml`)
- Forbidden content: gambling, illegal drugs, extreme violence
- Ratings: ALL, 7, 12, 15, 19 (KMRB)
- Ad restrictions: Max 90s per break, 10min intervals, max 8/hour
- Language: Korean subtitles required

### Saudi Arabia Policy (`policies/saudi_arabia.yaml`)
- Forbidden content: alcohol, gambling, dating, LGBTQ, immodest content
- Ratings: G, PG, PG13, 15, 18 (GCAM)
- Ad restrictions: Max 60s per break, 15min intervals, max 6/hour
- Language: Arabic subtitles required

### Adding New Policies

Create a new YAML file in `policies/` directory:

```yaml
# policies/new_country.yaml
country_name: "Country Name"
country_code: "CC"

forbidden_content:
  keywords:
    - "forbidden_word"
  categories:
    - "forbidden_category"

rating_requirements:
  required: true
  allowed_ratings:
    - "G"
    - "PG"

ad_windows:
  max_duration_seconds: 90
  min_interval_seconds: 600
  max_per_hour: 8

language_requirements:
  required_subtitles:
    - "en"
```

## Content Metadata Format

```json
{
  "title": "Content Title",
  "description": "Content description",
  "categories": ["category1", "category2"],
  "tags": ["tag1", "tag2"],
  "rating": "PG13",
  "duration_minutes": 120,
  "subtitle_languages": ["ko", "en", "ar"],
  "audio_languages": ["en", "ko"],
  "ad_breaks": [
    {
      "timestamp_seconds": 600,
      "duration_seconds": 30
    }
  ]
}
```

## API Reference

### POST /validate
Validate content against a specific country policy.

**Request:**
```json
{
  "content": { /* content metadata */ },
  "country": "korea"
}
```

**Response:**
```json
{
  "status": "PASS" | "REJECT",
  "country": "korea",
  "violations": ["violation 1", "violation 2"],
  "warnings": ["warning 1"],
  "message": "Content approved for deployment in korea"
}
```

### POST /validate/batch
Validate content against multiple countries.

**Parameters:**
- `countries`: List of country codes

**Request Body:**
```json
{
  "title": "Content Title",
  "categories": ["documentary"],
  "rating": "G",
  ...
}
```

**Response:**
```json
{
  "results": {
    "korea": { "status": "PASS", ... },
    "saudi_arabia": { "status": "REJECT", ... }
  },
  "summary": {
    "total": 2,
    "passed": 1,
    "rejected": 1,
    "errors": 0
  }
}
```

### GET /policies
List available country policies.

**Response:**
```json
{
  "available_policies": ["korea", "saudi_arabia"],
  "count": 2
}
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_rule_engine.py

# Run with coverage
pytest --cov=src tests/
```

## Examples

The `examples/` directory contains sample code:

- `usage_examples.py` - Python API usage examples
- `api_client.py` - HTTP API client examples

Run examples:
```bash
# Python API examples
python examples/usage_examples.py

# API client examples (requires server running)
python examples/api_client.py
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Content Validation

on: [push]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Start Guardrail API
        run: |
          python src/api.py &
          sleep 5
      
      - name: Validate Content
        run: |
          curl -X POST http://localhost:8000/validate \
            -H "Content-Type: application/json" \
            -d @content.json \
            | jq -e '.status == "PASS"'
```

### Jenkins Example

```groovy
pipeline {
    agent any
    stages {
        stage('Validate Content') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python src/api.py &'
                sh 'sleep 5'
                sh '''
                    curl -X POST http://localhost:8000/validate \
                      -H "Content-Type: application/json" \
                      -d @content.json
                '''
            }
        }
    }
}
```

## Architecture

```
Glocal-Policy-Guardrail/
├── src/
│   ├── guardrail/
│   │   ├── __init__.py
│   │   └── rule_engine.py      # Core validation logic
│   └── api.py                   # FastAPI server
├── policies/
│   ├── korea.yaml              # Korea policy config
│   └── saudi_arabia.yaml       # Saudi Arabia policy config
├── tests/
│   ├── test_rule_engine.py     # Unit tests
│   └── test_api.py             # API integration tests
├── examples/
│   ├── usage_examples.py       # Python API examples
│   └── api_client.py           # HTTP client examples
├── requirements.txt            # Production dependencies
└── requirements-test.txt       # Test dependencies
```

## Use Cases

1. **Pre-deployment Validation**: Validate content before deploying to specific regions
2. **Content Localization**: Ensure proper subtitles and audio tracks for target markets
3. **Regulatory Compliance**: Automatically check against local content regulations
4. **Ad Compliance**: Verify advertising breaks meet regional restrictions
5. **Cultural Sensitivity**: Detect potentially sensitive content requiring manual review

## Supported Countries

Currently supported:
- 🇰🇷 **South Korea** - KMRB ratings, Korean broadcast standards
- 🇸🇦 **Saudi Arabia** - GCAM ratings, Islamic cultural guidelines

More countries can be easily added by creating new policy YAML files.

## Contributing

To add support for a new country:

1. Create a new YAML policy file in `policies/`
2. Define country-specific rules
3. Add tests in `tests/`
4. Update documentation

## License

See LICENSE file for details.

## Support

For issues, questions, or contributions, please open an issue on GitHub.
