import { createContext, useContext, useState, useEffect } from 'react'
import { auth } from '../services/api'

const AuthContext = createContext({})

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    checkAuth()
  }, [])

  const checkAuth = async () => {
    const token = localStorage.getItem('token')
    
    if (token) {
      try {
        const response = await auth.getCurrentUser()
        setUser(response.data)
      } catch (error) {
        localStorage.removeItem('token')
        localStorage.removeItem('refreshToken')
      }
    }
    
    setLoading(false)
  }

  const login = async (credentials) => {
    const response = await auth.login(credentials)
    const { access_token, refresh_token, user: userData } = response.data
    
    localStorage.setItem('token', access_token)
    localStorage.setItem('refreshToken', refresh_token)
    setUser(userData)
    
    return response.data
  }

  const register = async (credentials) => {
    const response = await auth.register(credentials)
    const { access_token, refresh_token, user: userData } = response.data
    
    localStorage.setItem('token', access_token)
    localStorage.setItem('refreshToken', refresh_token)
    setUser(userData)
    
    return response.data
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    setUser(null)
  }

  const value = {
    user,
    login,
    register,
    logout,
    isAuthenticated: !!user,
    loading,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  return useContext(AuthContext)
}
