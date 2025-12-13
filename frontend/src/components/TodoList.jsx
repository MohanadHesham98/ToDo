// frontend/src/components/TodoList.jsx
import React, { useEffect, useState } from 'react'
import { fetchTodos, createTodo, updateTodo, deleteTodo } from '../services/api'
import { DateTime } from 'luxon'

export default function TodoList() {
  const [todos, setTodos] = useState([])
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [alarmTime, setAlarmTime] = useState('')
  const [editing, setEditing] = useState(null)

  useEffect(() => {
    load()
  }, [])

  async function load() {
    const data = await fetchTodos()
    setTodos(data || [])
  }

  // SAVE EXACT USER TIME (No conversion)
  async function handleAdd(e) {
    e.preventDefault()
    if (!title.trim()) return
    const payload = {
      title,
      description,
      done: false,
      alarm_time: alarmTime || null
    }
    const newTodo = await createTodo(payload)
    setTitle('')
    setDescription('')
    setAlarmTime('')
    setTodos(prev => [...prev, newTodo])
  }

  async function handleToggle(todo) {
    const updated = await updateTodo(todo.id, { ...todo, done: !todo.done })
    setTodos(prev => prev.map(t => (t.id === updated.id ? updated : t)))
  }

  async function handleDelete(id) {
    await deleteTodo(id)
    setTodos(prev => prev.filter(t => t.id !== id))
  }

  function startEdit(todo) {
    setEditing({ ...todo })
  }

  async function saveEdit() {
    const payload = {
      title: editing.title,
      description: editing.description,
      done: editing.done,
      alarm_time: editing.alarm_time || null
    }
    const updated = await updateTodo(editing.id, payload)
    setTodos(prev => prev.map(t => (t.id === updated.id ? updated : t)))
    setEditing(null)
  }

  return (
    <div>
      <form onSubmit={handleAdd} className="flex flex-col gap-2 mb-4">
        <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Title" className="border p-2 rounded" />
        <input value={description} onChange={e => setDescription(e.target.value)} placeholder="Description" className="border p-2 rounded" />

        {/* datetime-local saved as-is */}
        <input value={alarmTime} onChange={e => setAlarmTime(e.target.value)} type="datetime-local" className="border p-2 rounded" />

        <button className="px-4 py-2 bg-blue-600 text-white rounded">Add</button>
      </form>

      <ul className="space-y-2">
        {todos.map(todo => (
          <li key={todo.id} className="flex items-center justify-between border p-3 rounded">
            <div>
              <div className={'font-semibold ' + (todo.done ? 'line-through text-slate-400' : '')}>
                {todo.title}
              </div>
              {todo.description && <div className="text-sm text-slate-500">{todo.description}</div>}

              {/* Display time as Cairo */}
              {todo.alarm_time && (
                <div className="text-sm text-red-600">
                  Alarm: {
                    DateTime.fromISO(todo.alarm_time)
                      .setZone('Africa/Cairo')
                      .toLocaleString(DateTime.DATETIME_SHORT)
                  }
                </div>
              )}
            </div>

            <div className="flex items-center gap-2">
              <button onClick={() => handleToggle(todo)} className="px-2 py-1 border rounded">{todo.done ? 'Undo' : 'Done'}</button>
              <button onClick={() => startEdit(todo)} className="px-2 py-1 border rounded">Edit</button>
              <button onClick={() => handleDelete(todo.id)} className="px-2 py-1 border rounded">Delete</button>
            </div>
          </li>
        ))}
      </ul>

      {editing && (
        <div className="mt-4 border p-3 rounded">
          <h3 className="font-semibold mb-2">Edit</h3>
          <input className="w-full mb-2 border p-2 rounded" value={editing.title} onChange={e => setEditing({ ...editing, title: e.target.value })} />
          <textarea className="w-full mb-2 border p-2 rounded" value={editing.description || ''} onChange={e => setEditing({ ...editing, description: e.target.value })} />

          {/* show user time without conversion */}
          <input
            type="datetime-local"
            className="w-full mb-2 border p-2 rounded"
            value={editing.alarm_time || ''}
            onChange={e => setEditing({ ...editing, alarm_time: e.target.value })}
          />

          <div className="flex gap-2">
            <button onClick={saveEdit} className="px-3 py-1 bg-green-600 text-white rounded">Save</button>
            <button onClick={() => setEditing(null)} className="px-3 py-1 border rounded">Cancel</button>
          </div>
        </div>
      )}
    </div>
  )
}
