from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Account

accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route('/', methods=['GET'])
@jwt_required()
def get_accounts():
    """Get all accounts for current user"""
    current_user_id = get_jwt_identity()
    accounts = Account.query.filter_by(user_id=current_user_id).all()
    
    return jsonify({
        'accounts': [{
            'id': account.id,
            'account_type': account.account_type,
            'account_name': account.account_name,
            'balance': account.balance,
            'interest_rate': account.interest_rate,
            'created_at': account.created_at.isoformat()
        } for account in accounts]
    }), 200

@accounts_bp.route('/<int:account_id>', methods=['GET'])
@jwt_required()
def get_account(account_id):
    """Get specific account"""
    current_user_id = get_jwt_identity()
    account = Account.query.filter_by(id=account_id, user_id=current_user_id).first()
    
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    
    return jsonify({
        'id': account.id,
        'account_type': account.account_type,
        'account_name': account.account_name,
        'balance': account.balance,
        'interest_rate': account.interest_rate,
        'created_at': account.created_at.isoformat()
    }), 200

@accounts_bp.route('/', methods=['POST'])
@jwt_required()
def create_account():
    """Create new account"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('account_type') or not data.get('account_name'):
        return jsonify({'error': 'account_type and account_name are required'}), 400
    
    account = Account(
        user_id=current_user_id,
        account_type=data['account_type'],
        account_name=data['account_name'],
        balance=data.get('balance', 0.0),
        interest_rate=data.get('interest_rate')
    )
    
    db.session.add(account)
    db.session.commit()
    
    return jsonify({
        'message': 'Account created successfully',
        'account': {
            'id': account.id,
            'account_type': account.account_type,
            'account_name': account.account_name,
            'balance': account.balance,
            'interest_rate': account.interest_rate
        }
    }), 201

@accounts_bp.route('/<int:account_id>', methods=['PUT'])
@jwt_required()
def update_account(account_id):
    """Update account"""
    current_user_id = get_jwt_identity()
    account = Account.query.filter_by(id=account_id, user_id=current_user_id).first()
    
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    
    data = request.get_json()
    
    if 'account_type' in data:
        account.account_type = data['account_type']
    if 'account_name' in data:
        account.account_name = data['account_name']
    if 'balance' in data:
        account.balance = data['balance']
    if 'interest_rate' in data:
        account.interest_rate = data['interest_rate']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Account updated successfully',
        'account': {
            'id': account.id,
            'account_type': account.account_type,
            'account_name': account.account_name,
            'balance': account.balance,
            'interest_rate': account.interest_rate
        }
    }), 200

@accounts_bp.route('/<int:account_id>', methods=['DELETE'])
@jwt_required()
def delete_account(account_id):
    """Delete account"""
    current_user_id = get_jwt_identity()
    account = Account.query.filter_by(id=account_id, user_id=current_user_id).first()
    
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    
    db.session.delete(account)
    db.session.commit()
    
    return jsonify({'message': 'Account deleted successfully'}), 200
