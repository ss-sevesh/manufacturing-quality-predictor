import {
  ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line, ReferenceLine,
} from 'recharts';
import KpiCard from '../components/ui/KpiCard';
import LoadingSkeleton from '../components/ui/LoadingSkeleton';
import { useMetrics } from '../hooks/usePredictions';

export default function Performance() {
  const { data: metrics, isLoading, isError } = useMetrics();

  if (isLoading) return <LoadingSkeleton rows={6} className="p-8" />;

  if (isError || !metrics) {
    return (
      <div className="space-y-8">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Model Performance</h2>
          <p className="text-gray-500 dark:text-gray-400">Evaluation metrics and diagnostics</p>
        </div>
        <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-16 text-center shadow-sm">
          <p className="text-lg font-medium text-gray-500 dark:text-gray-400">No metrics available</p>
          <p className="mt-2 text-sm text-gray-400 dark:text-gray-500">
            Run <code className="bg-gray-100 dark:bg-gray-800 px-1 rounded">python -m src.models.train</code> to generate metrics.
          </p>
        </div>
      </div>
    );
  }

  const lossData = (metrics.loss_history?.train ?? []).map((v, i) => ({
    epoch: i + 1,
    train: +v.toFixed(6),
    val: +(metrics.loss_history.val[i] ?? 0).toFixed(6),
  }));

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">Model Performance</h2>
        <p className="text-gray-500 dark:text-gray-400">
          Evaluation metrics and diagnostics &mdash; trained {new Date(metrics.generated_at).toLocaleString()}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KpiCard title="RMSE" value={metrics.rmse.toFixed(3)} subtitle="Root Mean Squared Error (0–100 scale)" />
        <KpiCard title="MAE" value={metrics.mae.toFixed(3)} subtitle="Mean Absolute Error (0–100 scale)" />
        <KpiCard title="R²" value={metrics.r2.toFixed(4)} subtitle="Coefficient of Determination" />
        <KpiCard title="MAPE" value={`${metrics.mape.toFixed(2)}%`} subtitle="Mean Absolute Percentage Error" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Actual vs Predicted */}
        <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm">
          <h3 className="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-1">Actual vs Predicted</h3>
          <p className="text-xs text-gray-400 dark:text-gray-500 mb-4">{metrics.scatter_sample.length} test samples</p>
          <ResponsiveContainer width="100%" height={280}>
            <ScatterChart>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.2} />
              <XAxis dataKey="actual" name="Actual" type="number" domain={[0, 100]} tick={{ fontSize: 12 }} label={{ value: 'Actual', position: 'insideBottom', offset: -2, fontSize: 12 }} />
              <YAxis dataKey="predicted" name="Predicted" type="number" domain={[0, 100]} tick={{ fontSize: 12 }} />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} formatter={(v) => v.toFixed(1)} />
              <ReferenceLine segment={[{ x: 0, y: 0 }, { x: 100, y: 100 }]} stroke="#dc2626" strokeDasharray="4 4" strokeWidth={1.5} />
              <Scatter data={metrics.scatter_sample} fill="#3b82f6" opacity={0.5} />
            </ScatterChart>
          </ResponsiveContainer>
        </div>

        {/* Training Loss */}
        <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm">
          <h3 className="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-1">Training Loss Curve</h3>
          <p className="text-xs text-gray-400 dark:text-gray-500 mb-4">
            {metrics.training_epochs > 0 ? `${metrics.training_epochs} epochs` : 'MSE on normalised [0, 1] scale'}
          </p>
          {lossData.length < 2 ? (
            <div className="flex items-center justify-center h-64 text-gray-400 dark:text-gray-500 text-sm">
              Loss history not available — retrain to capture it.
            </div>
          ) : (
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={lossData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.2} />
                <XAxis dataKey="epoch" tick={{ fontSize: 12 }} label={{ value: 'Epoch', position: 'insideBottom', offset: -2, fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip formatter={(v) => v.toFixed(6)} />
                <Line type="monotone" dataKey="train" stroke="#3b82f6" strokeWidth={2} dot={false} name="Train Loss" />
                <Line type="monotone" dataKey="val" stroke="#f59e0b" strokeWidth={2} dot={false} name="Val Loss" />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 shadow-sm text-sm text-gray-500 dark:text-gray-400">
        Dataset: {metrics.train_samples.toLocaleString()} train / {metrics.test_samples.toLocaleString()} test &nbsp;·&nbsp;
        Architecture: MLP 15 → 128 → 64 → 32 → 1 &nbsp;·&nbsp;
        Metrics computed on 0–100 scale
      </div>
    </div>
  );
}
