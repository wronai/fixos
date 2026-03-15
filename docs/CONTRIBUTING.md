# Contributing to fixOS

## Development Setup

```bash
git clone https://github.com/wronai/fixfedora
cd fixOS
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

## Development Workflow

1. Create a feature branch from `main`
2. Make your changes
3. Add or update tests
4. Run the test suite
5. Submit a pull request

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov --cov-report=term-missing

# Run a specific test file
pytest tests/test_specific.py -v
```

## Code Style

Follow PEP 8 conventions.

## Pull Request Guidelines

- Keep PRs focused — one feature or fix per PR
- Include tests for new functionality
- Update documentation if needed
- Ensure all tests pass before submitting
- Use descriptive commit messages
