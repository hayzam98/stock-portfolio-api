# Stock Portfolio API 📈

![Tests](https://github.com/your-username/stock-portfolio-api/workflows/Tests/badge.svg)
![Code Quality](https://github.com/your-username/stock-portfolio-api/workflows/Code%20Quality/badge.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A professional RESTful API for tracking stock portfolio transactions with user authentication, built with FastAPI and MySQL.

A professional RESTful API for tracking stock portfolio transactions with user authentication, built with FastAPI and MySQL.

## ✨ Features

- 🔐 **Secure Authentication**: OAuth2 with JWT tokens
- 📊 **Transaction Management**: Track buy and sell operations
- 💰 **Portfolio Analysis**: Automatic profit/loss calculations
- 📈 **Real-time Statistics**: Per-stock and total portfolio summaries
- 🗄️ **MySQL Database**: Robust data persistence with SQLAlchemy ORM
- ✅ **Comprehensive Testing**: Full test coverage with pytest
- 📚 **Auto Documentation**: Interactive API docs with Swagger UI

## 🛠️ Technologies

- **Backend**: Python 3.11+, FastAPI
- **Database**: MySQL 8.0+ with SQLAlchemy ORM
- **Authentication**: OAuth2 + JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Validation**: Pydantic v2
- **Testing**: pytest, httpx
- **Documentation**: OpenAPI (Swagger/ReDoc)

## 📋 Prerequisites

- Python 3.11 or higher
- MySQL 8.0 or higher
- pip (Python package manager)
- Git

## 🚀 Quick Start

### 1. Clone the Repository
```powershell
git clone https://github.com/your-username/stock-portfolio-api.git
cd stock-portfolio-api
```

### 2. Create Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file:
```powershell
Copy-Item .env.example .env
```

Edit `.env` and update:
```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/stock_portfolio
SECRET_KEY=your-generated-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Generate a secure SECRET_KEY:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Create Database

Open MySQL and run:
```sql
CREATE DATABASE stock_portfolio CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Or use the provided script:
```powershell
mysql -u root -p < scripts\create_database.sql
```

### 6. Initialize Database Tables
```powershell
python scripts\init_db.py
```

### 7. Run the Application
```powershell
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once running, access the interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and get access token |
| GET | `/auth/me` | Get current user info |

### Transactions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/transactions/` | Create new transaction |
| GET | `/transactions/` | Get all user transactions |
| GET | `/transactions/{id}` | Get specific transaction |
| GET | `/transactions/stock/{symbol}` | Get transactions by stock |
| DELETE | `/transactions/{id}` | Delete transaction |

### Portfolio

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/portfolio/summary` | Get portfolio summary (all stocks) |
| GET | `/portfolio/summary/{symbol}` | Get summary for specific stock |
| GET | `/portfolio/total` | Get total portfolio statistics |

## 💡 Usage Examples

### Register a User
```powershell
curl -X POST "http://localhost:8000/auth/register" `
  -H "Content-Type: application/json" `
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepass123"
  }'
```

### Login
```powershell
curl -X POST "http://localhost:8000/auth/login" `
  -H "Content-Type: application/x-www-form-urlencoded" `
  -d "username=johndoe&password=securepass123"
```

### Create Transaction
```powershell
curl -X POST "http://localhost:8000/transactions/" `
  -H "Authorization: Bearer YOUR_TOKEN" `
  -H "Content-Type: application/json" `
  -d '{
    "stock_symbol": "AAPL",
    "stock_name": "Apple Inc.",
    "transaction_type": "buy",
    "quantity": 10,
    "price_per_share": 150.50
  }'
```

### Get Portfolio Summary
```powershell
curl -X GET "http://localhost:8000/portfolio/summary" `
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🧪 Running Tests

Run all tests:
```powershell
pytest
```

With verbose output:
```powershell
pytest -v
```

With coverage report:
```powershell
pytest --cov=app tests\
```

Run specific test file:
```powershell
pytest tests\test_auth.py -v
```

## 📊 Database Schema

### Users Table
- `id` (PK): User ID
- `email`: Unique email address
- `username`: Unique username
- `hashed_password`: Hashed password
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp

### Transactions Table
- `id` (PK): Transaction ID
- `user_id` (FK): Reference to user
- `stock_symbol`: Stock ticker symbol
- `stock_name`: Company name
- `transaction_type`: 'buy' or 'sell'
- `quantity`: Number of shares
- `price_per_share`: Price per share
- `total_amount`: Total transaction amount
- `transaction_date`: Transaction timestamp
- `notes`: Optional notes

## 🏗️ Project Structure
```
stock-portfolio-api/
│
├── app/
│   ├── auth/              # Authentication logic
│   │   ├── security.py    # Password & JWT utilities
│   │   └── dependencies.py # Auth dependencies
│   │
│   ├── database/          # Database configuration
│   │   └── connection.py  # SQLAlchemy setup
│   │
│   ├── models/            # Database models
│   │   ├── user.py
│   │   └── transaction.py
│   │
│   ├── routers/           # API endpoints
│   │   ├── auth.py
│   │   ├── transactions.py
│   │   └── portfolio.py
│   │
│   ├── schemas/           # Pydantic models
│   │   ├── user.py
│   │   └── transaction.py
│   │
│   ├── services/          # Business logic
│   │   └── portfolio_service.py
│   │
│   ├── config.py          # Configuration
│   └── main.py            # FastAPI app
│
├── scripts/               # Utility scripts
│   ├── create_database.sql
│   └── init_db.py
│
├── tests/                 # Test files
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_transactions.py
│   └── test_portfolio.py
│
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
├── pytest.ini             # Pytest configuration
├── requirements.txt       # Dependencies
└── README.md              # This file
```

## 🔒 Security

- ✅ Passwords hashed with bcrypt
- ✅ JWT tokens with expiration
- ✅ OAuth2 password flow
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Input validation (Pydantic)
- ✅ CORS middleware configured

## 🌿 Git Workflow

This project uses Git Flow with feature branches:
```
main (production)
  ↑
  └── develop (development)
        ↑
        ├── feature/initial-setup
        ├── feature/database-config
        ├── feature/database-models
        ├── feature/pydantic-schemas
        ├── feature/auth-system
        ├── feature/auth-endpoints
        ├── feature/portfolio-service
        ├── feature/transaction-endpoints
        ├── feature/portfolio-endpoints
        ├── feature/main-application
        ├── feature/testing
        └── feature/documentation
```

## 🤝 Contributing

Contributions are welcome! Please check [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Hayzam Adan**
- GitHub: [@hayzam98](https://github.com/hayzam98)
- LinkedIn: [Hayzam Adan](https://linkedin.com/in/hayzam-adan-martinez-3765a6102/)

## 🙏 Acknowledgments

- FastAPI documentation and community
- SQLAlchemy team
- Python community

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.
⭐ If you found this project helpful, please give it a star!