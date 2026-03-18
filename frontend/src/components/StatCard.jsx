// src/components/StatCard.jsx
import './StatCard.css';

export default function StatCard({ icon, label, value, sub, color = 'var(--accent)', delay = 0 }) {
  return (
    <div
      className="stat-card glass-card fade-up"
      style={{ animationDelay: `${delay}ms`, '--card-color': color }}
    >
      <div className="stat-card__icon">
        {icon}
      </div>
      <div className="stat-card__body">
        <span className="stat-card__label">{label}</span>
        <span className="stat-card__value">{value}</span>
        {sub && <span className="stat-card__sub">{sub}</span>}
      </div>
      <div className="stat-card__glow" />
    </div>
  );
}
