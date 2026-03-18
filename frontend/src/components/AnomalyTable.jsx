// src/components/AnomalyTable.jsx
import { AlertTriangle, CheckCircle } from 'lucide-react';
import './AnomalyTable.css';

export default function AnomalyTable({ anomalies }) {
  if (!anomalies?.length) {
    return (
      <div className="anomaly-empty">
        <CheckCircle size={32} className="anomaly-empty__icon" />
        <p>No anomalies detected — your spending looks normal! 🎉</p>
      </div>
    );
  }

  return (
    <div className="anomaly-table-wrap">
      <div className="table-scroll">
        <table className="anomaly-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Description</th>
              <th>Category</th>
              <th className="text-right">Amount</th>
              <th className="text-right">Score</th>
            </tr>
          </thead>
          <tbody>
            {anomalies.map((tx, i) => (
              <tr key={i}>
                <td className="date-cell">{tx.date}</td>
                <td className="desc-cell">
                  <span className="desc-text">{tx.description}</span>
                </td>
                <td>
                  <span className="cat-badge">{tx.category}</span>
                </td>
                <td className="text-right amount-cell">
                  ${parseFloat(tx.amount).toFixed(2)}
                </td>
                <td className="text-right">
                  <span className="score-badge">
                    <AlertTriangle size={11} />
                    {tx.anomaly_score?.toFixed(3)}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
