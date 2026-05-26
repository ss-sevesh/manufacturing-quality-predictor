import { RadialBarChart, RadialBar, ResponsiveContainer } from 'recharts';
import KpiCard from '../components/ui/KpiCard';
import ScoreBadge from '../components/ui/ScoreBadge';
import LoadingSkeleton from '../components/ui/LoadingSkeleton';
import { useHistory, useHealth } from '../hooks/usePredictions';
import { formatTimestamp } from '../utils/helpers';

export default function Dashboard() {
  const { data: history = [], isLoading } = useHistory();
  const { data: health } = useHealth();

  const total = history.length;
  const avgScore = total ? history.reduce((s, h) => s + h.quality_score, 0) / total : 0;
  const defects = total ? history.filter((h) => h.status === 'fail').length : 0;
  const defectRate = total ? ((defects / total) * 100).toFixed(1) : '0.0';

  const gaugeData = [{ name: 'Quality', value: avgScore, fill: avgScore > 75 ? '#16a34a' : avgScore >= 50 ? '#d97706' : '#dc2626' }];

  if (isLoading) return <LoadingSkeleton rows={6} className="p-8" />;

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">Dashboard</h2>
        <p className="text-gray-500 dark:text-gray-400">Manufacturing quality overview</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <KpiCard title="Avg Quality Score" value={avgScore.toFixed(1)} subtitle="Across all predictions" />
        <KpiCard title="Total Predictions" value={total} subtitle="Lifetime count" />
        <KpiCard title="Defect Rate" value={`${defectRate}%`} subtitle="Status: fail" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Quality Gauge */}
        <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm">
          <h3 className="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-4">Quality Gauge</h3>
          {total === 0 ? (
            <div className="flex items-center justify-center h-48 text-gray-400 dark:text-gray-500">No predictions yet</div>
          ) : (
            <ResponsiveContainer width="100%" height={220}>
              <RadialBarChart cx="50%" cy="50%" innerRadius="60%" outerRadius="90%" startAngle={180} endAngle={0} data={gaugeData}>
                <RadialBar dataKey="value" cornerRadius={8} background={{ fill: '#e5e7eb' }} max={100} />
                <text x="50%" y="50%" textAnchor="middle" dominantBaseline="middle" className="fill-gray-900 dark:fill-gray-100 text-3xl font-bold">
                  {avgScore.toFixed(1)}
                </text>
              </RadialBarChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* Recent Predictions */}
        <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm">
          <h3 className="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-4">Recent Predictions</h3>
          {total === 0 ? (
            <div className="flex items-center justify-center h-48 text-gray-400 dark:text-gray-500">No predictions yet</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-200 dark:border-gray-700">
                    <th className="text-left py-2 font-medium text-gray-500 dark:text-gray-400">Time</th>
                    <th className="text-left py-2 font-medium text-gray-500 dark:text-gray-400">Score</th>
                    <th className="text-left py-2 font-medium text-gray-500 dark:text-gray-400">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {history.slice(0, 5).map((h, i) => (
                    <tr key={i} className="border-b border-gray-100 dark:border-gray-800">
                      <td className="py-2.5 text-gray-600 dark:text-gray-300">{formatTimestamp(h.timestamp)}</td>
                      <td className="py-2.5"><ScoreBadge score={h.quality_score} /></td>
                      <td className="py-2.5 capitalize text-gray-600 dark:text-gray-300">{h.status}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
