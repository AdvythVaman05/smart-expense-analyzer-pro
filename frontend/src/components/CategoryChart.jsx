// src/components/CategoryChart.jsx
import {
  PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const COLORS = [
  '#6c63ff', '#9f7aea', '#63b3ff', '#48bb78', '#f59e0b',
  '#ef4444', '#ed64a6', '#38bdf8',
];

const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null;
  const { name, value } = payload[0];
  return (
    <div style={{
      background: 'rgba(15,20,40,0.95)',
      border: '1px solid rgba(255,255,255,0.1)',
      borderRadius: 10,
      padding: '10px 14px',
      fontSize: '0.82rem',
    }}>
      <p style={{ color: '#f0f0ff', fontWeight: 700 }}>{name}</p>
      <p style={{ color: '#9090b8' }}>${value.toFixed(2)}</p>
    </div>
  );
};

export default function CategoryChart({ data }) {
  const chartData = Object.entries(data).map(([name, value]) => ({ name, value }));

  return (
    <ResponsiveContainer width="100%" height={280}>
      <PieChart>
        <Pie
          data={chartData}
          cx="50%"
          cy="50%"
          innerRadius={65}
          outerRadius={105}
          paddingAngle={3}
          dataKey="value"
        >
          {chartData.map((_, i) => (
            <Cell key={i} fill={COLORS[i % COLORS.length]} stroke="none" />
          ))}
        </Pie>
        <Tooltip content={<CustomTooltip />} />
        <Legend
          formatter={(val) => (
            <span style={{ color: '#9090b8', fontSize: '0.76rem' }}>{val}</span>
          )}
        />
      </PieChart>
    </ResponsiveContainer>
  );
}
