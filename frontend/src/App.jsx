import { useState, useEffect } from 'react'

function App() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('http://localhost:8000/stats')
      .then(res => res.json())
      .then(data => {
        setStats(data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching stats:', err)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900 text-white flex items-center justify-center">
        <p className="text-xl">Loading...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <h1 className="text-4xl font-bold text-cyan-400 mb-8">
        QueryCache Dashboard
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-slate-800 p-6 rounded-lg">
          <p className="text-gray-400 text-sm mb-2">Total Queries</p>
          <p className="text-3xl font-bold text-cyan-400">{stats?.total_queries || 0}</p>
        </div>

        <div className="bg-slate-800 p-6 rounded-lg">
          <p className="text-gray-400 text-sm mb-2">Total Hits</p>
          <p className="text-3xl font-bold text-green-400">{stats?.total_hits || 0}</p>
        </div>

        <div className="bg-slate-800 p-6 rounded-lg">
          <p className="text-gray-400 text-sm mb-2">Cache Size</p>
          <p className="text-3xl font-bold text-purple-400">{stats?.cache_size || '0 KB'}</p>
        </div>
      </div>

      <div className="bg-slate-800 p-6 rounded-lg">
        <h2 className="text-2xl font-bold text-cyan-400 mb-4">Top Queries</h2>

        {stats?.top_queries?.length > 0 ? (
          <div className="space-y-3">
            {stats.top_queries.map((query, idx) => (
              <div key={idx} className="bg-slate-700 p-4 rounded">
                <p className="text-white font-mono text-sm mb-2">{query.query}</p>
                <div className="flex gap-4 text-sm text-gray-400">
                  <span>Hits: {query.hits}</span>
                  <span>Cached: {new Date(query.cached_at).toLocaleString()}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-400">No queries cached yet</p>
        )}
      </div>
    </div>
  )
}

export default App