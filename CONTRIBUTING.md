# Developer Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Project Setup](#project-setup)
4. [Coding Standards](#coding-standards)
5. [Running the Application](#running-the-application)
6. [Testing](#testing)
7. [Security Considerations](#security-considerations)
8. [Deployment](#deployment)
9. [Contribution Guidelines](#contribution-guidelines)
10. [License](#license)

---

## Introduction

This document provides a comprehensive guide for developers contributing to the **Python Fail2Ban API** project. It
outlines the necessary steps for setting up the development environment, coding standards, security practices, testing,
and deployment procedures.

---

## Prerequisites

Before starting development, ensure that your environment meets the following requirements:

- **Python 3.12** or higher
- **Poetry** for dependency management
- **FastAPI** as the web framework
- **Pydantic** for data validation
- **Git** for version control

### Install Required Tools

1. **Python 3.12**: Download and install from [python.org](https://www.python.org/downloads/).
2. **Poetry**: Install Poetry by following the [official guide](https://python-poetry.org/docs/).
3. **Git**: Install Git from [git-scm.com](https://git-scm.com/).

---

## Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/orenlab/pyfail2banapi.git
cd pyfail2banapi
```

### 2. Set Up Virtual Environment

We recommend using `Poetry` to manage dependencies:

```bash
poetry install
```

This will create a virtual environment and install all necessary dependencies.

---

## Coding Standards

### Code Formatting

We adhere to **PEP 8** guidelines for Python code. Please ensure your code is formatted using `black`:

```bash
black .
```

### Type Hinting

Use **type hints** throughout the code for better readability and maintainability. Follow **PEP 484** for type
annotations.

```python
def get_jail_status(jail_name: str) -> JailStatus:
# Function implementation
```

### Linting

Run `flake8` to check for any linting issues:

```bash
flake8 .
```

### Docstrings

Follow **PEP 257** for docstrings. Every module, class, and function should have a clear, concise docstring.

---

## Running the Application

### 1. Local Development

Start the FastAPI development server:

```bash
poetry run uvicorn pyfail2banapi.app:app --reload
```

Visit `http://127.0.0.1:8000/docs` to see the automatically generated API documentation.

---

## Testing

### 1. Run Unit Tests

We use `pytest` for unit testing. Ensure that all tests pass before committing your code:

```bash
pytest
```

### 2. Coverage Report

Check the test coverage using `pytest-cov`:

```bash
pytest --cov=pyfail2banapi tests/
```

Ensure that test coverage is at least **90%** for all modules.

---

## Security Considerations

Security is a top priority for this project, especially since we interact with system-level services like `Fail2Ban` via
subprocesses.

### Best Practices

1. **Subprocess Execution**:
    - Always sanitize input before passing it to a subprocess.
    - Use `shlex` to safely handle shell commands.
    - Avoid direct shell execution where possible.

2. **Environment Variables**:
    - Never hardcode sensitive information like API keys or passwords.
    - Use environment variables and `.env` files to manage sensitive data.

3. **Input Validation**:
    - Use Pydantic models to validate all input data.

4. **Logging**:
    - Avoid logging sensitive information (e.g., passwords, API keys).
    - Use JSON format for logs to improve traceability.

### Security Audits

Ensure all dependencies are regularly updated and free of vulnerabilities. Use tools like `safety` or `bandit`:

```bash
poetry run safety check
```

```bash
poetry run bandit -r .
```

---

## Contribution Guidelines

We welcome contributions from the community! To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`.
3. Make your changes and add tests if needed.
4. Commit your changes: `git commit -m 'Add some feature'`.
5. Push to the branch: `git push origin feature/your-feature`.
6. Create a Pull Request.

Please ensure all code is properly documented, tested, and adheres to the coding standards before submitting a PR.

- **Commit Messages**: Write clear and descriptive commit messages. Use the following format:
  ```
  [type]: [short summary]

  [longer description, if necessary]
  ```

  Types of commits might include:
    - `feat`: A new feature
    - `fix`: A bug fix
    - `docs`: Documentation changes
    - `style`: Code style improvements (non-functional changes)
    - `refactor`: Code refactoring (no functional changes)
    - `test`: Adding or updating tests
    - `chore`: Other changes (e.g., build process, CI configuration)

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for more details.

---

This developer guide provides the essential steps and practices to maintain consistency and high-quality code in the *
*Python Fail2Ban API** project. For more information, feel free to contact the maintainers or open an issue on GitHub.
