
import React from 'react';
import '../global.css';
import './dashboard.css';
import Sidebar from './components/Sidebar';

import {
  ResponsiveContainer,
  LineChart,   Line,
  BarChart,    Bar,
  PieChart,    Pie, Cell,
  CartesianGrid, XAxis, YAxis, Tooltip,
} from 'recharts';

/* ─────────────────────────  MOCK-ДАННЫЕ  ───────────────────────── */

const portfolioValue = [
  { date: '2025-06-01', value: 1235.50 },
  { date: '2025-06-02', value: 1248.12 },
  { date: '2025-06-03', value: 1254.77 },
  { date: '2025-06-04', value: 1246.90 },
];

const dailyPL = [
  { date: '2025-06-01', pl:  12.62 },
  { date: '2025-06-02', pl:  18.44 },
  { date: '2025-06-03', pl:   6.65 },
  { date: '2025-06-04', pl:  -7.87 },
];

const allocation = [
  { portfolio_id: 3, name: 'Gold',         value: 750.0, share_percent: 60.0 },
  { portfolio_id: 7, name: 'Index',        value: 335.0, share_percent: 26.8 },
  { portfolio_id: 9, name: 'Conservative', value: 165.5, share_percent: 13.2 },
];

const PIE_COLORS = ['#6366f1', '#f59e0b', '#10b981'];

/* ─────────────────────────  КОМПОНЕНТ  ─────────────────────────── */

export default function DashboardPage() {
  return (
    <div className="dashboard">{/* 1. flex-контейнер */}
      <Sidebar />

      <main className="main-content">
        {/* ——— верхняя панель ——— */}
        <div className="top-bar">
          <h1 className="title">Dashboard</h1>
          <div className="date-filters">
            <input type="date" className="date-input" />
            <input type="date" className="date-input" />
          </div>
        </div>

        {/* ——— summary-карточки ) ——— */}
        <div className="summary">
          {[
            { label: 'Save Products',  value: '178+', type: 'save' },
            { label: 'Stock Products', value: '20+',  type: 'stock' },
            { label: 'Sales Products', value: '190+', type: 'sales' },
            { label: 'Job Application',value: '12+',  type: 'jobs' },
          ].map(c => (
            <div key={c.label} className="card">
              <div className={`card-icon ${c.type}`} />
              <div className="card-info">
                <div className="card-label">{c.label}</div>
                <div className="card-value">{c.value}</div>
              </div>
            </div>
          ))}
        </div>

        {/* ——— блок графиков ——— */}
        <div className="charts">
          {/* 1. Portfolio Value vs Time  */}
          <section className="chart large">
            <h2 className="chart-title">Portfolio Value vs Time</h2>
            <ResponsiveContainer width="100%" height={240}>
              <LineChart data={portfolioValue}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="value"
                  stroke="#6366f1"
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </section>

          {/* 2. Daily P/L bar-chart */}
          <section className="chart small">
            <h2 className="chart-title">Daily P/L</h2>
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={dailyPL}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="pl" fill="#10b981" />
              </BarChart>
            </ResponsiveContainer>
          </section>

          {/* 3. Allocation Pie */}
          <section className="chart small">
            <h2 className="chart-title">Allocation</h2>
            <ResponsiveContainer width="100%" height={240}>
              <PieChart>
                <Tooltip />
                <Pie
                  data={allocation}
                  dataKey="share_percent"
                  nameKey="name"
                  cx="50%" cy="50%"
                  outerRadius={80}
                  label={({ name, share_percent }) =>
                    `${name} (${share_percent}%)`
                  }
                >
                  {allocation.map((_, idx) => (
                    <Cell key={idx} fill={PIE_COLORS[idx % PIE_COLORS.length]} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </section>
        </div>

  
        <div className="bottom-panels">
          <section className="orders">
            <h2 className="panel-title">Recent Orders</h2>
            <table className="orders-table">
              <thead>
                <tr>
                  <th>Tracking no</th><th>Product Name</th><th>Price</th>
                  <th>Total Order</th><th>Total Amount</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>#98760</td><td>Product 1</td><td>$99</td>
                  <td>42</td><td>$4,158</td>
                </tr>
              </tbody>
            </table>
          </section>
        </div>
      </main>
    </div>
  );
}
