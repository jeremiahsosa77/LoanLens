from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Loan, Account

loans_bp = Blueprint('loans', __name__)

@loans_bp.route('/', methods=['GET'])
@jwt_required()
def get_loans():
    """Get all loans for current user"""
    current_user_id = get_jwt_identity()
    
    # Get loans through accounts
    accounts = Account.query.filter_by(user_id=current_user_id).all()
    account_ids = [acc.id for acc in accounts]
    loans = Loan.query.filter(Loan.account_id.in_(account_ids)).all()
    
    return jsonify({
        'loans': [{
            'id': loan.id,
            'account_id': loan.account_id,
            'loan_type': loan.loan_type,
            'loan_name': loan.loan_name,
            'principal': loan.principal,
            'interest_rate': loan.interest_rate,
            'term_months': loan.term_months,
            'monthly_payment': loan.monthly_payment,
            'remaining_balance': loan.remaining_balance,
            'start_date': loan.start_date.isoformat() if loan.start_date else None
        } for loan in loans]
    }), 200

@loans_bp.route('/<int:loan_id>', methods=['GET'])
@jwt_required()
def get_loan(loan_id):
    """Get specific loan"""
    current_user_id = get_jwt_identity()
    
    loan = Loan.query.join(Account).filter(
        Loan.id == loan_id,
        Account.user_id == current_user_id
    ).first()
    
    if not loan:
        return jsonify({'error': 'Loan not found'}), 404
    
    return jsonify({
        'id': loan.id,
        'account_id': loan.account_id,
        'loan_type': loan.loan_type,
        'loan_name': loan.loan_name,
        'principal': loan.principal,
        'interest_rate': loan.interest_rate,
        'term_months': loan.term_months,
        'monthly_payment': loan.monthly_payment,
        'remaining_balance': loan.remaining_balance,
        'start_date': loan.start_date.isoformat() if loan.start_date else None
    }), 200

@loans_bp.route('/', methods=['POST'])
@jwt_required()
def create_loan():
    """Create new loan"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not all(k in data for k in ['account_id', 'loan_type', 'loan_name', 'principal', 'interest_rate', 'term_months']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Verify account belongs to user
    account = Account.query.filter_by(id=data['account_id'], user_id=current_user_id).first()
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    
    # Calculate monthly payment
    from utils.calculations import calculate_monthly_payment
    monthly_payment = calculate_monthly_payment(
        data['principal'],
        data['interest_rate'],
        data['term_months']
    )
    
    loan = Loan(
        account_id=data['account_id'],
        loan_type=data['loan_type'],
        loan_name=data['loan_name'],
        principal=data['principal'],
        interest_rate=data['interest_rate'],
        term_months=data['term_months'],
        monthly_payment=monthly_payment,
        remaining_balance=data.get('remaining_balance', data['principal'])
    )
    
    if data.get('start_date'):
        from datetime import datetime
        loan.start_date = datetime.fromisoformat(data['start_date'])
    
    db.session.add(loan)
    db.session.commit()
    
    return jsonify({
        'message': 'Loan created successfully',
        'loan': {
            'id': loan.id,
            'loan_type': loan.loan_type,
            'loan_name': loan.loan_name,
            'principal': loan.principal,
            'interest_rate': loan.interest_rate,
            'term_months': loan.term_months,
            'monthly_payment': loan.monthly_payment
        }
    }), 201

@loans_bp.route('/<int:loan_id>', methods=['PUT'])
@jwt_required()
def update_loan(loan_id):
    """Update loan"""
    current_user_id = get_jwt_identity()
    
    loan = Loan.query.join(Account).filter(
        Loan.id == loan_id,
        Account.user_id == current_user_id
    ).first()
    
    if not loan:
        return jsonify({'error': 'Loan not found'}), 404
    
    data = request.get_json()
    
    # Update fields
    if 'loan_type' in data:
        loan.loan_type = data['loan_type']
    if 'loan_name' in data:
        loan.loan_name = data['loan_name']
    if 'remaining_balance' in data:
        loan.remaining_balance = data['remaining_balance']
    
    # Recalculate if principal, rate, or term changed
    recalc = False
    if 'principal' in data:
        loan.principal = data['principal']
        recalc = True
    if 'interest_rate' in data:
        loan.interest_rate = data['interest_rate']
        recalc = True
    if 'term_months' in data:
        loan.term_months = data['term_months']
        recalc = True
    
    if recalc:
        from utils.calculations import calculate_monthly_payment
        loan.monthly_payment = calculate_monthly_payment(
            loan.principal,
            loan.interest_rate,
            loan.term_months
        )
    
    db.session.commit()
    
    return jsonify({
        'message': 'Loan updated successfully',
        'loan': {
            'id': loan.id,
            'loan_type': loan.loan_type,
            'loan_name': loan.loan_name,
            'principal': loan.principal,
            'interest_rate': loan.interest_rate,
            'term_months': loan.term_months,
            'monthly_payment': loan.monthly_payment
        }
    }), 200

@loans_bp.route('/<int:loan_id>', methods=['DELETE'])
@jwt_required()
def delete_loan(loan_id):
    """Delete loan"""
    current_user_id = get_jwt_identity()
    
    loan = Loan.query.join(Account).filter(
        Loan.id == loan_id,
        Account.user_id == current_user_id
    ).first()
    
    if not loan:
        return jsonify({'error': 'Loan not found'}), 404
    
    db.session.delete(loan)
    db.session.commit()
    
    return jsonify({'message': 'Loan deleted successfully'}), 200
