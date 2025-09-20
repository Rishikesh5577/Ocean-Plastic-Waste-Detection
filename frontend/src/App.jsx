import React, { useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'

export default function App() {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [detections, setDetections] = useState([]) // plastic detections
  const [plasticCount, setPlasticCount] = useState(0)
  const [annotated, setAnnotated] = useState(null)
  const [error, setError] = useState('')

  const onUpload = async () => {
    if (!file) return
    setLoading(true)
    setError('')
    setDetections([])
    setPlasticCount(0)
    setAnnotated(null)

    const form = new FormData()
    form.append('file', file)

    try {
      const res = await fetch(`${API_BASE}/predict`, {
        method: 'POST',
        body: form,
      })
      if (!res.ok) {
        throw new Error(`Request failed: ${res.status}`)
      }
      const data = await res.json()
      setDetections(data.plastic_detections || [])
      setPlasticCount(data.plastic_count || 0)
      setAnnotated(`data:image/jpeg;base64,${data.annotated_image_b64}`)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <header className="header">
        <h1>🌊 Ocean Plastics Waste Detection</h1>
        <p>React + FastAPI</p>
      </header>

      <section className="card">
        <h3>📤 Upload Image</h3>
        <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <button disabled={!file || loading} onClick={onUpload}>
          {loading ? 'Detecting…' : 'Run Detection'}
        </button>
        {error && <p className="error">{error}</p>}
      </section>

      {annotated && (
        <section className="card">
          <h3>🎯 Annotated Result</h3>
          <img src={annotated} alt="annotated" style={{ maxWidth: '100%' }} />
        </section>
      )}

      {typeof plasticCount === 'number' && (
        <section className="card">
          <h3>🥤 Plastic Count: {plasticCount}</h3>
        </section>
      )}

    </div>
  )
}
