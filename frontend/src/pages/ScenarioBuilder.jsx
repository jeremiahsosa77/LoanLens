import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { loans, calculations, scenarios } from '../services/api'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function ScenarioBuilder() {
  const [loansList, setLoansList] = useState([])
  const [selectedLoans, setSelectedLoans] = useState([])
  const [calculationType, setCalculationType] = useState('amortization')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  
  // Loan input for new calculation
  const [loanInput, setLoanInput] = useState({
    principal: '',
    annual_rate: '',
    term_months: '',
    extra_payment: '0',
  })

  const navigate = useNavigate()

  useEffect(() => {
    loadLoans()
  }, [])

  const loadLoans = async () => {
    try {
      const response = await loans.getAll()
      setLoansList(response.data.loans || [])
    } catch (error) {
      console.error('Failed to load loans:', error)
    }
  }

  const handleCalculate = async () => {
    setError('')
    setLoading(true)

    try {
      let response
      
      switch (calculationType) {
        case 'amortization':
          response = await calculations.amortization({
            principal: parseFloat(loanInput.principal),
            annual_rate: parseFloat(loanInput.annual_rate),
            term_months: parseInt(loanInput.term_months),
            extra_payment: parseFloat(loanInput.extra_payment || 0),
          })
          setResult(response.data)
          break

        case 'payoff':
          if (selectedLoans.length === 0) {
            setError('Please select at least one loan')
            setLoading(false)
            return
          }
          
          const loansForPayoff = selectedLoans.map(id => {
            const loan = loansList.find(l => l.id === id)
            return {
              name: loan.loan_name,
              balance: loan.remaining_balance || loan.principal,
              rate: loan.interest_rate,
              min_payment: loan.monthly_payment,
            }
          })
          
          response = await calculations.payoff({
            loans: loansForPayoff,
            strategy: 'avalanche',
            extra_payment: parseFloat(loanInput.extra_payment || 0),
          })
          setResult(response.data)
          break

        case 'monthly_payment':
          response = await calculations.monthlyPayment({
            principal: parseFloat(loanInput.principal),
            annual_rate: parseFloat(loanInput.annual_rate),
            term_months: parseInt(loanInput.term_months),
          })
          setResult(response.data)
          break

        default:
          setError('Invalid calculation type')
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Calculation failed')
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e) => {
    setLoanInput({
      ...loanInput,
      [e.target.name]: e.target.value,
    })
  }

  const toggleLoanSelection = (loanId) => {
    setSelectedLoans(prev =>
      prev.includes(loanId)
        ? prev.filter(id => id !== loanId)
        : [...prev, loanId]
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Scenario Builder</h1>
          <button onClick={() => navigate('/dashboard')} className="btn-secondary">
            Back to Dashboard
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Input Section */}
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Configure Scenario</h2>

            {/* Calculation Type */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Calculation Type
              </label>
              <select
                value={calculationType}
                onChange={(e) => setCalculationType(e.target.value)}
                className="input-field"
              >
                <option value="amortization">Amortization Schedule</option>
                <option value="payoff">Payoff Plan</option>
                <option value="monthly_payment">Monthly Payment Calculator</option>
              </select>
            </div>

            {/* Loan Selection for Payoff */}
            {calculationType === 'payoff' && (
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Select Loans
                </label>
                <div className="space-y-2 max-h-48 overflow-y-auto border border-gray-200 rounded-lg p-3">
                  {loansList.length > 0 ? (
                    loansList.map(loan => (
                      <label key={loan.id} className="flex items-center gap-2 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={selectedLoans.includes(loan.id)}
                          onChange={() => toggleLoanSelection(loan.id)}
                          className="rounded text-primary-600"
                        />
                        <span className="text-sm">{loan.loan_name} - ${(loan.remaining_balance || loan.principal).toLocaleString()}</span>
                      </label>
                    ))
                  ) : (
                    <p className="text-sm text-gray-500">No loans available. Add loans first.</p>
                  )}
                </div>
              </div>
            )}

            {/* Loan Parameters */}
            {(calculationType === 'amortization' || calculationType === 'monthly_payment') && (
              <>
                <div className="mb-4">
                  <label htmlFor="principal" className="block text-sm font-medium text-gray-700 mb-1">
                    Loan Amount ($)
                  </label>
                  <input
                    id="principal"
                    name="principal"
                    type="number"
                    value={loanInput.principal}
                    onChange={handleInputChange}
                    className="input-field"
                    placeholder="100000"
                    required
                  />
                </div>

                <div className="mb-4">
                  <label htmlFor="annual_rate" className="block text-sm font-medium text-gray-700 mb-1">
                    Interest Rate (%)
                  </label>
                  <input
                    id="annual_rate"
                    name="annual_rate"
                    type="number"
                    step="0.01"
                    value={loanInput.annual_rate}
                    onChange={handleInputChange}
                    className="input-field"
                    placeholder="5.5"
                    required
                  />
                </div>

                <div className="mb-4">
                  <label htmlFor="term_months" className="block text-sm font-medium text-gray-700 mb-1">
                    Loan Term (months)
                  </label>
                  <input
                    id="term_months"
                    name="term_months"
                    type="number"
                    value={loanInput.term_months}
                    onChange={handleInputChange}
                    className="input-field"
                    placeholder="360"
                    required
                  />
                </div>
              </>
            )}

            {/* Extra Payment */}
            {(calculationType === 'amortization' || calculationType === 'payoff') && (
              <div className="mb-4">
                <label htmlFor="extra_payment" className="block text-sm font-medium text-gray-700 mb-1">
                  Extra Monthly Payment ($)
                </label>
                <input
                  id="extra_payment"
                  name="extra_payment"
                  type="number"
                  value={loanInput.extra_payment}
                  onChange={handleInputChange}
                  className="input-field"
                  placeholder="0"
                />
              </div>
            )}

            {error && (
              <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            <button
              onClick={handleCalculate}
              disabled={loading}
              className="btn-primary w-full"
            >
              {loading ? 'Calculating...' : 'Calculate'}
            </button>
          </div>

          {/* Results Section */}
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Results</h2>
            
            {!result ? (
              <div className="text-center text-gray-500 py-12">
                Configure and run a calculation to see results
              </div>
            ) : (
              <div>
                {calculationType === 'amortization' && result.summary && (
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-primary-50 rounded-lg p-4">
                        <p className="text-sm text-gray-600">Monthly Payment</p>
                        <p className="text-2xl font-bold text-primary-600">
                          ${result.summary.monthly_payment.toLocaleString()}
                        </p>
                      </div>
                      <div className="bg-purple-50 rounded-lg p-4">
                        <p className="text-sm text-gray-600">Total Interest</p>
                        <p className="text-2xl font-bold text-purple-600">
                          ${result.summary.total_interest.toLocaleString()}
                        </p>
                      </div>
                      <div className="bg-green-50 rounded-lg p-4">
                        <p className="text-sm text-gray-600">Total Amount</p>
                        <p className="text-2xl font-bold text-green-600">
                          ${result.summary.total_amount.toLocaleString()}
                        </p>
                      </div>
                      <div className="bg-orange-50 rounded-lg p-4">
                        <p className="text-sm text-gray-600">Payoff Date</p>
                        <p className="text-lg font-bold text-orange-600">
                          {result.summary.payoff_date}
                        </p>
                      </div>
                    </div>

                    {/* Amortization Chart */}
                    <div className="mt-6">
                      <h3 className="font-semibold mb-2">Payment Breakdown</h3>
                      <ResponsiveContainer width="100%" height={250}>
                        <LineChart data={result.schedule.slice(0, 60)}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="payment_number" />
                          <YAxis />
                          <Tooltip />
                          <Legend />
                          <Line type="monotone" dataKey="principal" stroke="#0ea5e9" name="Principal" />
                          <Line type="monotone" dataKey="interest" stroke="#ec4899" name="Interest" />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                )}

                {calculationType === 'payoff' && (
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-primary-50 rounded-lg p-4">
                        <p className="text-sm text-gray-600">Months to Payoff</p>
                        <p className="text-2xl font-bold text-primary-600">
                          {result.months_to_payoff}
                        </p>
                      </div>
                      <div className="bg-purple-50 rounded-lg p-4">
                        <p className="text-sm text-gray-600">Total Interest</p>
                        <p className="text-2xl font-bold text-purple-600">
                          ${result.total_interest.toLocaleString()}
                        </p>
                      </div>
                    </div>
                    <div className="bg-gray-50 rounded-lg p-4">
                      <p className="text-sm text-gray-600 mb-2">Strategy</p>
                      <p className="text-lg font-semibold capitalize">{result.strategy}</p>
                    </div>
                  </div>
                )}

                {calculationType === 'monthly_payment' && (
                  <div className="bg-primary-50 rounded-lg p-6 text-center">
                    <p className="text-sm text-gray-600 mb-2">Monthly Payment</p>
                    <p className="text-4xl font-bold text-primary-600">
                      ${result.monthly_payment.toLocaleString()}
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
