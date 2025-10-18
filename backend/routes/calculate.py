from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.calculations import (
    calculate_amortization_schedule,
    calculate_apr,
    calculate_dti,
    calculate_payoff_plan,
    calculate_refinance_savings,
    calculate_monthly_payment
)

calculate_bp = Blueprint('calculate', __name__)

@calculate_bp.route('/amortization', methods=['POST'])
@jwt_required()
def amortization():
    """Calculate amortization schedule"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['principal', 'annual_rate', 'term_months']):
        return jsonify({'error': 'principal, annual_rate, and term_months are required'}), 400
    
    try:
        result = calculate_amortization_schedule(
            principal=float(data['principal']),
            annual_rate=float(data['annual_rate']),
            term_months=int(data['term_months']),
            extra_payment=float(data.get('extra_payment', 0))
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@calculate_bp.route('/apr', methods=['POST'])
@jwt_required()
def apr():
    """Calculate Annual Percentage Rate"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['loan_amount', 'monthly_payment', 'term_months']):
        return jsonify({'error': 'loan_amount, monthly_payment, and term_months are required'}), 400
    
    try:
        result = calculate_apr(
            loan_amount=float(data['loan_amount']),
            monthly_payment=float(data['monthly_payment']),
            term_months=int(data['term_months']),
            fees=float(data.get('fees', 0))
        )
        return jsonify({'apr': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@calculate_bp.route('/dti', methods=['POST'])
@jwt_required()
def dti():
    """Calculate Debt-to-Income ratio"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['monthly_debt_payments', 'monthly_gross_income']):
        return jsonify({'error': 'monthly_debt_payments and monthly_gross_income are required'}), 400
    
    try:
        result = calculate_dti(
            monthly_debt_payments=float(data['monthly_debt_payments']),
            monthly_gross_income=float(data['monthly_gross_income'])
        )
        return jsonify({'dti': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@calculate_bp.route('/payoff', methods=['POST'])
@jwt_required()
def payoff():
    """Calculate payoff plan for multiple loans"""
    data = request.get_json()
    
    if not data or not data.get('loans'):
        return jsonify({'error': 'loans array is required'}), 400
    
    try:
        result = calculate_payoff_plan(
            loans=data['loans'],
            strategy=data.get('strategy', 'avalanche'),
            extra_payment=float(data.get('extra_payment', 0))
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@calculate_bp.route('/refinance', methods=['POST'])
@jwt_required()
def refinance():
    """Calculate refinance savings"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['current_loan', 'new_rate', 'new_term_months']):
        return jsonify({'error': 'current_loan, new_rate, and new_term_months are required'}), 400
    
    try:
        result = calculate_refinance_savings(
            current_loan=data['current_loan'],
            new_rate=float(data['new_rate']),
            new_term_months=int(data['new_term_months']),
            refinance_costs=float(data.get('refinance_costs', 0))
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@calculate_bp.route('/monthly-payment', methods=['POST'])
@jwt_required()
def monthly_payment():
    """Calculate monthly payment"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['principal', 'annual_rate', 'term_months']):
        return jsonify({'error': 'principal, annual_rate, and term_months are required'}), 400
    
    try:
        result = calculate_monthly_payment(
            principal=float(data['principal']),
            annual_rate=float(data['annual_rate']),
            term_months=int(data['term_months'])
        )
        return jsonify({'monthly_payment': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
