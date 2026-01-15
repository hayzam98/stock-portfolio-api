# Useful Commands for Stock Portfolio API

## 🐍 Python & Virtual Environment
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate virtual environment (Windows CMD)
venv\Scripts\activate.bat

# Deactivate virtual environment
deactivate

# Install dependencies
pip install -r requirements.txt

# Update pip
python -m pip install --upgrade pip

# Freeze current dependencies
pip freeze > requirements.txt
```

## 🗄️ Database Commands
```powershell
# Create database (MySQL)
mysql -u root -p < scripts\create_database.sql

# Initialize database tables
python scripts\init_db.py

# Access MySQL CLI
mysql -u root -p

# Show databases
mysql -u root -p -e "SHOW DATABASES;"

# Drop database (CAUTION!)
mysql -u root -p -e "DROP DATABASE IF EXISTS stock_portfolio;"
```

## 🚀 Running the Application
```powershell
# Run with auto-reload (development)
uvicorn app.main:app --reload

# Run on specific port
uvicorn app.main:app --reload --port 8080

# Run with host binding
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run without reload (production-like)
uvicorn app.main:app
```

## 🧪 Testing Commands
```powershell
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests\test_auth.py

# Run specific test
pytest tests\test_auth.py::test_register_user

# Run with coverage
pytest --cov=app

# Run with coverage report
pytest --cov=app --cov-report=html

# Run with coverage and open HTML report
pytest --cov=app --cov-report=html
Start-Process htmlcov\index.html

# Run tests matching a keyword
pytest -k "auth"

# Run tests by marker
pytest -m auth
```

## 🌿 Git Commands
```powershell
# Check current branch
git branch

# Check status
git status

# View commit history
git log --oneline --graph --all --decorate

# Create new feature branch
git checkout develop
git checkout -b feature/new-feature

# Add all changes
git add .

# Commit with message
git commit -m "feat: Add new feature"

# Push to remote
git push origin feature/new-feature

# Merge feature to develop
git checkout develop
git merge feature/new-feature --no-ff

# Delete local branch
git branch -d feature/new-feature

# Delete remote branch
git push origin --delete feature/new-feature

# View all remote branches
git branch -r

# Pull latest changes
git pull origin develop

# Stash changes
git stash

# Apply stashed changes
git stash pop

# View tags
git tag

# Create annotated tag
git tag -a v1.0.1 -m "Version 1.0.1"

# Push tags
git push origin --tags
```

## 🔒 Security & Environment
```powershell
# Generate secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Copy environment template
Copy-Item .env.example .env

# Check environment variables (PowerShell)
Get-Content .env
```

## 📦 Package Management
```powershell
# List installed packages
pip list

# Show package info
pip show fastapi

# Uninstall package
pip uninstall package-name

# Install specific version
pip install fastapi==0.104.1

# Upgrade package
pip install --upgrade fastapi
```

## 🐛 Debugging
```powershell
# Run with Python debugger
python -m pdb app/main.py

# Check Python version
python --version

# Check pip version
pip --version

# Check installed packages versions
pip show fastapi sqlalchemy uvicorn
```

## 📊 Code Quality
```powershell
# Format code with black (if installed)
black app/

# Check code style with flake8 (if installed)
flake8 app/

# Type checking with mypy (if installed)
mypy app/

# Sort imports with isort (if installed)
isort app/
```

## 🔄 API Testing with curl
```powershell
# Health check
curl http://localhost:8000/health

# Register user
curl -X POST http://localhost:8000/auth/register `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test@example.com\",\"username\":\"testuser\",\"password\":\"test123\"}'

# Login
curl -X POST http://localhost:8000/auth/login `
  -H "Content-Type: application/x-www-form-urlencoded" `
  -d "username=testuser&password=test123"

# Get transactions (replace TOKEN)
curl -X GET http://localhost:8000/transactions/ `
  -H "Authorization: Bearer TOKEN"
```

## 🧹 Cleanup Commands
```powershell
# Remove Python cache
Get-ChildItem -Path . -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force

# Remove test database
Remove-Item -Path test.db -ErrorAction SilentlyContinue

# Remove coverage files
Remove-Item -Path .coverage -ErrorAction SilentlyContinue
Remove-Item -Path htmlcov -Recurse -Force -ErrorAction SilentlyContinue
```

## 📝 Documentation
```powershell
# View API docs (after running the app)
Start-Process http://localhost:8000/docs

# View alternative docs
Start-Process http://localhost:8000/redoc

# Download OpenAPI schema
curl http://localhost:8000/openapi.json -o openapi.json
```
