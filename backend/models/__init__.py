from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profile = relationship('Profile', back_populates='user', uselist=False, cascade='all, delete-orphan')
    accounts = relationship('Account', back_populates='user', cascade='all, delete-orphan')
    scenarios = relationship('Scenario', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'

class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    date_of_birth = Column(DateTime)
    annual_income = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='profile')
    
    def __repr__(self):
        return f'<Profile {self.first_name} {self.last_name}>'

class Account(db.Model):
    __tablename__ = 'accounts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    account_type = Column(String(50), nullable=False)  # checking, savings, credit_card, etc.
    account_name = Column(String(100), nullable=False)
    balance = Column(Float, default=0.0)
    interest_rate = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='accounts')
    loans = relationship('Loan', back_populates='account', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Account {self.account_name}>'

class Loan(db.Model):
    __tablename__ = 'loans'
    
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    loan_type = Column(String(50), nullable=False)  # mortgage, auto, personal, student, etc.
    loan_name = Column(String(100), nullable=False)
    principal = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    term_months = Column(Integer, nullable=False)
    monthly_payment = Column(Float)
    start_date = Column(DateTime)
    remaining_balance = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    account = relationship('Account', back_populates='loans')
    
    def __repr__(self):
        return f'<Loan {self.loan_name}>'

class Scenario(db.Model):
    __tablename__ = 'scenarios'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    scenario_type = Column(String(50))  # payoff_plan, refinance, comparison, etc.
    parameters = Column(Text)  # JSON string of scenario parameters
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='scenarios')
    results = relationship('Result', back_populates='scenario', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Scenario {self.name}>'

class Result(db.Model):
    __tablename__ = 'results'
    
    id = Column(Integer, primary_key=True)
    scenario_id = Column(Integer, ForeignKey('scenarios.id'), nullable=False)
    calculation_type = Column(String(50), nullable=False)  # amortization, apr, dti, etc.
    data = Column(Text)  # JSON string of calculation results
    total_interest = Column(Float)
    total_payment = Column(Float)
    payoff_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    scenario = relationship('Scenario', back_populates='results')
    
    def __repr__(self):
        return f'<Result {self.calculation_type}>'
