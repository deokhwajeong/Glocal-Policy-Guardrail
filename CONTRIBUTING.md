# Contributing to Glocal Policy Guardrail

Thank you for your interest in contributing to the Glocal Policy Guardrail project! This guide will help you add new country policies and contribute to the framework.

## Table of Contents

- [Adding a New Country Policy](#adding-a-new-country-policy)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Submitting Changes](#submitting-changes)

## Adding a New Country Policy

Follow these steps to add a new country to the framework:

### 1. Create the Policy YAML File

Create a new YAML file in the `policies/` directory (e.g., `policies/france.yaml`):

```yaml
# France Policy Configuration
country_code: FR
country_name: France

# Forbidden keywords that cannot appear in content metadata
forbidden_keywords:
  - example_forbidden_term

# Content rating restrictions
content_rating:
  minimum_age: 0
  prohibited_ratings: []
  allowed_ratings:
    - ALL
    - 10
    - 12
    - 16
    - 18

# Ad time-window restrictions (24-hour format)
advertising:
  forbidden_time_windows: []
  max_duration_minutes: 12

# Mandatory features
mandatory_features:
  - gdpr_compliance

# Regional compliance
compliance:
  requires_gdpr_compliance: true
```

### 2. Update PolicyLoader

Edit `glocal_guardrail/policy_loader.py` to include your new country:

```python
# In the load_policy method, add to country_file_map:
country_file_map = {
    "SA": "saudi_arabia.yaml",
    "KR": "south_korea.yaml",
    "DE": "germany.yaml",
    "FR": "france.yaml",  # Add your new country
}
```

Note: The `list_available_policies()` method will automatically include the new country.

### 3. Add Tests

Create tests for your new policy in `tests/test_rule_engine.py`:

```python
@pytest.fixture
def france_policy():
    """Fixture for France policy"""
    loader = PolicyLoader()
    return loader.load_policy("FR")


def test_load_france_policy():
    """Test loading France policy"""
    loader = PolicyLoader()
    policy = loader.load_policy("FR")
    
    assert policy.country_code == "FR"
    assert policy.country_name == "France"
    assert "gdpr_compliance" in policy.mandatory_features


def test_france_gdpr_compliance(france_policy):
    """Test GDPR compliance for France"""
    engine = RuleEngine(france_policy)
    
    metadata = {
        "title": "App",
        "features": ["gdpr_compliance"],
        "gdpr_compliant": True
    }
    
    result = engine.validate(metadata)
    assert result.status == "PASS"
```

### 4. Update Documentation

Add your country to the README.md supported countries section:

```markdown
### 🌍 Supported Countries

- **Saudi Arabia (SA)**: ...
- **South Korea (KR)**: ...
- **Germany (DE)**: ...
- **France (FR)**: GDPR compliance, content rating requirements
```

### 5. Run Tests

Verify all tests pass:

```bash
pytest -v
```

### 6. Test Manually

Test your new policy with the example scripts:

```python
from glocal_guardrail.governance import GovernanceEngine

governance = GovernanceEngine()
metadata = {
    "title": "Test App",
    "features": ["gdpr_compliance"],
    "gdpr_compliant": True
}

result = governance.check_single_country(metadata, "FR")
print(f"Status: {result.status}")
```

## Code Standards

### Python Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Add docstrings to all public functions and classes
- Keep functions focused and single-purpose

### YAML Policy Files

- Use consistent indentation (2 spaces)
- Include comments explaining complex rules
- Organize sections consistently across all policies
- Use lowercase with underscores for field names

### Testing

- Write tests for all new functionality
- Aim for high test coverage (>80%)
- Use descriptive test names that explain what is being tested
- Include both positive and negative test cases

## Testing Guidelines

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_rule_engine.py

# Run with coverage
pytest --cov=glocal_guardrail

# Run with verbose output
pytest -v
```

### Test Structure

Each test should:
1. Set up test data (arrange)
2. Execute the code being tested (act)
3. Verify the results (assert)

Example:

```python
def test_forbidden_keywords():
    # Arrange
    loader = PolicyLoader()
    policy = loader.load_policy("SA")
    engine = RuleEngine(policy)
    metadata = {"title": "Casino Night"}
    
    # Act
    result = engine.validate(metadata)
    
    # Assert
    assert result.status == "REJECT"
    assert any("forbidden_keywords" in v["rule"] for v in result.violations)
```

## Submitting Changes

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/add-france-policy`)
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass
6. Update documentation
7. Commit your changes with clear messages
8. Push to your fork
9. Create a Pull Request

### Commit Message Guidelines

Use clear, descriptive commit messages:

- Start with a verb in imperative mood (Add, Fix, Update, Remove)
- Keep the first line under 72 characters
- Add detailed description if needed

Examples:
```
Add France policy configuration

- Create france.yaml with GDPR compliance rules
- Update policy loader to support FR country code
- Add comprehensive tests for France policy
```

### Pull Request Checklist

Before submitting your PR, ensure:

- [ ] All tests pass
- [ ] New tests are added for new functionality
- [ ] Documentation is updated
- [ ] Code follows project style guidelines
- [ ] Commit messages are clear and descriptive
- [ ] No sensitive data is included in commits

## Policy Configuration Fields

### Required Fields

All policy files must include:
- `country_code`: ISO 3166-1 alpha-2 code
- `country_name`: Full country name

### Optional Sections

- `forbidden_keywords`: List of prohibited terms
- `content_rating`: Rating system restrictions
- `advertising`: Ad timing and duration rules
- `mandatory_features`: Required app features
- `youth_protection`: Age-based restrictions
- `compliance`: Regional legal requirements

## Getting Help

If you need help or have questions:

1. Check existing issues and discussions
2. Read the documentation in README.md
3. Look at existing policy files for examples
4. Open an issue for discussion

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the project
- Show empathy towards other contributors

Thank you for contributing to Glocal Policy Guardrail!
