from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Scenario, Result
import json

scenarios_bp = Blueprint('scenarios', __name__)

@scenarios_bp.route('/', methods=['GET'])
@jwt_required()
def get_scenarios():
    """Get all scenarios for current user"""
    current_user_id = get_jwt_identity()
    scenarios = Scenario.query.filter_by(user_id=current_user_id).all()
    
    return jsonify({
        'scenarios': [{
            'id': scenario.id,
            'name': scenario.name,
            'description': scenario.description,
            'scenario_type': scenario.scenario_type,
            'parameters': json.loads(scenario.parameters) if scenario.parameters else {},
            'created_at': scenario.created_at.isoformat()
        } for scenario in scenarios]
    }), 200

@scenarios_bp.route('/<int:scenario_id>', methods=['GET'])
@jwt_required()
def get_scenario(scenario_id):
    """Get specific scenario with results"""
    current_user_id = get_jwt_identity()
    scenario = Scenario.query.filter_by(id=scenario_id, user_id=current_user_id).first()
    
    if not scenario:
        return jsonify({'error': 'Scenario not found'}), 404
    
    return jsonify({
        'id': scenario.id,
        'name': scenario.name,
        'description': scenario.description,
        'scenario_type': scenario.scenario_type,
        'parameters': json.loads(scenario.parameters) if scenario.parameters else {},
        'results': [{
            'id': result.id,
            'calculation_type': result.calculation_type,
            'data': json.loads(result.data) if result.data else {},
            'total_interest': result.total_interest,
            'total_payment': result.total_payment,
            'payoff_date': result.payoff_date.isoformat() if result.payoff_date else None
        } for result in scenario.results],
        'created_at': scenario.created_at.isoformat()
    }), 200

@scenarios_bp.route('/', methods=['POST'])
@jwt_required()
def create_scenario():
    """Create new scenario"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Scenario name is required'}), 400
    
    scenario = Scenario(
        user_id=current_user_id,
        name=data['name'],
        description=data.get('description'),
        scenario_type=data.get('scenario_type'),
        parameters=json.dumps(data.get('parameters', {}))
    )
    
    db.session.add(scenario)
    db.session.commit()
    
    return jsonify({
        'message': 'Scenario created successfully',
        'scenario': {
            'id': scenario.id,
            'name': scenario.name,
            'description': scenario.description,
            'scenario_type': scenario.scenario_type,
            'parameters': json.loads(scenario.parameters) if scenario.parameters else {}
        }
    }), 201

@scenarios_bp.route('/<int:scenario_id>', methods=['PUT'])
@jwt_required()
def update_scenario(scenario_id):
    """Update scenario"""
    current_user_id = get_jwt_identity()
    scenario = Scenario.query.filter_by(id=scenario_id, user_id=current_user_id).first()
    
    if not scenario:
        return jsonify({'error': 'Scenario not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        scenario.name = data['name']
    if 'description' in data:
        scenario.description = data['description']
    if 'scenario_type' in data:
        scenario.scenario_type = data['scenario_type']
    if 'parameters' in data:
        scenario.parameters = json.dumps(data['parameters'])
    
    db.session.commit()
    
    return jsonify({
        'message': 'Scenario updated successfully',
        'scenario': {
            'id': scenario.id,
            'name': scenario.name,
            'description': scenario.description,
            'scenario_type': scenario.scenario_type,
            'parameters': json.loads(scenario.parameters) if scenario.parameters else {}
        }
    }), 200

@scenarios_bp.route('/<int:scenario_id>', methods=['DELETE'])
@jwt_required()
def delete_scenario(scenario_id):
    """Delete scenario"""
    current_user_id = get_jwt_identity()
    scenario = Scenario.query.filter_by(id=scenario_id, user_id=current_user_id).first()
    
    if not scenario:
        return jsonify({'error': 'Scenario not found'}), 404
    
    db.session.delete(scenario)
    db.session.commit()
    
    return jsonify({'message': 'Scenario deleted successfully'}), 200
