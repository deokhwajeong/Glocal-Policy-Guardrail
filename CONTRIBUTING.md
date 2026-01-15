# Contributing to Glocal Policy Guardrail

First off, thank you for considering contributing to Glocal Policy Guardrail! It's people like you that make this tool better for the global content compliance community.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)

---

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please be respectful, inclusive, and professional in all interactions.

**Our Pledge**: We are committed to providing a welcoming and inspiring community for all.

---

## How Can I Contribute?

### 🐛 Reporting Bugs
- Use the bug report template
- Include detailed steps to reproduce
- Provide system information
- Add relevant error messages/logs

### 💡 Suggesting Features
- Use the feature request template
- Explain the problem you're solving
- Describe your proposed solution
- Consider backward compatibility

### 🌍 Adding Country Support
- Use the country request template
- Research regulatory framework thoroughly
- Identify official monitoring sources
- Create comprehensive test cases

### 📝 Improving Documentation
- Fix typos, clarify instructions
- Add code examples
- Translate documentation
- Create video tutorials

### 🔧 Contributing Code
- Pick an issue labeled `good-first-issue` or `help-wanted`
- Comment on the issue to claim it
- Fork, develop, test, and submit a PR

---

## Development Setup

### Prerequisites
```bash
# Required
- Python 3.8 or higher
- Git
- pip

# Optional but recommended
- Docker & Docker Compose
- VS Code with Python extension
```

### Local Setup
```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/Glocal-Policy-Guardrail.git
cd Glocal-Policy-Guardrail

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# 4. Install pre-commit hooks
pre-commit install

# 5. Run tests to verify setup
pytest

# 6. Start development server
python web_dashboard.py
```

### Docker Setup
```bash
# Build and run with Docker Compose
docker-compose up --build

# Access dashboard at http://localhost:5000
```

---

## Pull Request Process

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-123
```

**Branch naming convention**:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `test/` - Test additions/improvements
- `refactor/` - Code refactoring
- `perf/` - Performance improvements

### 2. Make Your Changes
- Write clear, concise commit messages
- Follow coding standards (see below)
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_compliance.py

# Run linting
black .
flake8 .
mypy src/
```

### 4. Commit Your Changes
```bash
git add .
git commit -m "feat: add support for Brazil regulatory policies"
```

**Commit message format**:
```
<type>: <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (no code change)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Example**:
```
feat: add AI-powered policy suggestion engine

- Integrate OpenAI GPT-4 for legal text analysis
- Add confidence scoring for suggestions
- Implement legal review workflow UI

Closes #42
```

### 5. Push and Create PR
```bash
git push origin feature/your-feature-name
```

Then:
1. Go to GitHub and create a Pull Request
2. Fill out the PR template completely
3. Link related issues
4. Request review from maintainers

### 6. Code Review Process
- Maintainers will review within 2-3 business days
- Address feedback promptly
- Update your PR based on comments
- Once approved, maintainers will merge

---

## Coding Standards

### Python Style Guide
We follow [PEP 8](https://pep8.org/) with some modifications:

```python
# ✅ Good
def check_compliance(country: str, content: Dict[str, Any]) -> ComplianceResult:
    """
    Check content compliance against country policies.
    
    Args:
        country: ISO country code (e.g., 'US', 'KR')
        content: Content metadata dictionary
        
    Returns:
        ComplianceResult with violations and severity
        
    Raises:
        ValueError: If country is not supported
    """
    if country not in SUPPORTED_COUNTRIES:
        raise ValueError(f"Country {country} not supported")
    
    violations = []
    # ... implementation
    return ComplianceResult(violations=violations)

# ❌ Bad
def check(c, d):
    """Check compliance."""
    # No type hints, unclear names, minimal docstring
    v = []
    # ... implementation
    return v
```

### Code Quality Tools
```bash
# Auto-formatting
black src/ tests/
isort src/ tests/

# Linting
flake8 src/ tests/
pylint src/

# Type checking
mypy src/
```

### Best Practices
1. **Type Hints**: Always use type hints for function parameters and return values
2. **Docstrings**: Google-style docstrings for all public functions
3. **Error Handling**: Explicit exception handling, avoid bare `except:`
4. **Constants**: Use UPPER_CASE for module-level constants
5. **Naming**: 
   - Classes: `PascalCase`
   - Functions/Variables: `snake_case`
   - Private: `_leading_underscore`
6. **Line Length**: Maximum 100 characters (not strict 79)
7. **Imports**: 
   - Standard library first
   - Third-party second
   - Local imports last
   - Alphabetically sorted within groups

---

## Testing Guidelines

### Test Structure
```
tests/
├── test_compliance.py      # Unit tests for compliance scanner
├── test_api.py            # API endpoint tests
├── test_integration.py    # End-to-end integration tests
├── test_updater.py        # Policy updater tests
├── conftest.py            # Pytest fixtures
└── test_data/             # Test fixtures and data
```

### Writing Tests
```python
import pytest
from src.compliance_scanner import ComplianceGuardrail

class TestComplianceScanner:
    """Test suite for compliance scanning functionality."""
    
    @pytest.fixture
    def guardrail(self):
        """Create a ComplianceGuardrail instance for testing."""
        return ComplianceGuardrail()
    
    def test_forbidden_keyword_detection(self, guardrail):
        """Test that forbidden keywords are correctly detected."""
        content = {
            'title': 'Casino Night',
            'description': 'Gambling entertainment',
            'country': 'Saudi_Arabia'
        }
        
        result = guardrail.check_deployment('Saudi_Arabia', content)
        
        assert result.status == 'CRITICAL'
        assert len(result.violations) > 0
        assert any('gambling' in v.message.lower() for v in result.violations)
    
    @pytest.mark.parametrize("country,expected_status", [
        ("United_States", "PASS"),
        ("Saudi_Arabia", "CRITICAL"),
        ("South_Korea", "HIGH"),
    ])
    def test_country_specific_rules(self, guardrail, country, expected_status):
        """Test country-specific compliance rules."""
        content = {'title': 'Test Content', 'genre': 'Drama'}
        result = guardrail.check_deployment(country, content)
        assert result.status == expected_status
```

### Test Coverage Requirements
- **Minimum**: 85% overall coverage
- **Target**: 95% overall coverage
- **Critical paths**: 100% coverage
- **New features**: Must include tests

### Running Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=term --cov-report=html

# Specific test
pytest tests/test_compliance.py::TestComplianceScanner::test_forbidden_keyword_detection

# Watch mode (auto-run on changes)
pytest-watch

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

---

## Documentation

### Code Documentation
- **Modules**: Module-level docstring explaining purpose
- **Classes**: Class docstring with attributes and examples
- **Functions**: Google-style docstrings

**Example**:
```python
def scan_content(content: Dict[str, Any], countries: List[str]) -> Dict[str, ComplianceResult]:
    """
    Scan content against multiple country policies simultaneously.
    
    This function performs parallel compliance checks across all specified
    countries, returning a comprehensive report of violations and compliance
    status for each jurisdiction.
    
    Args:
        content: Content metadata dictionary containing:
            - title (str): Content title
            - description (str): Content description
            - genre (str): Content genre
            - tags (List[str]): Content tags
        countries: List of ISO country codes to check (e.g., ['US', 'KR', 'DE'])
        
    Returns:
        Dictionary mapping country codes to ComplianceResult objects:
        {
            'US': ComplianceResult(status='PASS', violations=[]),
            'SA': ComplianceResult(status='CRITICAL', violations=[...])
        }
        
    Raises:
        ValueError: If any country code is not supported
        KeyError: If required content fields are missing
        
    Example:
        >>> content = {
        ...     'title': 'Documentary Series',
        ...     'description': 'Educational content',
        ...     'genre': 'Documentary'
        ... }
        >>> results = scan_content(content, ['US', 'KR'])
        >>> results['US'].status
        'PASS'
    """
    # Implementation
```

### README Updates
When adding features, update:
- Feature list
- Usage examples
- Installation instructions (if needed)
- Supported countries table

### CHANGELOG
Add entry for your changes:
```markdown
## [Unreleased]

### Added
- AI-powered policy suggestion engine (#42)
- Support for Brazil regulatory framework (#51)

### Changed
- Improved scanning performance by 40% (#48)

### Fixed
- Fix timezone handling for ad restrictions (#49)
```

---

## Country Policy Contributions

### Research Checklist
When adding a new country:

1. **Regulatory Research**:
   - [ ] Identify primary regulatory bodies
   - [ ] Document key regulations and laws
   - [ ] List forbidden content categories
   - [ ] Define advertising restrictions
   - [ ] Identify age rating system
   - [ ] List mandatory platform features

2. **Source Identification**:
   - [ ] Official government websites
   - [ ] RSS feeds (if available)
   - [ ] Legal databases
   - [ ] Industry reports

3. **Policy File Creation**:
   - [ ] Create YAML policy file in `config/policy_rules.yaml`
   - [ ] Add monitoring sources to `config/regulatory_sources.yaml`
   - [ ] Follow existing structure and naming conventions

4. **Testing**:
   - [ ] Create test cases in `test_data/sample_deployments.yaml`
   - [ ] Test forbidden keywords
   - [ ] Test ad restrictions
   - [ ] Test feature requirements
   - [ ] Verify severity levels

5. **Documentation**:
   - [ ] Update README country list
   - [ ] Add country to OFFICIAL_REGULATORY_SOURCES.md
   - [ ] Include sources and references

### Example Policy Entry
```yaml
Brazil:
  forbidden_keywords:
    - "underage gambling"
    - "illegal substances"
  ad_restrictions:
    alcohol:
      restriction_type: "time_based"
      allowed_time_window: "21:00-06:00"
  age_rating_system: "DJCTQ"
  mandatory_features:
    - "Brazilian Portuguese subtitles"
    - "Accessibility features (closed captions)"
  violation_severity: "HIGH"
```

---

## Getting Help

- **Questions**: Open a [Discussion](https://github.com/deokhwajeong/Glocal-Policy-Guardrail/discussions)
- **Bugs**: Create an [Issue](https://github.com/deokhwajeong/Glocal-Policy-Guardrail/issues)
- **Chat**: Join our community chat (link TBD)
- **Email**: contact@glocalguardrail.io (for security issues)

---

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Featured on project website (coming soon)

Top contributors may receive:
- Swag (stickers, t-shirts)
- Conference sponsorship
- Co-authorship on research papers

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping make global content compliance easier for everyone!** 🌍
