# Contributing

## Development Setup

See the [README.md](README.md#installation) for installation instructions.

### Additional setup for development

```bash
# Install pre-commit hooks
pre-commit install
```

## Tools

We use the following tools:

- **uv**: Package management
- **ruff**: Fast Python linter and formatter
- **pyright**: Static type checker with strict mode enabled
- **pre-commit**: Git hooks for code quality checks
- **pytest**: Testing framework

### Running Quality Checks

```bash
# Run all pre-commit checks
pre-commit run --all-files

# Run individual tools
ruff check .
ruff format .
pyright
pytest
```

### Code Style

- All code should be type-annotated (enforced by pyright strict mode)
- Follow ruff's formatting rules (automatically applied)
- Use meaningful variable names
- Add docstrings to all public functions and classes

### Project Structure

```
awair-exporter/
├── scripts/
│   └── awair-export.py     # CLI entry point
├── src/
│   └── awair_exporter/
│       ├── __init__.py
│       ├── client.py       # Awair API client
│       ├── config.py       # Configuration handling
│       ├── models.py       # Pydantic models for API responses
│       └── exporter.py     # CSV export logic
├── tests/
│   └── ...
├── .env.example            # Example environment variables
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
├── README.md
└── CONTRIBUTING.md
```

### Adding Dependencies

```bash
# Add a runtime dependency
uv add requests

# Add a development dependency
uv add --group dev pytest-cov
```

### Making Changes

1. Create a new branch for your feature/fix
2. Make your changes
3. Ensure all checks pass (`pre-commit run --all-files`)
4. Add tests for new functionality
5. Update documentation if needed
6. Submit a pull request

### Environment Variables

For development, copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
# Edit .env with your credentials
```

Never commit the `.env` file or any credentials to the repository.
