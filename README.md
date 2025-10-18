# LoanLens

A full-stack financial planning application that enables complex, real-time financial calculations to generate personalized loan and credit scenarios for users.

## Features

### Backend (Python Flask API)
- **Authentication**: JWT-based auth with bcrypt password hashing
- **Database**: PostgreSQL with SQLAlchemy ORM and Alembic migrations
- **Models**: User, Profile, Account, Loan, Scenario, Result
- **API Routes**:
  - `/auth` - User registration, login, token refresh
  - `/profile` - User profile management
  - `/accounts` - Financial account tracking
  - `/loans` - Loan management
  - `/scenarios` - Scenario creation and analysis
  - `/calculate` - Financial calculations (amortization, APR, DTI, payoff, refinance)
- **Calculations Module**:
  - Amortization schedule generation
  - APR calculation
  - Debt-to-Income ratio
  - Multi-loan payoff planning (avalanche/snowball)
  - Refinance savings analysis
- **Testing**: Pytest with coverage reporting

### Frontend (React + Vite + Tailwind CSS)
- **Pages**:
  - **Onboarding Wizard**: Multi-step user profile setup
  - **Dashboard**: Overview with charts showing loan distribution and financial summary
  - **Scenario Builder**: Interactive calculator with live results and charts
- **Features**:
  - API client with automatic token refresh
  - Protected routes with authentication
  - Form validation
  - Responsive design with Tailwind CSS
  - Interactive charts with Recharts
- **Testing**: Vitest for unit tests

## Technology Stack

### Backend
- Python 3.11
- Flask 3.0
- SQLAlchemy 2.0
- PostgreSQL 16
- Flask-JWT-Extended
- Flask-Bcrypt
- Alembic
- Pytest

### Frontend
- React 18
- Vite 5
- Tailwind CSS 3
- React Router DOM
- Axios
- Recharts
- React Hook Form
- Zod
- Vitest

### DevOps
- Docker & Docker Compose
- GitHub Actions CI
- PostgreSQL (containerized)

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/jeremiahsosa77/LoanLens.git
cd LoanLens
```

2. Copy environment variables:
```bash
cp .env.example .env
```

3. Start the application:
```bash
docker-compose up --build
```

4. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000

### Local Development

#### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export DATABASE_URL=postgresql://loanlens_user:loanlens_password@localhost:5432/loanlens_db
export SECRET_KEY=your-secret-key
export JWT_SECRET_KEY=your-jwt-secret-key
```

5. Initialize database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Run the application:
```bash
python app.py
```

7. Run tests:
```bash
pytest
```

#### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

4. Run tests:
```bash
npm test
```

5. Build for production:
```bash
npm run build
```

## API Documentation

### Authentication Endpoints

- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/refresh` - Refresh access token
- `GET /auth/me` - Get current user

### Profile Endpoints

- `GET /profile` - Get user profile
- `POST /profile` - Create/update profile
- `DELETE /profile` - Delete profile

### Account Endpoints

- `GET /accounts` - List all accounts
- `GET /accounts/:id` - Get specific account
- `POST /accounts` - Create account
- `PUT /accounts/:id` - Update account
- `DELETE /accounts/:id` - Delete account

### Loan Endpoints

- `GET /loans` - List all loans
- `GET /loans/:id` - Get specific loan
- `POST /loans` - Create loan
- `PUT /loans/:id` - Update loan
- `DELETE /loans/:id` - Delete loan

### Scenario Endpoints

- `GET /scenarios` - List all scenarios
- `GET /scenarios/:id` - Get specific scenario
- `POST /scenarios` - Create scenario
- `PUT /scenarios/:id` - Update scenario
- `DELETE /scenarios/:id` - Delete scenario

### Calculation Endpoints

- `POST /calculate/amortization` - Generate amortization schedule
- `POST /calculate/apr` - Calculate APR
- `POST /calculate/dti` - Calculate debt-to-income ratio
- `POST /calculate/payoff` - Calculate payoff plan
- `POST /calculate/refinance` - Analyze refinance savings
- `POST /calculate/monthly-payment` - Calculate monthly payment

## Project Structure

```
LoanLens/
├── backend/
│   ├── models/          # Database models
│   ├── routes/          # API routes
│   ├── utils/           # Utility functions (calculations)
│   ├── tests/           # Backend tests
│   ├── migrations/      # Database migrations
│   ├── app.py           # Flask application
│   ├── requirements.txt # Python dependencies
│   └── Dockerfile       # Backend Docker config
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API client
│   │   ├── hooks/       # Custom React hooks
│   │   └── utils/       # Utility functions
│   ├── package.json     # Node dependencies
│   ├── vite.config.js   # Vite configuration
│   ├── tailwind.config.js # Tailwind configuration
│   └── Dockerfile       # Frontend Docker config
├── .github/
│   └── workflows/
│       └── ci.yml       # GitHub Actions CI
├── docker-compose.yml   # Docker Compose configuration
├── .env.example         # Environment variables template
└── README.md            # This file
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Run All Tests with Coverage
```bash
# Backend
cd backend
pytest --cov

# Frontend
cd frontend
npm test -- --coverage
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

Built with modern web technologies to provide accurate financial planning and loan analysis tools.
