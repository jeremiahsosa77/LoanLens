"""
Financial calculation utilities for LoanLens
Includes: amortization, APR, DTI, payoff, refinance calculations
"""
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import math

def calculate_monthly_payment(principal, annual_rate, term_months):
    """
    Calculate monthly payment for a loan using the standard formula.
    
    Args:
        principal: Loan principal amount
        annual_rate: Annual interest rate (as percentage, e.g., 5.5 for 5.5%)
        term_months: Loan term in months
    
    Returns:
        Monthly payment amount
    """
    if annual_rate == 0:
        return principal / term_months
    
    monthly_rate = (annual_rate / 100) / 12
    payment = principal * (monthly_rate * (1 + monthly_rate)**term_months) / \
              ((1 + monthly_rate)**term_months - 1)
    return round(payment, 2)

def calculate_amortization_schedule(principal, annual_rate, term_months, start_date=None, extra_payment=0):
    """
    Generate complete amortization schedule for a loan.
    
    Args:
        principal: Loan principal amount
        annual_rate: Annual interest rate (as percentage)
        term_months: Loan term in months
        start_date: Starting date for the loan (defaults to today)
        extra_payment: Additional monthly payment amount
    
    Returns:
        Dictionary containing schedule and summary information
    """
    if start_date is None:
        start_date = datetime.now()
    
    monthly_payment = calculate_monthly_payment(principal, annual_rate, term_months)
    monthly_rate = (annual_rate / 100) / 12
    
    schedule = []
    balance = principal
    total_interest = 0
    total_principal = 0
    
    payment_number = 1
    current_date = start_date
    
    while balance > 0 and payment_number <= term_months:
        interest_payment = balance * monthly_rate
        principal_payment = min(monthly_payment - interest_payment + extra_payment, balance)
        
        if principal_payment < 0:
            principal_payment = balance
            
        balance -= principal_payment
        total_interest += interest_payment
        total_principal += principal_payment
        
        schedule.append({
            'payment_number': payment_number,
            'date': current_date.strftime('%Y-%m-%d'),
            'payment': round(monthly_payment + extra_payment, 2),
            'principal': round(principal_payment, 2),
            'interest': round(interest_payment, 2),
            'balance': round(max(balance, 0), 2)
        })
        
        payment_number += 1
        current_date += relativedelta(months=1)
    
    return {
        'schedule': schedule,
        'summary': {
            'monthly_payment': round(monthly_payment, 2),
            'total_payments': len(schedule),
            'total_interest': round(total_interest, 2),
            'total_principal': round(total_principal, 2),
            'total_amount': round(total_interest + total_principal, 2),
            'payoff_date': schedule[-1]['date'] if schedule else None
        }
    }

def calculate_apr(loan_amount, monthly_payment, term_months, fees=0):
    """
    Calculate Annual Percentage Rate (APR) for a loan.
    
    Args:
        loan_amount: Principal amount
        monthly_payment: Monthly payment amount
        term_months: Loan term in months
        fees: Upfront fees and costs
    
    Returns:
        APR as a percentage
    """
    # Adjust loan amount for fees
    net_loan = loan_amount - fees
    
    # Use iterative method to find APR
    def npv(rate):
        """Calculate net present value"""
        pv = sum([monthly_payment / ((1 + rate) ** i) for i in range(1, term_months + 1)])
        return pv - net_loan
    
    # Binary search for the rate
    low, high = 0.0, 1.0
    tolerance = 0.0001
    
    while high - low > tolerance:
        mid = (low + high) / 2
        if npv(mid) > 0:
            low = mid
        else:
            high = mid
    
    monthly_rate = (low + high) / 2
    apr = monthly_rate * 12 * 100
    return round(apr, 2)

def calculate_dti(monthly_debt_payments, monthly_gross_income):
    """
    Calculate Debt-to-Income ratio.
    
    Args:
        monthly_debt_payments: Total monthly debt payments
        monthly_gross_income: Monthly gross income
    
    Returns:
        DTI ratio as a percentage
    """
    if monthly_gross_income == 0:
        return 0
    
    dti = (monthly_debt_payments / monthly_gross_income) * 100
    return round(dti, 2)

def calculate_payoff_plan(loans, strategy='avalanche', extra_payment=0):
    """
    Calculate optimal payoff plan for multiple loans.
    
    Args:
        loans: List of loan dictionaries with keys: name, balance, rate, min_payment
        strategy: 'avalanche' (highest rate first) or 'snowball' (lowest balance first)
        extra_payment: Extra amount to apply each month
    
    Returns:
        Payoff plan with timeline and savings
    """
    # Sort loans based on strategy
    if strategy == 'avalanche':
        sorted_loans = sorted(loans, key=lambda x: x['rate'], reverse=True)
    else:  # snowball
        sorted_loans = sorted(loans, key=lambda x: x['balance'])
    
    # Calculate payoff
    month = 0
    total_interest = 0
    timeline = []
    remaining_loans = [loan.copy() for loan in sorted_loans]
    
    while any(loan['balance'] > 0 for loan in remaining_loans):
        month += 1
        month_interest = 0
        month_principal = 0
        available_extra = extra_payment
        
        # Pay minimum on all loans
        for loan in remaining_loans:
            if loan['balance'] > 0:
                interest = loan['balance'] * (loan['rate'] / 100 / 12)
                principal = min(loan['min_payment'] - interest, loan['balance'])
                
                loan['balance'] -= principal
                month_interest += interest
                month_principal += principal
        
        # Apply extra payment to first loan with balance
        for loan in remaining_loans:
            if loan['balance'] > 0 and available_extra > 0:
                extra_principal = min(available_extra, loan['balance'])
                loan['balance'] -= extra_principal
                month_principal += extra_principal
                available_extra -= extra_principal
                break
        
        total_interest += month_interest
        
        timeline.append({
            'month': month,
            'interest_paid': round(month_interest, 2),
            'principal_paid': round(month_principal, 2),
            'remaining_balances': {loan['name']: round(loan['balance'], 2) for loan in remaining_loans}
        })
        
        # Safety break
        if month > 600:  # 50 years
            break
    
    return {
        'timeline': timeline,
        'months_to_payoff': month,
        'total_interest': round(total_interest, 2),
        'strategy': strategy
    }

def calculate_refinance_savings(current_loan, new_rate, new_term_months, refinance_costs=0):
    """
    Calculate savings from refinancing a loan.
    
    Args:
        current_loan: Dict with keys: balance, rate, remaining_months, monthly_payment
        new_rate: New interest rate (percentage)
        new_term_months: New loan term in months
        refinance_costs: Upfront costs of refinancing
    
    Returns:
        Dictionary with refinance analysis
    """
    # Current loan remaining payments
    current_total = current_loan['monthly_payment'] * current_loan['remaining_months']
    
    # Calculate current remaining interest
    current_schedule = calculate_amortization_schedule(
        current_loan['balance'],
        current_loan['rate'],
        current_loan['remaining_months']
    )
    current_interest = current_schedule['summary']['total_interest']
    
    # New loan calculations
    new_payment = calculate_monthly_payment(current_loan['balance'], new_rate, new_term_months)
    new_schedule = calculate_amortization_schedule(
        current_loan['balance'],
        new_rate,
        new_term_months
    )
    new_interest = new_schedule['summary']['total_interest']
    new_total = new_payment * new_term_months
    
    # Calculate savings
    interest_savings = current_interest - new_interest - refinance_costs
    monthly_payment_change = new_payment - current_loan['monthly_payment']
    total_cost_change = new_total + refinance_costs - current_total
    
    return {
        'current': {
            'monthly_payment': current_loan['monthly_payment'],
            'remaining_months': current_loan['remaining_months'],
            'total_interest': round(current_interest, 2),
            'total_cost': round(current_total, 2)
        },
        'refinanced': {
            'monthly_payment': round(new_payment, 2),
            'term_months': new_term_months,
            'total_interest': round(new_interest, 2),
            'total_cost': round(new_total + refinance_costs, 2),
            'refinance_costs': refinance_costs
        },
        'savings': {
            'interest_savings': round(interest_savings, 2),
            'monthly_payment_change': round(monthly_payment_change, 2),
            'total_cost_change': round(total_cost_change, 2),
            'break_even_months': round(refinance_costs / abs(monthly_payment_change), 0) if monthly_payment_change < 0 else None
        },
        'recommendation': 'refinance' if interest_savings > 0 else 'keep_current'
    }
