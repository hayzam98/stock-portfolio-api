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

The application will be available at:
- **🌐 Web Interface**: http://localhost:8000 (User-friendly UI)
- **📚 API Documentation**: http://localhost:8000/docs (Swagger UI)
- **🏥 Health Check**: http://localhost:8000/health
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

## 📊 Stock Price Integration

The API integrates with **Yahoo Finance** to provide real-time stock prices and information.

### Features

- ✅ **Real-time Prices**: Get current stock prices
- ✅ **Stock Information**: Company details, market cap, sector, etc.
- ✅ **Historical Data**: Access historical price data
- ✅ **Symbol Validation**: Check if a stock symbol exists
- ✅ **Smart Caching**: 5-minute cache to reduce API calls
- ✅ **Auto-fill**: Web interface automatically fetches prices
- ✅ **Watchlist**: Monitor stocks without buying them

### Stock Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/stocks/price/{symbol}` | Get current price |
| GET | `/stocks/info/{symbol}` | Get detailed information |
| GET | `/stocks/history/{symbol}` | Get historical prices |
| POST | `/stocks/validate/{symbol}` | Validate symbol |

### Example Usage
```powershell
# Get current price for Apple
curl -X GET "http://localhost:8000/stocks/price/AAPL" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response:
{
  "symbol": "AAPL",
  "current_price": 185.50,
  "currency": "USD"
}

# Get detailed stock info
curl -X GET "http://localhost:8000/stocks/info/GOOGL" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get historical data for Microsoft
curl -X GET "http://localhost:8000/stocks/history/MSFT?period=1mo" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Supported Stock Symbols

Any valid stock symbol from major exchanges:
- 🇺🇸 US Stocks: AAPL, GOOGL, MSFT, AMZN, TSLA, etc.
- 🌍 International: Add exchange suffix (e.g., NESN.SW, BP.L)

### Historical Data Periods

- `1d`, `5d`, `1mo`, `3mo`, `6mo`
- `1y`, `2y`, `5y`, `10y`
- `ytd` (year to date)
- `max` (maximum available)

### Portfolio Integration

Portfolio summaries use **real-time prices** from Yahoo Finance:
- Current value = Shares × Real-time price
- Profit/Loss calculated with actual market prices
- Automatic fallback to last transaction price if API fails

### Caching

- Prices are cached for **5 minutes**
- Reduces API calls and improves performance
- Cache is cleared on server restart

## 🌐 Web Interface

The application includes a **user-friendly web interface** accessible at `http://localhost:8000/`

### Features

#### 🔐 Authentication
- **Register**: Create a new account with email and username
- **Login**: Secure login with JWT tokens
- **Session Persistence**: Stay logged in using localStorage
- **User Profile**: View current user information

#### 📊 Transactions
- **Create Transactions**: Buy or sell stocks with real-time prices
- **Auto-fill**: Type a stock symbol and automatically get:
  - Company name
  - Current market price
  - Calculated total
- **Transaction History**: View all your transactions
- **Filter**: Filter by stock symbol or transaction type
- **Delete**: Remove unwanted transactions

#### 💼 Portfolio
- **Dashboard**: Overview of your entire portfolio
- **Summary Cards**: See at a glance:
  - Total Current Value
  - Total Invested
  - Total Profit/Loss
  - Return Percentage
- **Per-Stock Details**: Individual holdings with:
  - Shares owned
  - Average buy price
  - Current value
  - Profit/Loss amount and percentage
- **Real-time Updates**: Uses live market prices

#### 👁️ Watchlist (Lista de Seguimiento)
- **Monitor Stocks**: Track stocks without buying them
- **Real-time Prices**: See current market prices
- **Price Changes**: View daily change (amount and percentage)
- **Market Data**: Display opening price, daily high/low, previous close
- **Easy Management**: Add or remove stocks with one click
- **Persistent**: Watchlist saved in localStorage
- **Manual Refresh**: Update all prices on demand

#### ➕ New Transaction
- **Smart Form**: Auto-calculating total amount
- **Stock Lookup**: Real-time price fetching
- **Validation**: Prevents selling more than you own
- **Notes**: Add optional notes to transactions

### Web Interface Screenshots

#### Main Dashboard
```
┌─────────────────────────────────────────────────────────┐
│  📈 Stock Portfolio Manager          Hola, juan [Logout]│
├─────────────────────────────────────────────────────────┤
│  [📊 Transacciones] [💼 Portfolio] [👁️ Lista de Seguimiento] [➕ Nueva Transacción] │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Current Section: Transactions / Portfolio / Watchlist  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

#### Transaction Auto-fill Example
1. User types: "AAPL"
2. System fetches info (0.8s delay)
3. Auto-fills:
   - Name: "Apple Inc."
   - Price: "$185.50"
   - Total: Calculated automatically

#### Watchlist Example
```
┌─────────────────────────────────────────────────────────┐
│  AAPL                                    $185.50         │
│  Apple Inc.                              +$2.30 (+1.26%) │
│  ─────────────────────────────────────────────────────  │
│  Apertura: $183.20  │  Máximo: $186.00                  │
│  Mínimo: $182.50    │  Cierre Ant.: $183.20             │
│  [🗑️ Eliminar]                                          │
└─────────────────────────────────────────────────────────┘
```

### Benefits Over Swagger UI

| Feature | Web Interface | Swagger UI |
|---------|---------------|------------|
| User-friendly | ✅ Very easy | ❌ Technical |
| Visual Design | ✅ Modern | ⚠️ Basic |
| Auto-calculations | ✅ Yes | ❌ No |
| Real-time prices | ✅ Yes | ❌ Manual |
| Watchlist | ✅ Yes | ❌ No |
| For end users | ✅ Perfect | ❌ Developers only |

Both interfaces are available and work simultaneously:
- **Web UI**: `http://localhost:8000/` - For regular users
- **Swagger UI**: `http://localhost:8000/docs` - For developers/testing

### Technology Stack

The web interface uses:
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **Vanilla JavaScript**: No frameworks needed
- **LocalStorage**: Client-side data persistence
- **Fetch API**: RESTful API communication

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