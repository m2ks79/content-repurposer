import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'
import './App.css'

export default function App() {
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [addWatermark, setAddWatermark] = useState(false)

  const onDrop = useCallback(acceptedFiles => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0])
      setError(null)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'video/*': ['.mp4', '.mov', '.webm', '.avi', '.mkv'] },
    maxSize: 500 * 1024 * 1024  // 500MB
  })

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!file) {
      setError('Please select a video file')
      return
    }

    setUploading(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('video', file)
      formData.append('watermark', addWatermark)

      const response = await axios.post('/api/repurpose', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      setResults(response.data.formats)
      console.log('Repurposing complete:', response.data)
    } catch (err) {
      console.error('Upload error:', err)
      setError(err.response?.data?.error || 'Failed to repurpose video')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🎬 Content Repurposer</h1>
        <p>Convert your video to all platforms in seconds</p>
      </header>

      <main className="container">
        <div className="upload-section">
          <form onSubmit={handleUpload}>
            <div
              {...getRootProps()}
              className={`dropzone ${isDragActive ? 'active' : ''} ${file ? 'has-file' : ''}`}
            >
              <input {...getInputProps()} />
              {file ? (
                <div className="file-info">
                  <p>📄 {file.name}</p>
                  <p className="file-size">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                </div>
              ) : (
                <div className="dropzone-content">
                  <p className="big">Drag video here or click to select</p>
                  <p className="small">Supports: MP4, MOV, WebM, AVI, MKV (up to 500MB)</p>
                </div>
              )}
            </div>

            <div className="options">
              <label>
                <input
                  type="checkbox"
                  checked={addWatermark}
                  onChange={(e) => setAddWatermark(e.target.checked)}
                />
                Add watermark
              </label>
            </div>

            {error && <div className="error">{error}</div>}

            <button
              type="submit"
              disabled={!file || uploading}
              className="btn-primary"
            >
              {uploading ? 'Processing...' : 'Repurpose Video'}
            </button>
          </form>
        </div>

        {results && (
          <div className="results">
            <h2>Your Videos Are Ready! 🎉</h2>
            <div className="formats-grid">
              {Object.entries(results).map(([platform, data]) => (
                <div key={platform} className="format-card">
                  <h3>{platform.charAt(0).toUpperCase() + platform.slice(1)}</h3>
                  <p className="dimensions">{data.dimensions}</p>
                  {data.status === 'done' ? (
                    <>
                      <p className="status ok">✓ Ready</p>
                      <a href={`/api/download/${data.filepath}`} className="btn-download">
                        Download
                      </a>
                    </>
                  ) : (
                    <p className="status error">✗ {data.error}</p>
                  )}
                </div>
              ))}
            </div>

            <button className="btn-secondary" onClick={() => {
              setFile(null)
              setResults(null)
            }}>
              Repurpose Another Video
            </button>
          </div>
        )}
      </main>

      <footer className="footer">
        <p>Phase 1: Basic repurposing | Phase 2 coming soon: Smart captions + scheduling</p>
      </footer>
    </div>
  )
}
