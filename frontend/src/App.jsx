// frontend/src/App.jsx
import React, { useEffect, useState } from 'react'
import TodoList from './components/TodoList'
import AuthForm from './components/AuthForm'
import { getCurrentUser, logout } from './services/api'

export default function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  async function loadUser() {
    try {
      const res = await getCurrentUser()
      if (res && res.id) setUser(res)
    } catch (err) {
      setUser(null)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadUser()
  }, [])

  if (loading) return <div className="p-6">Loading...</div>

  if (!user) {
    return <AuthForm onAuth={loadUser} />
  }

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="max-w-3xl mx-auto bg-white shadow-md rounded-lg p-6">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-2xl">ToDo ({user.email})</h1>
          <div>
            <button onClick={() => { logout(); setUser(null) }} className="px-3 py-1 border rounded">Logout</button>
          </div>
        </div>
        <TodoList />
      </div>
    </div>
  )
}

