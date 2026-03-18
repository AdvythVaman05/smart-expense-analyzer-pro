// src/pages/Dashboard.jsx  — Phase 4 upgrade
import { useState, useCallback } from 'react';
import {
  DollarSign, TrendingUp, AlertTriangle, Layers,
  UploadCloud, ShieldCheck, Sparkles, BarChart2,
  Zap, Clock
} from 'lucide-react';
import toast from 'react-hot-toast';
import api from '../services/api';
import Navbar from '../components/Navbar';
import StatCard from '../components/StatCard';
import UploadZone from '../components/UploadZone';
import CategoryChart from '../components/CategoryChart';
import MonthlyChart from '../components/MonthlyChart';
import AnomalyTable from '../components/AnomalyTable';
import CategoryBreakdown from '../components/CategoryBreakdown';
import './Dashboard.css';

// ── Category icon color map ──────────────────────────────────────────
export const CAT_COLORS = {
  'Food & Dining':    '#f59e0b',
  'Transport':        '#63b3ff',
  'Shopping':         '#ec4899',
  'Entertainment':    '#a78bfa',
  'Health & Wellness':'#34d399',
  'Utilities & Bills':'#fb923c',
  'Travel':           '#38bdf8',
  'Education':        '#818cf8',
  'Other':            '#6b7280',
};

export default function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [animKey, setAnimKey] = useState(0); // force re-animation on new upload

  const handleUpload = useCallback(async (file) => {
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await api.post('/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(res.data);
      setAnimKey(k => k + 1);
      toast.success('✨ Analysis complete!', { duration: 3500 });
    } catch (err) {
      const msg = err.response?.data?.error || 'Upload failed. Please try again.';
      toast.error(msg);
    } finally {
      setLoading(false);
    }
  }, []);

  // Derived stats
  const totalSpend   = result ? Object.values(result.category_summary).reduce((a,b)=>a+b,0) : 0;
  const avgTx        = result ? totalSpend / result.transactions.length : 0;
  const topCategory  = result ? Object.entries(result.category_summary)[0] : null;
  const anomalyCount = result?.anomalies?.length ?? 0;
  const txCount      = result?.transactions?.length ?? 0;

  return (
    <div className="dashboard-layout">
      <Navbar />

      <main className="dashboard-main container">

        {/* ── Page Header ── */}
        <header className="dash-header fade-up">
          <div>
            <h1 className="dash-title">Expense Dashboard</h1>
            <p className="dash-sub">AI-powered spending analysis — upload a CSV to begin</p>
          </div>
          {result && (
            <div className="dash-header-badge fade-up">
              <ShieldCheck size={14} /> Analysis ready
            </div>
          )}
        </header>

        {/* ── Upload Zone ── */}
        <section className="dash-section fade-up" style={{ animationDelay: '60ms' }}>
          <UploadZone onUpload={handleUpload} loading={loading} />
        </section>

        {/* ── Hero — shown before first upload ── */}
        {!result && !loading && <HeroFeatureGrid />}

        {/* ── Alert Banner ── */}
        {result?.alert && (
          <div className={`alert-banner fade-up ${anomalyCount > 0 ? 'alert-banner--warn' : 'alert-banner--ok'}`}>
            {anomalyCount > 0 ? <AlertTriangle size={16} /> : <ShieldCheck size={16} />}
            {result.alert}
          </div>
        )}

        {/* ────────── RESULTS ────────── */}
        {result && (
          <div key={animKey}>

            {/* ── Stat Cards ── */}
            <div className="stats-grid">
              <StatCard
                icon={<DollarSign size={20} />}
                label="Total Spend"
                value={`$${totalSpend.toFixed(2)}`}
                sub={`${txCount} transactions`}
                color="var(--accent)"
                delay={0}
              />
              <StatCard
                icon={<Layers size={20} />}
                label="Top Category"
                value={topCategory?.[0] ?? '—'}
                sub={topCategory ? `$${topCategory[1].toFixed(2)}` : ''}
                color={CAT_COLORS[topCategory?.[0]] ?? 'var(--accent)'}
                delay={80}
              />
              <StatCard
                icon={<TrendingUp size={20} />}
                label="Avg Transaction"
                value={`$${avgTx.toFixed(2)}`}
                sub={`across ${Object.keys(result.monthly_summary).length} months`}
                color="#34d399"
                delay={160}
              />
              <StatCard
                icon={<AlertTriangle size={20} />}
                label="Anomalies"
                value={anomalyCount}
                sub={anomalyCount > 0 ? 'requires review' : 'all clear'}
                color={anomalyCount > 0 ? 'var(--danger)' : 'var(--success)'}
                delay={240}
              />
            </div>

            {/* ── Charts Row ── */}
            <div className="charts-grid fade-up" style={{ animationDelay: '120ms' }}>
              <div className="glass-card chart-card">
                <h2 className="chart-title"><BarChart2 size={15} /> Spend by Category</h2>
                <CategoryChart data={result.category_summary} />
              </div>
              <div className="glass-card chart-card">
                <h2 className="chart-title"><TrendingUp size={15} /> Monthly Breakdown</h2>
                <MonthlyChart data={result.monthly_summary} />
              </div>
            </div>

            {/* ── Category Breakdown Progress Bars ── */}
            <div className="glass-card section-card fade-up" style={{ animationDelay: '180ms' }}>
              <div className="section-header">
                <h2 className="chart-title"><Layers size={15} /> Category Breakdown</h2>
                <span className="badge badge-success">{txCount} transactions</span>
              </div>
              <CategoryBreakdown data={result.category_summary} total={totalSpend} />
            </div>

            {/* ── Anomalies ── */}
            <div className="glass-card section-card fade-up" style={{ animationDelay: '240ms' }}>
              <div className="section-header">
                <h2 className="chart-title">
                  <AlertTriangle size={15} style={{ color: 'var(--warning)' }} />
                  Anomalous Transactions
                </h2>
                <span className={`badge ${anomalyCount > 0 ? 'badge-danger' : 'badge-success'}`}>
                  {anomalyCount > 0 ? `${anomalyCount} flagged` : 'All clear'}
                </span>
              </div>
              <AnomalyTable anomalies={result.anomalies} />
            </div>

            {/* ── Full Transactions ── */}
            <div className="glass-card section-card fade-up" style={{ animationDelay: '280ms' }}>
              <div className="section-header">
                <h2 className="chart-title"><Clock size={15} /> All Transactions</h2>
                <span className="badge badge-success">{txCount} records</span>
              </div>
              <TransactionTable transactions={result.transactions} />
            </div>

          </div>
        )}
      </main>
    </div>
  );
}

/* ── Sub-components ──────────────────────────────────────────────── */

function HeroFeatureGrid() {
  const features = [
    { icon: <UploadCloud size={22} />, title: 'Smart CSV Import', desc: 'Works with any bank export — flexible column detection' },
    { icon: <Layers size={22} />, title: '8 Auto-Categories', desc: 'Food, Transport, Shopping, Travel, and more — instant' },
    { icon: <Zap size={22} />, title: 'ML Anomaly Detection', desc: 'Isolation Forest flags unusual transactions automatically' },
    { icon: <BarChart2 size={22} />, title: 'Visual Insights', desc: 'Pie charts, monthly bar charts, and breakdown bars' },
    { icon: <ShieldCheck size={22} />, title: 'Secure & Private', desc: 'JWT auth — your data stays in your account only' },
    { icon: <Sparkles size={22} />, title: 'Instant Results', desc: 'Full analysis in under a second — no waiting' },
  ];

  return (
    <div className="hero-grid fade-up" style={{ animationDelay: '120ms' }}>
      <p className="hero-label">What you get after uploading</p>
      <div className="hero-features">
        {features.map((f, i) => (
          <div
            key={i}
            className="hero-feature-card glass-card fade-up"
            style={{ animationDelay: `${160 + i * 55}ms` }}
          >
            <div className="hero-feature-icon">{f.icon}</div>
            <div>
              <p className="hero-feature-title">{f.title}</p>
              <p className="hero-feature-desc">{f.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function TransactionTable({ transactions }) {
  return (
    <div className="table-scroll">
      <table className="anomaly-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Description</th>
            <th>Category</th>
            <th className="text-right">Amount</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((tx, i) => (
            <tr key={i} className={tx.anomaly ? 'tx-row--anomaly' : ''}>
              <td className="date-cell">{tx.date}</td>
              <td className="desc-cell"><span className="desc-text">{tx.description}</span></td>
              <td>
                <span
                  className="cat-badge"
                  style={{
                    background: `${CAT_COLORS[tx.category] ?? '#6c63ff'}22`,
                    color: CAT_COLORS[tx.category] ?? 'var(--accent-light)',
                  }}
                >
                  {tx.category}
                </span>
              </td>
              <td
                className="text-right"
                style={{
                  fontVariantNumeric: 'tabular-nums',
                  fontWeight: 700,
                  color: tx.anomaly ? 'var(--danger)' : 'var(--text-primary)',
                }}
              >
                ${parseFloat(tx.amount).toFixed(2)}
              </td>
              <td>
                {tx.anomaly
                  ? <span className="badge badge-danger"><AlertTriangle size={10} /> Anomaly</span>
                  : <span className="badge badge-success">Normal</span>}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
