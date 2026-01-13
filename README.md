# Glocal Policy Guardrail

An automated Policy-as-Code (PaC) framework for Smart TV/OTT platforms to manage global legal and cultural compliance risks.

## 🚀 Features

- **Rule Engine**: Python-based validator for country-specific content rules (Korea, Saudi Arabia)
- **Policy Config**: YAML files for localized rules (forbidden content, ad windows, ratings)
- **Pre-deployment Check**: Returns PASS/REJECT status based on regional triggers
- **FastAPI**: RESTful API for seamless CI/CD integration

## 📦 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Using the Python API

```python
from src.guardrail.rule_engine import RuleEngine

engine = RuleEngine()
content = {
    "title": "Family Movie",
    "categories": ["family"],
    "rating": "ALL",
    "subtitle_languages": ["ko"],
    "ad_breaks": []
}

result = engine.validate_content(content, "korea")
print(f"Status: {result.status.value}")  # PASS or REJECT
```

### Using the FastAPI Server

```bash
# Start the server
python src/api.py

# Validate content
curl -X POST "http://localhost:8000/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "title": "Test Movie",
      "categories": ["action"],
      "rating": "15",
      "subtitle_languages": ["ko"]
    },
    "country": "korea"
  }'
```

Access the interactive API docs at: `http://localhost:8000/docs`

## 🌍 Supported Countries

- 🇰🇷 **South Korea** - KMRB ratings, Korean broadcast standards
- 🇸🇦 **Saudi Arabia** - GCAM ratings, Islamic cultural guidelines

## 📚 Documentation

See [docs/README.md](docs/README.md) for comprehensive documentation including:
- Detailed API reference
- Policy configuration guide
- CI/CD integration examples
- Testing instructions

## 🧪 Testing

```bash
pip install -r requirements-test.txt
pytest tests/
```

## 📁 Project Structure

```
Glocal-Policy-Guardrail/
├── src/
│   ├── guardrail/
│   │   └── rule_engine.py      # Core validation logic
│   └── api.py                   # FastAPI server
├── policies/
│   ├── korea.yaml              # Korea policy config
│   └── saudi_arabia.yaml       # Saudi Arabia policy config
├── tests/                       # Unit and integration tests
└── examples/                    # Usage examples
```

## 🔧 Example Usage

Run the included examples:

```bash
# Python API examples
python examples/usage_examples.py

# API client examples (requires server running)
python examples/api_client.py
```

## 📄 License

See LICENSE file for details.
