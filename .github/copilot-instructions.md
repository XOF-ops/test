# Copilot Instructions

## Project Overview

This repository contains the Master Brain system, an autonomous research and development protocol infrastructure with Agent API integration.

## Code Style Guidelines

- Use Python 3.12+ syntax and features
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write descriptive docstrings for all public functions and classes

## Commit Message Format

Use descriptive commit messages following this format:
```
Tier 2: [Component] - [Action]
Coherence: [Impact on System]
Change: [Technical Detail]
```

**Note on Tier System:**
- **Tier 1**: Perfect coherence (5/5) - major architectural changes
- **Tier 2**: Standard changes with documented impact and rationale

Example: `Tier 2: Postgres - Fix Connection Loop. Coherence: Restored Memory Access. Change: Updated docker-compose.yml ports.`

## Testing

- Write pytest tests for all new functionality
- Place tests in the `tests/` directory
- Use pytest fixtures for common test setup
- Run tests with: `pytest tests/ -v`

## Security Guidelines

- Never commit secrets or API keys
- Use `.env` files for local development (these are gitignored)
- Use `.env.example` as a template for required environment variables
- Review all changes for potential security vulnerabilities

## Architecture Notes

The system follows a multi-layer axiom-based architecture:
- **Layer 4 (Immutable)**: Core axioms A1, A2, A4, A7, A9
- **Layer 3 (Revisable)**: Ethics axioms A3, A5, A6, A8
- **Patterns**: Various patterns for detecting structural tensions

## API Endpoints

When creating new API endpoints:
- Follow RESTful conventions
- Include proper error handling
- Return JSON responses with appropriate status codes
- Document new endpoints in the README
