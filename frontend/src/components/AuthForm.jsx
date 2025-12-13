// frontend/src/components/AuthForm.jsx
import React, { useState } from 'react'
import { register, login } from '../services/api'

export default function AuthForm({ onAuth }) {
  const [isRegister, setIsRegister] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  async function submit(e) {
    e.preventDefault()
    setError('')
    try {
      if (isRegister) {
        const regRes = await register({ email, password })
        if (regRes.detail) {
          setError(regRes.detail)
          return
        }
        // بعد التسجيل مباشرة نسجل الدخول
      }
      const res = await login({ email, password })
      if (res.access_token) {
        onAuth()
      } else {
        setError(res.detail || 'Auth failed')
      }
    } catch (err) {
      setError('Request failed')
    }
  }

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded shadow">
      <h2 className="text-xl mb-4">{isRegister ? 'Register' : 'Login'}</h2>
      <form onSubmit={submit} className="flex flex-col gap-2">
        <input value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" className="border p-2 rounded" />
        <input value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" type="password" className="border p-2 rounded" />
        {error && <div className="text-red-500">{error}</div>}
        <button className="px-4 py-2 bg-blue-600 text-white rounded">{isRegister ? 'Register' : 'Login'}</button>
      </form>
      <div className="mt-3">
        <button onClick={() => setIsRegister(!isRegister)} className="text-sm text-blue-600">
          {isRegister ? 'Have an account? Login' : "Don't have an account? Register"}
        </button>
      </div>
    </div>
  )
}
