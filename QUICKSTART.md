# LoanLens Quick Start Guide

## Prerequisites
- Docker and Docker Compose installed
- For local development: Python 3.11+, Node.js 18+

## Quick Start with Docker Compose

### 1. Clone and Setup
```bash
git clone https://github.com/jeremiahsosa77/LoanLens.git
cd LoanLens
cp .env.example .env
```

### 2. Start All Services
```bash
docker-compose up --build
```

This will start:
- PostgreSQL database on port 5432
- Flask backend API on port 5000
- React frontend on port 5173

### 3. Access the Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

### 4. Create Your First Account
1. Navigate to http://localhost:5173
2. Click "Sign up" to create an account
3. Complete the onboarding wizard
4. Start exploring the dashboard and scenario builder!

## Development Mode

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql://loanlens_user:loanlens_password@localhost:5432/loanlens_db
export SECRET_KEY=your-secret-key
export JWT_SECRET_KEY=your-jwt-secret-key

# Run the server
python app.py

# Run tests
pytest
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev  # Starts dev server on http://localhost:5173

# Run tests
npm test

# Build for production
npm run build
```

## Using the Application

### 1. Authentication
- Register a new account with email and password
- Login to access your dashboard

### 2. Complete Onboarding
- Add your personal information
- Set your annual income
- This information helps provide accurate financial calculations

### 3. Add Accounts and Loans
- From the dashboard, click "Add Account" to track your financial accounts
- Click "Add Loan" to add your loans (mortgages, auto loans, student loans, etc.)
- Each loan automatically calculates monthly payments

### 4. Create Financial Scenarios
- Click "Create Scenario" or navigate to the Scenario Builder
- Choose calculation type:
  - **Amortization Schedule**: See how your loan payments break down over time
  - **Payoff Plan**: Optimize paying off multiple loans (avalanche or snowball method)
  - **Monthly Payment Calculator**: Calculate payments for a new loan
- Configure parameters (loan amount, interest rate, term, extra payments)
- Get instant results with visual charts

### 5. View Your Dashboard
- See all your loans and accounts at a glance
- Visual charts showing loan distribution
- Track total debt, monthly payments, and assets

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login
- `GET /auth/me` - Get current user

### Financial Data
- `GET /loans` - List all loans
- `POST /loans` - Create new loan
- `GET /accounts` - List all accounts
- `POST /accounts` - Create new account
- `GET /scenarios` - List all scenarios
- `POST /scenarios` - Create new scenario

### Calculations
- `POST /calculate/amortization` - Generate amortization schedule
- `POST /calculate/payoff` - Calculate multi-loan payoff plan
- `POST /calculate/monthly-payment` - Calculate monthly payment
- `POST /calculate/apr` - Calculate APR
- `POST /calculate/dti` - Calculate debt-to-income ratio
- `POST /calculate/refinance` - Analyze refinance savings

## Troubleshooting

### Docker Issues
```bash
# Stop all services
docker-compose down

# Remove volumes and rebuild
docker-compose down -v
docker-compose up --build
```

### Database Migration Issues
```bash
# Enter backend container
docker exec -it loanlens_backend bash

# Run migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Frontend Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

## Testing

### Run All Tests
```bash
# Backend
cd backend
pytest -v

# Frontend
cd frontend
npm test
```

### Check Code Coverage
```bash
# Backend
cd backend
pytest --cov

# Frontend
cd frontend
npm test -- --coverage
```

## Production Deployment

1. Update `.env` with production values
2. Set strong `SECRET_KEY` and `JWT_SECRET_KEY`
3. Use production PostgreSQL database
4. Build production images:
```bash
docker-compose -f docker-compose.yml up --build -d
```

## Support

For issues, questions, or contributions, please open an issue on GitHub.
