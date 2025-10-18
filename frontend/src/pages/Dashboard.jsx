import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { loans, accounts, calculations } from '../services/api'
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { useAuth } from '../hooks/useAuth'

export default function Dashboard() {
  const [loansData, setLoansData] = useState([])
  const [accountsData, setAccountsData] = useState([])
  const [loading, setLoading] = useState(true)
  const [dti, setDti] = useState(null)
  const { logout, user } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [loansResponse, accountsResponse] = await Promise.all([
        loans.getAll(),
        accounts.getAll(),
      ])
      
      setLoansData(loansResponse.data.loans || [])
      setAccountsData(accountsResponse.data.accounts || [])
      setLoading(false)
    } catch (error) {
      console.error('Failed to load data:', error)
      setLoading(false)
    }
  }

  const totalLoanBalance = loansData.reduce((sum, loan) => sum + (loan.remaining_balance || loan.principal), 0)
  const totalMonthlyPayment = loansData.reduce((sum, loan) => sum + (loan.monthly_payment || 0), 0)
  const totalAccounts = accountsData.reduce((sum, account) => sum + (account.balance || 0), 0)

  const COLORS = ['#0ea5e9', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981']

  const loanDistribution = loansData.map((loan, index) => ({
    name: loan.loan_name,
    value: loan.remaining_balance || loan.principal,
    color: COLORS[index % COLORS.length],
  }))

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">LoanLens Dashboard</h1>
          <div className="flex items-center gap-4">
            <span className="text-gray-600">{user?.email}</span>
            <button onClick={handleLogout} className="btn-secondary">
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <button
            onClick={() => navigate('/scenarios')}
            className="card hover:shadow-lg transition-shadow text-left"
          >
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Create Scenario</h3>
            <p className="text-gray-600">Build and analyze financial scenarios</p>
          </button>
          <button className="card hover:shadow-lg transition-shadow text-left">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Add Loan</h3>
            <p className="text-gray-600">Track a new loan or debt</p>
          </button>
          <button className="card hover:shadow-lg transition-shadow text-left">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Add Account</h3>
            <p className="text-gray-600">Link a bank or credit account</p>
          </button>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="card bg-gradient-to-br from-primary-500 to-primary-600 text-white">
            <h3 className="text-sm font-medium opacity-90 mb-1">Total Loan Balance</h3>
            <p className="text-3xl font-bold">${totalLoanBalance.toLocaleString()}</p>
          </div>
          <div className="card bg-gradient-to-br from-purple-500 to-purple-600 text-white">
            <h3 className="text-sm font-medium opacity-90 mb-1">Monthly Payments</h3>
            <p className="text-3xl font-bold">${totalMonthlyPayment.toLocaleString()}</p>
          </div>
          <div className="card bg-gradient-to-br from-green-500 to-green-600 text-white">
            <h3 className="text-sm font-medium opacity-90 mb-1">Total Assets</h3>
            <p className="text-3xl font-bold">${totalAccounts.toLocaleString()}</p>
          </div>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Loan Distribution */}
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Loan Distribution</h2>
            {loanDistribution.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={loanDistribution}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {loanDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="text-center text-gray-500 py-12">
                No loans to display. Add your first loan to see distribution.
              </div>
            )}
          </div>

          {/* Loans List */}
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Your Loans</h2>
            <div className="space-y-3">
              {loansData.length > 0 ? (
                loansData.map((loan) => (
                  <div key={loan.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h3 className="font-semibold text-gray-900">{loan.loan_name}</h3>
                        <p className="text-sm text-gray-600 capitalize">{loan.loan_type}</p>
                      </div>
                      <span className="text-sm font-medium text-primary-600">{loan.interest_rate}%</span>
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      <div>
                        <span className="text-gray-600">Balance:</span>{' '}
                        <span className="font-medium">${(loan.remaining_balance || loan.principal).toLocaleString()}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Payment:</span>{' '}
                        <span className="font-medium">${loan.monthly_payment?.toLocaleString()}</span>
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center text-gray-500 py-8">
                  No loans yet. Add your first loan to get started!
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Accounts List */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Accounts</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {accountsData.length > 0 ? (
              accountsData.map((account) => (
                <div key={account.id} className="border border-gray-200 rounded-lg p-4">
                  <h3 className="font-semibold text-gray-900 mb-1">{account.account_name}</h3>
                  <p className="text-sm text-gray-600 capitalize mb-2">{account.account_type}</p>
                  <p className="text-2xl font-bold text-primary-600">
                    ${account.balance.toLocaleString()}
                  </p>
                </div>
              ))
            ) : (
              <div className="col-span-full text-center text-gray-500 py-8">
                No accounts yet. Add an account to track your finances!
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
