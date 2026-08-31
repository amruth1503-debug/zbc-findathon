import { useState } from 'react'
import './App.css'

function App() {
  const [selectedFiles, setSelectedFiles] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleFileChange = (e) => {
    // e.target.files contains the list of selected files
    setSelectedFiles(e.target.files)
    setResult(null)
  }

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!selectedFiles || selectedFiles.length === 0) {
      alert('Please select at least one image first!')
      return
    }

    const formData = new FormData()
    
    // Append each file to the 'files' form data field to match FastAPI backend
    for (let i = 0; i < selectedFiles.length; i++) {
      formData.append('files', selectedFiles[i])
    }

    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()
      if (response.ok) {
        setResult(data)
      } else {
        alert(data.detail || 'Error uploading images')
      }
    } catch (err) {
      console.error(err)
      alert('Failed to connect to the backend server.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: '40px', fontFamily: 'Arial, sans-serif', maxWidth: '600px', margin: '0 auto' }}>
      <h2>Image Duplicate Finder</h2>
      
      <form onSubmit={handleUpload} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
        {/* Added the 'multiple' attribute here */}
        <input type="file" accept="image/*" multiple onChange={handleFileChange} />
        <button type="submit" disabled={loading} style={{ padding: '10px 20px', cursor: 'pointer' }}>
          {loading ? 'Processing...' : 'Upload & Check Duplicates'}
        </button>
      </form>

      {result && (
        <div style={{ marginTop: '20px', padding: '15px', background: '#f4f4f4', borderRadius: '5px' }}>
          <h3>Results:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}

export default App