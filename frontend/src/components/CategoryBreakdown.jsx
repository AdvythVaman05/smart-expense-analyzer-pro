// src/components/CategoryBreakdown.jsx
// Horizontal progress-bar breakdown of spending per category
import { CAT_COLORS } from '../pages/Dashboard.jsx';
import './CategoryBreakdown.css';

export default function CategoryBreakdown({ data, total }) {
  const entries = Object.entries(data); // already sorted desc by categorizer

  return (
    <div className="cat-breakdown">
      {entries.map(([category, amount], i) => {
        const pct = total > 0 ? (amount / total) * 100 : 0;
        const color = CAT_COLORS[category] ?? '#6c63ff';

        return (
          <div
            key={category}
            className="cat-breakdown__row fade-up"
            style={{ animationDelay: `${i * 50}ms` }}
          >
            <div className="cat-breakdown__meta">
              <div className="cat-breakdown__dot" style={{ background: color }} />
              <span className="cat-breakdown__name">{category}</span>
              <span className="cat-breakdown__pct">{pct.toFixed(1)}%</span>
              <span className="cat-breakdown__amount">${amount.toFixed(2)}</span>
            </div>
            <div className="cat-breakdown__bar-bg">
              <div
                className="cat-breakdown__bar-fill"
                style={{
                  width: `${pct}%`,
                  background: `linear-gradient(90deg, ${color}cc, ${color}66)`,
                  animationDelay: `${150 + i * 50}ms`,
                }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
}
