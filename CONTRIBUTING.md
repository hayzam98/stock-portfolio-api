# Contributing to Stock Portfolio API

Thank you for considering contributing to Stock Portfolio API! This document outlines the process and guidelines for contributing.

## 🚀 How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/hayzam98/stock-portfolio-api/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Detailed description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)
   - Screenshots if applicable

### Suggesting Enhancements

1. Check if the enhancement has already been suggested
2. Create a new issue with:
   - Clear description of the enhancement
   - Why it would be useful
   - Possible implementation approach
   - Examples of usage

### Pull Requests

1. Fork the repository
2. Create a new branch from `develop`:
```powershell
   git checkout develop
   git checkout -b feature/your-feature-name
```
3. Make your changes
4. Write or update tests as needed
5. Ensure all tests pass:
```powershell
   pytest
```
6. Commit your changes with clear messages:
```powershell
   git commit -m "feat: Add amazing feature"
```
7. Push to your fork:
```powershell
   git push origin feature/your-feature-name
```
8. Open a Pull Request to the `develop` branch

## 📋 Development Setup

1. Clone your fork:
```powershell
   git clone https://github.com/hayzam98/stock-portfolio-api.git
   cd stock-portfolio-api
```

2. Create virtual environment:
```powershell
   python -m venv venv
   .\venv\Scripts\Activate
```

3. Install dependencies:
```powershell
   pip install -r requirements.txt
```

4. Set up environment variables (copy `.env.example` to `.env`)

5. Create and initialize database:
```powershell
   mysql -u root -p < scripts\create_database.sql
   python scripts\init_db.py
```

## 🎨 Code Style

- Follow [PEP 8](https://pep8.org/) guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes (Google style)
- Keep functions focused and small
- Use meaningful variable names

### Example:
```python
def calculate_total_value(quantity: float, price: float) -> float:
    """
    Calculate the total value of a stock position
    
    Args:
        quantity: Number of shares
        price: Price per share
        
    Returns:
        Total value of the position
    """
    return quantity * price
```

## 🧪 Testing

- Write tests for new features
- Ensure existing tests still pass
- Aim for good test coverage
- Use pytest fixtures for setup

### Running Tests:
```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests\

# Run specific test file
pytest tests\test_auth.py -v

# Run tests by marker
pytest -m auth
```

## 📝 Commit Messages

Follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding or updating tests
- `refactor:` Code refactoring
- `style:` Code style changes
- `chore:` Maintenance tasks

### Examples:
```
feat: Add pagination to transaction list endpoint
fix: Correct profit calculation for partial sells
docs: Update API documentation for portfolio endpoints
test: Add tests for sell transaction validation
refactor: Simplify portfolio calculation logic
```

## 🌿 Branching Strategy

- `main`: Production-ready code (protected)
- `develop`: Development branch (default)
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `hotfix/*`: Urgent fixes for production
- `release/*`: Release preparation

### Workflow:
```powershell
# Create feature branch
git checkout develop
git checkout -b feature/my-feature

# Work on feature
git add .
git commit -m "feat: Add my feature"

# Merge to develop
git checkout develop
git merge feature/my-feature --no-ff

# Delete feature branch
git branch -d feature/my-feature
```

## ✅ Pull Request Checklist

Before submitting your PR, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass (`pytest`)
- [ ] New tests added for new features
- [ ] Documentation updated if needed
- [ ] Commit messages are clear and follow conventions
- [ ] Branch is up to date with `develop`
- [ ] No merge conflicts
- [ ] Code is properly commented

## 🔍 Code Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged
4. Your contribution will be acknowledged

## 💬 Questions?

Feel free to open an issue for any questions or discussions!

## 📜 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help create a welcoming environment

## 🙏 Thank You!

Your contributions make this project better for everyone!
