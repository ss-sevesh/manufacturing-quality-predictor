import {
  ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  BarChart, Bar, LineChart, Line,
} from 'recharts';
import KpiCard from '../components/ui/KpiCard';
import LoadingSkeleton from '../components/ui/LoadingSkeleton';
import { useModelInfo } from '../hooks/usePredictions';

// Mock data — replaced by real endpoint data when available
const scatterData = Array.from({ length: 80 }, (_, i) => {
  const actual = 30 + Math.random() * 60;
  return { actual, predicted: actual + (Math.random() - 0.5) * 12 };
});

const shapData = [
  { feature: 'tool_wear', importance: 0.28 },
  { feature: 'vibration', importance: 0.22 },
  { feature: 'temperature', importance: 0.17 },
  { feature: 'surface_roughness', importance: 0.14 },
  { feature: 'pressure', importance: 0.09 },
];

const lossData = Array.from({ length: 40 }, (_, i) => ({
  epoch: i + 1,
  train: 0.08 * Math.exp(-0.06 * i) + 0.003,
  val: 0.09 * Math.exp(-0.05 * i) + 0.005 + Math.random() * 0.002,
}));

export default function Performance() {
  const { data: modelInfo, isLoading } = useModelInfo();

  if (isLoading) return <LoadingSkeleton rows={6} className="p-8" />;

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">Model Performance</h2>
        <p className="text-gray-500 dark:text-gray-400">Evaluation metrics and diagnostics</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KpiCard title="RMSE" value="3.42" subtitle="Root Mean Squared Error" />
        <KpiCard title="MAE" value="2.61" subtitle="Mean Absolute Error" />
        <KpiCard title="R-squared" value="0.94" subtitle="Coefficient of Determination" />
        <KpiCard title="Training Time" value="47s" subtitle="Last training run" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Actual vs Predicted */}
        <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm">
          <h3 className="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-4">Actual vs Predicted</h3>
          <ResponsiveContainer width="100%" height={280}>
            <ScatterChart>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.2} />
              <XAxis dataKey="actual" name="Actual" type="number" domain={[20, 100]} tick={{ fontSize: 12 }} />
              <YAxis dataKey="predicted" name="Predicted" type="number" domain={[20, 100]} tick={{ fontSize: 12 }} />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} />
              <Scatter data={scatterData} fill="#3b82f6" opacity={0.6} />
            </ScatterChart>
          </ResponsiveContainer>
        </div>

        {/* SHAP Feature Importance */}
        <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm">
          <h3 className="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-4">Top Feature Importances (SHAP)</h3>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={shapData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.2} />
              <XAxis type="number" tick={{ fontSize: 12 }} />
              <YAxis dataKey="feature" type="category" width={120} tick={{ fontSize: 12 }} />
              <Tooltip />
              <Bar dataKey="importance" fill="#8b5cf6" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Training Loss */}
      <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm">
        <h3 className="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-4">Training Loss Curve</h3>
        <ResponsiveContainer width="100%" height={280}>
          <LineChart data={lossData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.2} />
            <XAxis dataKey="epoch" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip />
            <Line type="monotone" dataKey="train" stroke="#3b82f6" strokeWidth={2} dot={false} name="Train Loss" />
            <Line type="monotone" dataKey="val" stroke="#f59e0b" strokeWidth={2} dot={false} name="Val Loss" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
