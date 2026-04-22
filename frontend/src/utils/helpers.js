import { format } from 'date-fns';

export function getScoreColor(score) {
  if (score > 75) return 'green';
  if (score >= 50) return 'amber';
  return 'red';
}

export function getScoreClasses(score) {
  const color = getScoreColor(score);
  const map = {
    green: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300',
    amber: 'bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300',
    red: 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300',
  };
  return map[color];
}

export function getScoreBorder(score) {
  const color = getScoreColor(score);
  const map = {
    green: 'border-emerald-500',
    amber: 'border-amber-500',
    red: 'border-red-500',
  };
  return map[color];
}

export function formatTimestamp(ts) {
  return format(new Date(ts), 'MMM d, yyyy HH:mm:ss');
}

export function downloadCsv(rows, filename = 'predictions.csv') {
  if (!rows.length) return;
  const headers = Object.keys(rows[0]);
  const csv = [
    headers.join(','),
    ...rows.map((r) => headers.map((h) => r[h] ?? '').join(',')),
  ].join('\n');
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export function loadHistory() {
  try {
    return JSON.parse(localStorage.getItem('prediction_history') || '[]');
  } catch {
    return [];
  }
}

export function saveHistory(history) {
  localStorage.setItem('prediction_history', JSON.stringify(history));
}
