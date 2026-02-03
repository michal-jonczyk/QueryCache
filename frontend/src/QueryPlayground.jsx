import { useState } from 'react'

export default function QueryPlayground() {
  const [sql, setSql] = useState('SELECT * FROM products LIMIT 10')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const executeQuery = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/query?sql=${encodeURIComponent(sql)}`)
      const data = await res.json()
      setResult(data)
    } catch (err) {
      console.error(err)
      setResult({ error: 'Failed to execute query' })
    }
    setLoading(false)
  }

 const clearCache = async () => {
  console.log('API URL:', import.meta.env.VITE_API_URL)

  try {
    await fetch(`${import.meta.env.VITE_API_URL}/cache`, { method: 'DELETE' })
    setResult(null)
    alert('Cache cleared!')
  } catch (err) {
    console.error('Error:', err)
    alert('Error: ' + err.message)
  }
}

  return (
    <div className="bg-slate-800 p-6 rounded-lg mb-8">
      <h2 className="text-2xl font-bold text-cyan-400 mb-4">Query Playground</h2>

      <textarea
        value={sql}
        onChange={(e) => setSql(e.target.value)}
        className="w-full bg-slate-900 text-white p-4 rounded font-mono text-sm mb-4 border border-slate-700 focus:border-cyan-500 focus:outline-none"
        rows={5}
        placeholder="Enter your SQL query..."
      />

      <div className="flex gap-4 mb-6">
        <button
          onClick={executeQuery}
          disabled={loading}
          className="bg-cyan-500 hover:bg-cyan-600 disabled:bg-slate-600 px-6 py-2 rounded font-bold transition"
        >
          {loading ? 'Executing...' : 'Execute Query'}
        </button>

        <button
          onClick={clearCache}
          className="bg-red-500 hover:bg-red-600 px-6 py-2 rounded font-bold transition"
        >
          Clear Cache
        </button>
      </div>

      {result && !result.error && (
        <div className="mt-6">
          <div className="flex gap-4 mb-4">
            <div className={`px-4 py-2 rounded font-bold ${
              result.source === 'cache' ? 'bg-green-600' : 'bg-orange-600'
            }`}>
              Source: {result.source?.toUpperCase()}
            </div>
            <div className="px-4 py-2 bg-slate-700 rounded font-bold">
              Time: {result.execution_time_ms}ms
            </div>
            <div className="px-4 py-2 bg-slate-700 rounded">
              Rows: {result.result?.length || 0}
            </div>
          </div>

          {result.result && result.result.length > 0 && (
            <div className="overflow-x-auto bg-slate-900 rounded border border-slate-700">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-slate-800 border-b border-slate-700">
                    {Object.keys(result.result[0]).map(key => (
                      <th key={key} className="px-4 py-3 text-left text-cyan-400 font-semibold">
                        {key}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {result.result.map((row, idx) => (
                    <tr key={idx} className="border-b border-slate-800 hover:bg-slate-800 transition">
                      {Object.values(row).map((val, i) => (
                        <td key={i} className="px-4 py-3 text-gray-300">
                          {typeof val === 'number' ? val.toLocaleString() : val}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {result?.error && (
        <div className="mt-6 bg-red-900 border border-red-700 text-red-200 p-4 rounded">
          <strong>Error:</strong> {result.error}
        </div>
      )}
    </div>
  )
}