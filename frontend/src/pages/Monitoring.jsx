import { useState, useEffect, useRef } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { useHealth, useHistory } from '../hooks/usePredictions';
import { Wifi, WifiOff, AlertTriangle } from 'lucide-react';

export default function Monitoring() {
  const { data: health, isError: healthError } = useHealth();
  const { data: history = [] } = useHistory();
  const [trendData, setTrendData] = useState([]);
  const indexRef = useRef(0);

  const isOnline = health && !healthError;

  // Simulate quality trend polling every 5s
  useEffect(() => {
    const interval = setInterval(() => {
      setTrendData((prev) => {
        const now = new Date().toLocaleTimeString();
        const score = history.length > 0
          ? history[indexRef.current % history.length]?.quality_score ?? 70 + (Math.random() - 0.5) * 20
          : 70 + (Math.random() - 0.5) * 20;
        indexRef.current += 1;
        const next = [...prev, { time: now, score: +score.toFixed(1) }];
        return next.slice(-30); // keep last 30 points
      });
    }, 5000);
    return () => clearInterval(interval);
  }, [history]);

  const QUALITY_THRESHOLD = 70;
  const alerts = history.filter((h) => h.status === 'fail').slice(0, 10);

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Monitoring</h2>
          <p className="text-gray-500 dark:text-gray-400">Real-time quality monitoring and alerts</p>
        </div>

        {/* API Status Badge */}
        <div
          className={`inline-flex items-center gap-2 rounded-full px-4 py-2 text-sm font-semibold ${
            isOnline
              ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300'
              : 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300'
          }`}
        >
          {isOnline ? <Wifi size={16} /> : <WifiOff size={16} />}
          {isOnline ? 'API Online' : 'API Offline'}
        </div>
      </div>

      {/* Quality Trend */}
      <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm">
        <h3 className="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-4">Quality Score Trend (live)</h3>
        {trendData.length < 2 ? (
          <div className="flex items-center justify-center h-64 text-gray-400 dark:text-gray-500">
            Collecting data points... (updates every 5s)
          </div>
        ) : (
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.2} />
              <XAxis dataKey="time" tick={{ fontSize: 11 }} />
              <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="score"
                stroke="#3b82f6"
                strokeWidth={2}
                dot={{ r: 3 }}
                activeDot={{ r: 5 }}
                name="Quality Score"
              />
              {/* Threshold line */}
              <Line
                type="monotone"
                dataKey={() => QUALITY_THRESHOLD}
                stroke="#dc2626"
                strokeWidth={1}
                strokeDasharray="5 5"
                dot={false}
                name="Alert Threshold"
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>

      {/* Alerts Panel */}
      <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm">
        <h3 className="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-4 flex items-center gap-2">
          <AlertTriangle size={16} className="text-amber-500" /> Quality Alerts
        </h3>
        {alerts.length === 0 ? (
          <p className="text-gray-400 dark:text-gray-500">No alerts -- all predictions above threshold</p>
        ) : (
          <div className="space-y-2">
            {alerts.map((a, i) => (
              <div
                key={i}
                className="flex items-center justify-between rounded-lg border border-red-200 dark:border-red-900/50 bg-red-50 dark:bg-red-900/20 px-4 py-3"
              >
                <div className="flex items-center gap-3">
                  <AlertTriangle size={16} className="text-red-500" />
                  <span className="text-sm text-red-700 dark:text-red-300">
                    Quality score <strong>{a.quality_score.toFixed(1)}</strong> -- below threshold
                  </span>
                </div>
                <span className="text-xs text-red-500 dark:text-red-400">
                  {new Date(a.timestamp).toLocaleTimeString()}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
