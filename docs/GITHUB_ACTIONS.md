# GitHub Actions and CI/CD - Complete Guide

*Comprehensive guide to continuous integration and continuous deployment automation for Dietaneo*

---

## Table of Contents
1. [What is CI/CD?](#what-is-cicd)
2. [GitHub Actions Workflow](#github-actions-workflow)
3. [Workflow File Structure](#workflow-file-structure)
4. [How to View Results](#how-to-view-results)
5. [Practical Example](#practical-example)
6. [Common Errors](#common-errors)
7. [Future Optimizations](#future-optimizations)

---

## What is CI/CD?

### CI = Continuous Integration

**Definition**: Every time you push code to GitHub, GitHub machines automatically:
1. 📥 Download your code
2. 🔧 Install dependencies
3. ✅ Run tests
4. 📊 Generate reports

**Benefit**: Errors are detected **immediately** without waiting for code to reach production.

### CD = Continuous Deployment

**Definition**: If tests pass, code automatically deploys to production servers.

> **Note**: Our project currently has **only CI** (GitHub Actions runs tests). CD (automatic deployment) can be added later.

---

## GitHub Actions Workflow

### What is a Workflow?

A workflow is an automated process that runs when certain events occur in your repository. It's defined in a YAML file that tells GitHub what to do and when.

### File Location
```
.github/
└── workflows/
    └── tests.yml          ← Our workflow file
```

---

## Workflow File Structure

### Complete Breakdown: `.github/workflows/tests.yml`

```yaml
name: Tests
```

**What it is?** The name shown in GitHub when the workflow executes.
**Result**: You'll see ✅ **Tests** in GitHub Actions.

---

### Triggers: When Does It Run?

```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
```

**What does it mean?**
- **`push`**: Runs when you `git push` to `main` or `develop` branches
- **`pull_request`**: Runs when someone opens a Pull Request to `main` or `develop`

**Practical example**:
```bash
# This triggers the workflow (because push to develop)
git push origin develop

# This also triggers (because opening PR to main or develop)
# Go to GitHub → Open Pull Request
```

---

### The Job Definition

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
```

**What is it?**
- `test`: Job name
- `runs-on: ubuntu-latest`: The machine that will run the code (Ubuntu Linux, latest version)

**Analogy**: Like borrowing a computer in the cloud to run your tests.

---

### Steps: Sequential Actions

Steps are **sequential actions** that execute in order:

#### Step 1: Download the Code
```yaml
- uses: actions/checkout@v5
```

**What it does**: GitHub downloads your repository to the Ubuntu machine.

---

#### Step 2: Install Python 3.13
```yaml
- name: Set up Python 3.13
  uses: actions/setup-python@v5
  with:
    python-version: '3.13'
```

**What it does?**
- `name`: Step description (shown in logs)
- `uses`: Use a predefined GitHub action to install Python
- `python-version`: Specifies version (3.13, same as our `Dockerfile`)

**Result**: The Ubuntu machine now has Python 3.13 ready.

---

#### Step 3: Install Dependencies
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
```

**What it does?**
- `run: |`: Execute shell commands (the `|` means "multiple lines")
- `python -m pip install --upgrade pip`: Upgrade pip (the package manager)
- `pip install -r requirements.txt`: Install all packages listed in `requirements.txt`

**Analogy**: Like creating a virtual environment and saying "install everything we need".

---

#### Step 4: Run Tests with Coverage
```yaml
- name: Run tests with coverage
  run: |
    pytest --cov=app --cov-report=term-missing --cov-report=xml
```

**What it does?**
- `pytest`: Run all tests in the `test/` directory
- `--cov=app`: Calculate **code coverage** (what percentage of code is tested)
- `--cov-report=term-missing`: Show in terminal which lines are NOT tested
- `--cov-report=xml`: Generate `coverage.xml` file with detailed data

**Result**:
```
test/test_api.py .................. [100%]
8 passed in 0.45s

Name                Stmts   Miss  Cover   Missing
---------------------------------------------------
app/api.py             95      0   100%
app/calculations.py    50      0   100%
---------------------------------------------------
TOTAL                 145      0   100%
```

---

#### Step 5: Upload Coverage to Codecov
```yaml
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    files: ./coverage.xml
    fail_ci_if_error: false
```

**What it does?**
- Uploads the coverage report to [Codecov.io](https://codecov.io) (external service)
- Codecov shows beautiful graphs and alerts if coverage decreases
- `fail_ci_if_error: false`: Don't stop workflow if Codecov fails (optional)

---

## How to View Results

### In GitHub (Web Interface)

1. Go to your repository: https://github.com/your_username/nutrition_calculator
2. Click the **"Actions"** tab
3. You'll see a list of executions:
   ```
   ✅ Commit message        main    2 min ago
   ❌ Commit message        develop 5 min ago
   ⏳ Commit message        main    in progress...
   ```

4. Click an execution to see details:
   ```
   Tests
   ├── test (ubuntu-latest)
   │   ├── ✅ Checkout code
   │   ├── ✅ Set up Python 3.13
   │   ├── ✅ Install dependencies
   │   ├── ✅ Run tests with coverage
   │   └── ✅ Upload coverage to Codecov
   ```

### In Pull Requests

When you open a PR, GitHub automatically:
1. Runs the workflow
2. Shows a status badge at the bottom of the PR:
   ```
   ✅ Tests - All checks passed
   ```

**Benefit**: Before merging, you know the code is working.

---

## Practical Example

### Scenario: You Change `app/calculations.py`

```bash
# 1. Make changes and commit
git add app/calculations.py
git commit -m "refactor: simplify get_age_reduction function"

# 2. Push to develop
git push origin develop
```

### What Happens Automatically?

```
┌─────────────────────────────────────┐
│ GitHub receives your push           │
│ → Triggers "Tests" workflow         │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ Ubuntu machine in GitHub Cloud:     │
│ 1. Downloads your code              │
│ 2. Installs Python 3.13             │
│ 3. Installs dependencies            │
│ 4. Runs: pytest --cov               │
│ 5. Uploads results to Codecov       │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ Results in GitHub                   │
│ ✅ All tests passed                 │
│ 📊 100% coverage                    │
│ 📈 Graphs in Codecov.io             │
└─────────────────────────────────────┘
```

---

## Common Errors

### ❌ Error: "ModuleNotFoundError: No module named 'app'"

**Cause**: Dependencies didn't install correctly.

**Solution**:
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt  # Verify this file exists
```

---

### ❌ Error: "pytest: command not found"

**Cause**: `pytest` is not in `requirements.txt`.

**Solution**: Verify that `requirements.txt` contains:
```
pytest
pytest-cov
httpx
```

---

### ❌ Error: "Tests failed: 2 passed, 1 failed"

**Cause**: A test is not passing.

**Solution**:
1. Look at the complete log in GitHub Actions
2. Run locally: `pytest -v` to see what fails
3. Fix the code
4. Push again

---

## Future Optimizations

### ✅ Things We Can Add:

#### 1. **Automatic Linting** (Code style check)
```yaml
- name: Lint with Ruff
  run: python -m ruff check .
```

#### 2. **Docker Build Check**
```yaml
- name: Build Docker image
  run: docker build -t nutrition-calculator .
```

#### 3. **Tests on Multiple Python Versions**
```yaml
strategy:
  matrix:
    python-version: ['3.11', '3.12', '3.13']
```

#### 4. **Automatic Deployment** (CD)
```yaml
- name: Deploy to Production
  if: github.ref == 'refs/heads/main'
  run: ./deploy.sh
```

---

## Key Concepts Summary

| Concept | Explanation |
|---------|-------------|
| **CI/CD** | Continuous Integration (automatic tests) + Continuous Deployment (push to production) |
| **Workflow** | YAML file that defines what to do and when |
| **Trigger** | Event that starts the workflow (push, pull_request) |
| **Job** | Set of steps that run on a machine |
| **Step** | Individual action (install Python, run tests, etc.) |
| **Coverage** | Percentage of code being tested |
| **Codecov** | Service that stores and displays coverage graphs |

---

## FAQ

### Q: Why is it in `.github/workflows/`?
**A**: GitHub automatically looks for workflows in that folder. It's a convention.

### Q: Does it run on my computer?
**A**: No, it runs on GitHub's servers in the cloud (free Ubuntu machines).

### Q: How much does it cost?
**A**: For public repositories it's **completely free**. GitHub gives you free minutes per month.

### Q: Can I see the logs?
**A**: Yes, in GitHub → Actions → Your workflow → View detailed logs.

### Q: What happens if a test fails?
**A**: The workflow stops with ❌ red status. The PR can't be merged until you fix the test.

---

## Next Steps

1. **Watch it in action**: Push to `develop` and observe GitHub Actions
2. **Experiment**: Deliberately break a test to see what happens
3. **Learn**: Read detailed logs to understand what each step does
4. **Enhance**: Add more validations (linting, Docker checks, etc.)

---

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pytest with GitHub Actions](https://github.com/actions/setup-python)
- [Codecov Integration](https://about.codecov.io/)

---

**Automated testing is your 24/7 assistant, ensuring code quality even while you sleep. 🤖✨**
