import { useState, useRef, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { Layout } from '../components/layout/Layout'
import { Card } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Upload, FileText, CheckCircle, XCircle, AlertTriangle, ArrowLeft } from 'lucide-react'
import api from '../lib/api'

interface ImportResult {
  imported: number
  skipped: number
  errors: string[]
}

export function ImportPage() {
  const navigate = useNavigate()
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [dragOver, setDragOver] = useState(false)
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<ImportResult | null>(null)
  const [uploadError, setUploadError] = useState<string | null>(null)

  const handleFile = useCallback((f: File) => {
    setUploadError(null)
    setResult(null)
    if (!f.name.toLowerCase().endsWith('.csv')) {
      setUploadError('Please select a .csv file')
      return
    }
    setFile(f)
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setDragOver(false)
    const f = e.dataTransfer.files[0]
    if (f) handleFile(f)
  }, [handleFile])

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setDragOver(true)
  }
  const handleDragLeave = () => setDragOver(false)

  const handleUpload = async () => {
    if (!file) return
    setLoading(true)
    setUploadError(null)
    setResult(null)

    try {
      const formData = new FormData()
      formData.append('file', file)
      const res = await api.post('/import/csv', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setResult(res.data)
    } catch (err: any) {
      const msg = err.response?.data?.detail || err.message || 'Upload failed'
      setUploadError(msg)
    } finally {
      setLoading(false)
    }
  }

  const reset = () => {
    setFile(null)
    setResult(null)
    setUploadError(null)
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  return (
    <Layout>
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <button onClick={() => navigate('/portfolio')} className="text-gray-400 hover:text-gray-200 p-1 rounded">
            <ArrowLeft size={20} />
          </button>
          <div>
            <h1 className="text-2xl font-bold text-gray-100">Import CSV</h1>
            <p className="text-sm text-gray-500 mt-1">Bulk-import holdings from a CSV file</p>
          </div>
        </div>
      </div>

      <Card className="max-w-xl mx-auto">
        {!file && !result && (
          <div
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onClick={() => fileInputRef.current?.click()}
            className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-colors ${
              dragOver
                ? 'border-blue-400 bg-blue-500/10'
                : 'border-gray-600 hover:border-gray-500 bg-gray-800/50'
            }`}
          >
            <Upload size={40} className="mx-auto mb-3 text-gray-400" />
            <p className="text-gray-300 font-medium mb-1">
              Drop your CSV file here, or click to browse
            </p>
            <p className="text-xs text-gray-500">
              Format: <code className="text-blue-400">ticker,shares,avg_cost,currency</code> (currency optional)
            </p>
            <input
              ref={fileInputRef}
              type="file"
              accept=".csv"
              className="hidden"
              onChange={(e) => {
                const f = e.target.files?.[0]
                if (f) handleFile(f)
              }}
            />
          </div>
        )}

        {file && !result && (
          <div className="p-6">
            <div className="flex items-center gap-3 mb-4 p-3 bg-gray-800 rounded-lg">
              <FileText size={24} className="text-blue-400" />
              <div className="flex-1 min-w-0">
                <p className="text-gray-200 font-medium truncate">{file.name}</p>
                <p className="text-xs text-gray-500">{(file.size / 1024).toFixed(1)} KB</p>
              </div>
              <button onClick={reset} className="text-gray-500 hover:text-gray-300 text-sm">Change</button>
            </div>

            {uploadError && (
              <div className="flex items-start gap-2 p-3 mb-4 bg-red-900/40 border border-red-800 rounded-lg text-red-300 text-sm">
                <XCircle size={16} className="mt-0.5 shrink-0" />
                <span>{uploadError}</span>
              </div>
            )}

            <Button onClick={handleUpload} disabled={loading} className="w-full">
              {loading ? 'Importing...' : 'Upload & Import'}
            </Button>
          </div>
        )}

        {result && (
          <div className="p-6 space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-green-900/30 border border-green-800 rounded-lg text-center">
                <CheckCircle size={24} className="mx-auto mb-1 text-green-400" />
                <p className="text-2xl font-bold text-green-400">{result.imported}</p>
                <p className="text-xs text-gray-400">Imported</p>
              </div>
              <div className="p-4 bg-yellow-900/30 border border-yellow-800 rounded-lg text-center">
                <AlertTriangle size={24} className="mx-auto mb-1 text-yellow-400" />
                <p className="text-2xl font-bold text-yellow-400">{result.skipped}</p>
                <p className="text-xs text-gray-400">Skipped</p>
              </div>
            </div>

            {result.errors.length > 0 && (
              <div>
                <p className="text-sm text-red-400 font-medium mb-2">Errors ({result.errors.length})</p>
                <div className="max-h-40 overflow-y-auto text-xs text-red-300 bg-red-900/20 border border-red-800/50 rounded-lg p-3 space-y-1">
                  {result.errors.map((err, i) => (
                    <p key={i}>{err}</p>
                  ))}
                </div>
              </div>
            )}

            <div className="flex gap-3">
              <Button onClick={() => navigate('/portfolio')} variant="default" className="flex-1">
                View Portfolio
              </Button>
              <Button onClick={reset} variant="outline" className="flex-1">
                Import Another
              </Button>
            </div>
          </div>
        )}
      </Card>

      <div className="max-w-xl mx-auto mt-6">
        <Card>
          <h3 className="text-sm font-medium text-gray-300 mb-2">CSV Format</h3>
          <div className="bg-gray-900 rounded-lg p-3 text-xs font-mono text-gray-400 overflow-x-auto">
            <p className="text-green-400">ticker,shares,avg_cost,currency</p>
            <p>AAPL,10,150.50,USD</p>
            <p>GOOGL,5,2750.00,USD</p>
            <p>TSLA,20,245.30,USD</p>
            <p className="text-gray-600 mt-2"># currency column is optional (defaults to USD)</p>
            <p className="text-gray-600"># Duplicate tickers are merged via weighted-average cost</p>
          </div>
        </Card>
      </div>
    </Layout>
  )
}