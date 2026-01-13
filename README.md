# Glocal Policy Guardrail

An automated **Policy-as-Code (PaC)** framework designed for Smart TV/OTT platforms to manage global legal and cultural compliance risks.

## Overview

The Glocal Policy Guardrail is a comprehensive compliance validation engine that helps media companies ensure their content and applications meet regional regulatory requirements across different countries. It provides automated pre-deployment checks to prevent regulatory violations in the global media ecosystem.

## Features

### 🎯 Core Components

1. **Rule Engine**: Python-based validator that checks content/app metadata against country-specific rules
2. **Policy Configuration**: YAML-based policy definitions for localized rules and compliance requirements
3. **Governance Logic**: Pre-deployment check system returning 'PASS' or 'REJECT' status
4. **API Layer**: Lightweight FastAPI interface for CI/CD pipeline integration

### 🌍 Supported Countries

- **Saudi Arabia (SA)**: Forbidden keywords, prayer time ad restrictions, local content quotas
- **South Korea (KR)**: Real-name verification, youth protection (Cinderella law), data localization
- **Germany (DE)**: GDPR compliance, FSK ratings, youth protection (JMStV)

### ✅ Validation Capabilities

- Forbidden keyword detection
- Content rating compliance
- Mandatory feature verification
- Advertising time-window restrictions
- Youth protection requirements
- Regional compliance checks (GDPR, data localization, real-name verification)
- Local content quota validation

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install the package in development mode:

```bash
pip install -e .
```

### Quick Server Start

For the fastest way to start the API server:

```bash
python run_server.py
```

This will start the server with sensible defaults on `http://127.0.0.1:8000`

## Quick Start

### 1. Python API Usage

```python
from glocal_guardrail.governance import GovernanceEngine

# Initialize the governance engine
governance = GovernanceEngine()

# Define your content/app metadata
metadata = {
    "title": "Family Entertainment Hub",
    "description": "Wholesome content for all ages",
    "features": [
        "parental_controls",
        "content_filtering",
        "gdpr_compliance"
    ],
    "gdpr_compliant": True,
    "local_content_percentage": 35
}

# Check compliance for a single country
result = governance.check_single_country(metadata, "SA")
print(f"Status: {result.status}")  # PASS or REJECT
print(f"Violations: {result.violations}")

# Check multiple countries for deployment readiness
report = governance.get_deployment_readiness(
    metadata,
    ["SA", "KR", "DE"]
)
print(f"Deployment Ready: {report['deployment_ready']}")
```

### 2. REST API Usage

Start the API server:

```bash
# Option 1: Using Python module (default: localhost:8000)
python -m glocal_guardrail.api

# Option 2: Using uvicorn directly
uvicorn glocal_guardrail.api:app --reload --host 127.0.0.1 --port 8000

# Option 3: Configure via environment variables
export GUARDRAIL_HOST=0.0.0.0
export GUARDRAIL_PORT=8080
python -m glocal_guardrail.api
```

API will be available at `http://localhost:8000` (or your configured host/port)

#### API Endpoints

- `GET /` - Service information
- `GET /health` - Health check
- `GET /policies` - List available country policies
- `POST /validate` - Validate against multiple countries
- `POST /validate/{country_code}` - Validate against single country
- `POST /deployment-check` - Comprehensive deployment readiness check

#### Example API Request

```bash
curl -X POST "http://localhost:8000/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {
      "title": "My Streaming App",
      "description": "Entertainment platform",
      "features": ["parental_controls", "gdpr_compliance"],
      "gdpr_compliant": true
    },
    "target_countries": ["DE", "KR"]
  }'
```

#### Example Response

```json
{
  "results": {
    "DE": {
      "status": "PASS",
      "country_code": "DE",
      "is_compliant": true,
      "violations": [],
      "warnings": [],
      "violation_count": 0,
      "warning_count": 0
    },
    "KR": {
      "status": "REJECT",
      "country_code": "KR",
      "is_compliant": false,
      "violations": [
        {
          "rule": "mandatory_features",
          "message": "Missing mandatory feature: 'real_name_verification'",
          "severity": "high"
        }
      ],
      "violation_count": 1,
      "warning_count": 0
    }
  }
}
```

## Policy Configuration

Policies are defined in YAML files located in the `policies/` directory:

- `policies/saudi_arabia.yaml` - Saudi Arabia compliance rules
- `policies/south_korea.yaml` - South Korea compliance rules
- `policies/germany.yaml` - Germany compliance rules

### Policy Structure

Each policy file contains:

```yaml
country_code: XX
country_name: Country Name

forbidden_keywords:
  - keyword1
  - keyword2

content_rating:
  minimum_age: 0
  prohibited_ratings: []
  allowed_ratings: []

advertising:
  forbidden_time_windows: []
  max_duration_minutes: 5

mandatory_features:
  - feature1
  - feature2

compliance:
  requires_gdpr_compliance: true
  # ... other compliance requirements
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=glocal_guardrail

# Run specific test file
pytest tests/test_rule_engine.py

# Run with verbose output
pytest -v
```

## Examples

See the `examples/` directory for complete usage examples:

- `examples/usage_example.py` - Python API usage examples
- `examples/api_client_example.py` - REST API client examples
- `examples/sample_metadata.json` - Template metadata file for validation

Run examples:

```bash
# Python API examples
python examples/usage_example.py

# API client examples (requires API server running)
python examples/api_client_example.py
```

## CI/CD Integration

The Glocal Policy Guardrail is designed to integrate seamlessly into CI/CD pipelines:

### GitHub Actions Example

```yaml
name: Content Compliance Check

on: [push, pull_request]

jobs:
  compliance:
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
      
      - name: Run compliance check
        run: |
          python -c "
          from glocal_guardrail.governance import GovernanceEngine
          import json
          
          governance = GovernanceEngine()
          metadata = json.load(open('metadata.json'))
          
          report = governance.get_deployment_readiness(
              metadata,
              ['SA', 'KR', 'DE']
          )
          
          if not report['deployment_ready']:
              print('Compliance check FAILED')
              exit(1)
          print('Compliance check PASSED')
          "
```

### Jenkins Pipeline Example

```groovy
pipeline {
    agent any
    
    stages {
        stage('Compliance Check') {
            steps {
                sh '''
                    pip install -r requirements.txt
                    python examples/usage_example.py
                '''
            }
        }
    }
}
```

## Architecture

```
glocal_guardrail/
├── __init__.py           # Package initialization
├── policy_loader.py      # YAML policy configuration loader
├── rule_engine.py        # Core validation engine
├── governance.py         # Pre-deployment check orchestration
└── api.py               # FastAPI REST interface

policies/
├── saudi_arabia.yaml    # Saudi Arabia policy rules
├── south_korea.yaml     # South Korea policy rules
└── germany.yaml         # Germany policy rules

tests/
├── test_policy_loader.py
├── test_rule_engine.py
├── test_governance.py
└── test_api.py

examples/
├── usage_example.py      # Python API examples
└── api_client_example.py # REST API examples
```

## Contributing

Contributions are welcome! To add a new country policy:

1. Create a new YAML file in `policies/` directory
2. Define country-specific rules following the existing structure
3. Update `policy_loader.py` to include the new country code mapping
4. Add tests for the new policy
5. Update documentation

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on adding new countries and contributing to the project.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Use Cases

- **Content Distribution**: Validate streaming content before regional deployment
- **App Store Submission**: Ensure OTT apps meet local requirements
- **Advertising Compliance**: Verify ad schedules comply with cultural restrictions
- **Regulatory Auditing**: Generate compliance reports for regulators
- **Multi-Region Deployment**: Check readiness across multiple markets simultaneously

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.
