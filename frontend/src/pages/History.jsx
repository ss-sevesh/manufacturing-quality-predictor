import { useState, useMemo } from 'react';
import { useHistory } from '../hooks/usePredictions';
import ScoreBadge from '../components/ui/ScoreBadge';
import LoadingSkeleton from '../components/ui/LoadingSkeleton';
import { formatTimestamp, downloadCsv } from '../utils/helpers';
import { Download, ChevronLeft, ChevronRight } from 'lucide-react';

const PAGE_SIZE = 10;

export default function History() {
  const { data: history = [], isLoading } = useHistory();
  const [page, setPage] = useState(0);
  const [range, setRange] = useState([0, 100]);

  const filtered = useMemo(
    () => history.filter((h) => h.quality_score >= range[0] && h.quality_score <= range[1]),
    [history, range]
  );

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const pageData = filtered.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);

  if (isLoading) return <LoadingSkeleton rows={8} className="p-8" />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Prediction History</h2>
          <p className="text-gray-500 dark:text-gray-400">{filtered.length} predictions</p>
        </div>
        <button
          onClick={() => downloadCsv(filtered)}
          disabled={!filtered.length}
          className="inline-flex items-center gap-2 rounded-lg border border-gray-300 dark:border-gray-700 px-4 py-2 text-sm font-medium hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-50 transition-colors"
        >
          <Download size={16} /> Export CSV
        </button>
      </div>

      {/* Score filter */}
      <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-4 shadow-sm flex items-center gap-6 flex-wrap">
        <label className="text-sm font-medium text-gray-600 dark:text-gray-300">Score Range</label>
        <div className="flex items-center gap-3">
          <input
            type="range" min="0" max="100" value={range[0]}
            onChange={(e) => { setRange([+e.target.value, range[1]]); setPage(0); }}
            className="accent-blue-600"
          />
          <span className="text-sm font-mono w-8 text-center">{range[0]}</span>
          <span className="text-gray-400">-</span>
          <input
            type="range" min="0" max="100" value={range[1]}
            onChange={(e) => { setRange([range[0], +e.target.value]); setPage(0); }}
            className="accent-blue-600"
          />
          <span className="text-sm font-mono w-8 text-center">{range[1]}</span>
        </div>
      </div>

      {filtered.length === 0 ? (
        <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-12 text-center text-gray-400 dark:text-gray-500">
          No predictions match the filter
        </div>
      ) : (
        <>
          <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200 dark:border-gray-700">
                  {['Time', 'Temp', 'Pressure', 'Humidity', 'Speed', 'Score', 'Status'].map((h) => (
                    <th key={h} className="text-left px-4 py-3 font-medium text-gray-500 dark:text-gray-400">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {pageData.map((h, i) => (
                  <tr key={i} className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                    <td className="px-4 py-3 text-gray-600 dark:text-gray-300 whitespace-nowrap">{formatTimestamp(h.timestamp)}</td>
                    <td className="px-4 py-3">{h.temperature}</td>
                    <td className="px-4 py-3">{h.pressure}</td>
                    <td className="px-4 py-3">{h.humidity}</td>
                    <td className="px-4 py-3">{h.speed}</td>
                    <td className="px-4 py-3"><ScoreBadge score={h.quality_score} /></td>
                    <td className="px-4 py-3 capitalize">{h.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="flex items-center justify-between">
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Page {page + 1} of {totalPages}
            </p>
            <div className="flex gap-2">
              <button
                onClick={() => setPage((p) => Math.max(0, p - 1))}
                disabled={page === 0}
                className="rounded-lg border border-gray-300 dark:border-gray-700 p-2 hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-50 transition-colors"
              >
                <ChevronLeft size={16} />
              </button>
              <button
                onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
                disabled={page >= totalPages - 1}
                className="rounded-lg border border-gray-300 dark:border-gray-700 p-2 hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-50 transition-colors"
              >
                <ChevronRight size={16} />
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
