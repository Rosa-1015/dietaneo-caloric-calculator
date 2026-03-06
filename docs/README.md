# 📚 Developer Documentation

This folder contains guides and documentation for developers working on the Dietaneo project.

## 📄 Available Guides

### [TESTING.md](TESTING.md)
**Complete Testing Guide** (Beginner-friendly, mentor-style)

Contents:
- Why testing matters
- Unit testing fundamentals
- Your first test (step-by-step)
- Testing calculations (pure functions)
- Testing API endpoints
- How to run tests
- Best practices & patterns
- Troubleshooting

**Read if**: You need to understand how to write tests or you're assigned testing tasks.

### [../CLAUDE.md](../CLAUDE.md)
**Architecture & Development Setup**

Contents:
- Project overview & structure
- Development commands (Docker, manual setup)
- Code quality (linting, testing)
- Calculation pipeline
- Important implementation details

## 📖 Quick Start

**New to the project?**
1. Read [../CLAUDE.md](../CLAUDE.md) - Understand the architecture
2. Read [TESTING.md](TESTING.md) - Learn how to write tests

**Ready to contribute?**
```bash
# Setup
docker compose up --build

# Run tests
pytest -v

# Lint code
python -m ruff check .
```

## 🤝 Contributing

Found issues or have improvements?
1. Open an issue
2. Create a PR with your changes

---

**Last updated**: March 2026
