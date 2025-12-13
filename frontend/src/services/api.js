// frontend/src/services/api.js

// =================================
// Backend URLs for docker-compose ports
//const API_BASE_AUTH = 'http://localhost:8001'
//const API_BASE_TODO = 'http://localhost:8002'
//const API_BASE_ALARM = 'http://localhost:8003'
// ==================================

// ==================================
//Backend URLs for k8s
const API_BASE_AUTH = '/api/auth'
const API_BASE_TODO = '/api/todos'
const API_BASE_ALARM = '/api/alarms'
// ==================================

function getToken() {
  return localStorage.getItem('token')
}

function authHeaders() {
  const token = getToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

// =======================
// AUTH
// =======================
export async function register({ email, password }) {
  const res = await fetch(`${API_BASE_AUTH}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  })
  return res.json()
}

export async function login({ email, password }) {
  // <-- تعديل هنا: JSON بدل form-urlencoded
  const res = await fetch(`${API_BASE_AUTH}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  })
  const data = await res.json()
  if (data.access_token) {
    localStorage.setItem('token', data.access_token)
  }
  return data
}

export async function logout() {
  localStorage.removeItem('token')
}

export async function getCurrentUser() {
  const res = await fetch(`${API_BASE_AUTH}/me`, {
    headers: { ...authHeaders() }
  })
  return res.json()
}

// =======================
// TODO SERVICE
// =======================
export async function fetchTodos() {
  const res = await fetch(`${API_BASE_TODO}/todos`, {
    headers: { ...authHeaders() }
  })
  return res.json()
}

export async function createTodo(payload) {
  const res = await fetch(`${API_BASE_TODO}/todos`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(payload)
  })
  return res.json()
}

export async function updateTodo(id, payload) {
  const res = await fetch(`${API_BASE_TODO}/todos/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(payload)
  })
  return res.json()
}

export async function deleteTodo(id) {
  const res = await fetch(`${API_BASE_TODO}/todos/${id}`, {
    method: 'DELETE',
    headers: { ...authHeaders() }
  })
  return res.json()
}

// =======================
// ALARM SERVICE (Optional)
// =======================
export async function fetchAlarms() {
  const res = await fetch(`${API_BASE_ALARM}/alarms`, {
    headers: { ...authHeaders() }
  })
  return res.json()
}
