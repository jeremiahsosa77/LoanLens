from utils.calculations import (
    calculate_monthly_payment,
    calculate_amortization_schedule,
    calculate_apr,
    calculate_dti,
    calculate_payoff_plan,
    calculate_refinance_savings
)

def test_calculate_monthly_payment():
    """Test monthly payment calculation"""
    payment = calculate_monthly_payment(
        principal=100000,
        annual_rate=5.0,
        term_months=360  # 30 years
    )
    
    # Expected payment is approximately $536.82
    assert 535 < payment < 538

def test_calculate_amortization_schedule():
    """Test amortization schedule generation"""
    result = calculate_amortization_schedule(
        principal=10000,
        annual_rate=5.0,
        term_months=12
    )
    
    assert 'schedule' in result
    assert 'summary' in result
    assert len(result['schedule']) == 12
    assert result['summary']['total_payments'] == 12
    assert result['summary']['total_interest'] > 0

def test_calculate_apr():
    """Test APR calculation"""
    apr = calculate_apr(
        loan_amount=10000,
        monthly_payment=856.07,
        term_months=12,
        fees=200
    )
    
    # APR should be higher than the nominal rate due to fees
    assert apr > 0
    assert apr < 100

def test_calculate_dti():
    """Test DTI calculation"""
    dti = calculate_dti(
        monthly_debt_payments=2000,
        monthly_gross_income=6000
    )
    
    assert dti == 33.33

def test_calculate_payoff_plan_avalanche():
    """Test payoff plan with avalanche strategy"""
    loans = [
        {'name': 'Loan A', 'balance': 5000, 'rate': 10.0, 'min_payment': 200},
        {'name': 'Loan B', 'balance': 3000, 'rate': 15.0, 'min_payment': 150}
    ]
    
    result = calculate_payoff_plan(
        loans=loans,
        strategy='avalanche',
        extra_payment=100
    )
    
    assert 'timeline' in result
    assert 'months_to_payoff' in result
    assert 'total_interest' in result
    assert result['strategy'] == 'avalanche'

def test_calculate_refinance_savings():
    """Test refinance savings calculation"""
    current_loan = {
        'balance': 200000,
        'rate': 6.0,
        'remaining_months': 300,
        'monthly_payment': 1500
    }
    
    result = calculate_refinance_savings(
        current_loan=current_loan,
        new_rate=4.5,
        new_term_months=300,
        refinance_costs=3000
    )
    
    assert 'current' in result
    assert 'refinanced' in result
    assert 'savings' in result
    assert 'recommendation' in result
