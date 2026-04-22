import { getScoreClasses } from '../../utils/helpers';

export default function ScoreBadge({ score }) {
  return (
    <span className={`inline-flex items-center rounded-full px-3 py-1 text-sm font-semibold ${getScoreClasses(score)}`}>
      {score.toFixed(1)}
    </span>
  );
}
