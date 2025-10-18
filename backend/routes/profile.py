from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Profile, User

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    current_user_id = get_jwt_identity()
    profile = Profile.query.filter_by(user_id=current_user_id).first()
    
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    return jsonify({
        'id': profile.id,
        'first_name': profile.first_name,
        'last_name': profile.last_name,
        'phone': profile.phone,
        'date_of_birth': profile.date_of_birth.isoformat() if profile.date_of_birth else None,
        'annual_income': profile.annual_income
    }), 200

@profile_bp.route('/', methods=['POST', 'PUT'])
@jwt_required()
def create_or_update_profile():
    """Create or update user profile"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    profile = Profile.query.filter_by(user_id=current_user_id).first()
    
    if profile:
        # Update existing profile
        if 'first_name' in data:
            profile.first_name = data['first_name']
        if 'last_name' in data:
            profile.last_name = data['last_name']
        if 'phone' in data:
            profile.phone = data['phone']
        if 'date_of_birth' in data:
            from datetime import datetime
            profile.date_of_birth = datetime.fromisoformat(data['date_of_birth'])
        if 'annual_income' in data:
            profile.annual_income = data['annual_income']
    else:
        # Create new profile
        profile = Profile(
            user_id=current_user_id,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone=data.get('phone'),
            annual_income=data.get('annual_income')
        )
        if data.get('date_of_birth'):
            from datetime import datetime
            profile.date_of_birth = datetime.fromisoformat(data['date_of_birth'])
        
        db.session.add(profile)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Profile saved successfully',
        'profile': {
            'id': profile.id,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'phone': profile.phone,
            'date_of_birth': profile.date_of_birth.isoformat() if profile.date_of_birth else None,
            'annual_income': profile.annual_income
        }
    }), 200

@profile_bp.route('/', methods=['DELETE'])
@jwt_required()
def delete_profile():
    """Delete user profile"""
    current_user_id = get_jwt_identity()
    profile = Profile.query.filter_by(user_id=current_user_id).first()
    
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    db.session.delete(profile)
    db.session.commit()
    
    return jsonify({'message': 'Profile deleted successfully'}), 200
