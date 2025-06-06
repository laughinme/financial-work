
import React, { useEffect, useState } from 'react';
import dayjs from 'dayjs';

import '../global.css';
import './dashboard.css';

import Sidebar from './components/Sidebar';
import SparklineChart from './components/charts/SparklineChart';
import { FiBarChart2 } from 'react-icons/fi';

import {
  ResponsiveContainer,
  LineChart,
  Line,
  BarChart,
  Bar,
  Cell,
  PieChart,
  Pie,
  Tooltip,
  CartesianGrid,
  XAxis,
  YAxis,
} from 'recharts';

import {
  fetchSummary,
  fetchCharts,
  fetchPortfolios,
  fetchTx,
} from '../mock/api';

/* ─── УТИЛИТЫ ───────────────────────────────────────────────── */
const fmtMoney = (n) => '$' + (+n).toLocaleString();
const colored = (n) => (+n >= 0 ? 'text-green-600' : 'text-red-600');
const Skel = ({ h = 24 }) => (
  <div
    className="animate-pulse bg-gray-200/60 rounded-lg"
    style={{ height: h }}
  />
);

/* ─── SparklineIcon с hover-tooltip ──────────────────────────── */
function SparklineIcon({ data }) {
  const series = Array.isArray(data) ? data.slice(0, 30) : [];

  return (
    <span className="spark-container">
      <FiBarChart2 size={18} className="spark-icon" />
      <div className="spark-tooltip">
        <div className="spark-chart-wrapper">
          <SparklineChart data={series} />
        </div>
      </div>
    </span>
  );
}

/* ─── КОМПОНЕНТ DashboardPage ─────────────────────────────────── */
export default function DashboardPage() {
  const [sum, setSum] = useState(null);
  const [charts, setCharts] = useState(null);
  const [ports, setPorts] = useState(null);
  const [tx, setTx] = useState(null);

  useEffect(() => {
    fetchSummary().then(setSum);
  }, []);

  useEffect(() => {
    fetchCharts().then(setCharts);
  }, []);

  useEffect(() => {
    fetchPortfolios().then(setPorts);
  }, []);

  useEffect(() => {
    fetchTx().then(setTx);
  }, []);

  return (
    <div className="dashboard">
      <Sidebar />

      <main className="main-content">
        {/* HEADER */}
        <header className="dash-header">
          <div className="logo-circle" />
          {sum ? (
            <>
              <span>
                Total Equity:&nbsp;<b>{fmtMoney(sum.total_equity)}</b>
              </span>
              <span>
                P/L Today:&nbsp;
                <b className={colored(sum.today_pl)}>
                  {'+' + fmtMoney(sum.today_pl)}
                </b>
              </span>
              <button className="btn-deposit">Deposit</button>
            </>
          ) : (
            <Skel h={32} />
          )}
        </header>

        {/* KPI GRID */}
        <section className="kpi-grid">
          {sum ? (
            <>
              <div className="kpi-card">
                <p>Total P/L</p>
                <h3 className={colored(sum.total_pnl)}>
                  {'+' + fmtMoney(sum.total_pnl)}
                </h3>
              </div>
              <div className="kpi-card">
                <p>Today P/L</p>
                <h3 className={colored(sum.today_pl)}>
                  {'+' + fmtMoney(sum.today_pl)}
                </h3>
              </div>
              <div className="kpi-card">
                <p># Portfolios</p>
                <h3>{sum.num_portfolios}</h3>
              </div>
              <div className="kpi-card">
                <p>Last Sync</p>
                <h3>{dayjs(sum.last_sync).format('HH:mm:ss')}</h3>
              </div>
            </>
          ) : (
            Array.from({ length: 4 }).map((_, i) => <Skel key={i} h={88} />)
          )}
        </section>

        {/* CHARTS */}
        <section className="charts">
          {charts ? (
            <>
              {/* 1) Portfolio Value vs Time */}
              <div className="chart large">
                <h2 className="chart-title">Portfolio Value vs Time</h2>
                <ResponsiveContainer width="100%" height={240}>
                  <LineChart data={charts.portfolio_value}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                    <XAxis
                      dataKey="date"
                      stroke="#6B7280"
                      tick={{ fontSize: 12 }}
                    />
                    <YAxis
                      stroke="#6B7280"
                      tick={{ fontSize: 12 }}
                      domain={[0, 'auto']}
                    />
                    <Tooltip
                      formatter={(v) => '$' + (+v).toLocaleString()}
                      contentStyle={{
                        backgroundColor: '#ffffff',
                        border: '1px solid #E5E7EB',
                        borderRadius: 4,
                      }}
                      labelStyle={{ color: '#000000' }}
                      itemStyle={{ color: '#000000' }}
                    />
                    <Line
                      type="monotone"
                      dataKey="value"
                      stroke="#2563EB"
                      strokeWidth={2}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              {/* 2) Daily P/L */}
              <div className="chart small">
                <h2 className="chart-title">Daily P/L</h2>
                <ResponsiveContainer width="100%" height={240}>
                  <BarChart data={charts.daily_pl}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                    <XAxis
                      dataKey="date"
                      stroke="#6B7280"
                      tick={{ fontSize: 12 }}
                    />
                    <YAxis
                      stroke="#6B7280"
                      tick={{ fontSize: 12 }}
                      domain={[0, 'auto']}
                    />
                    <Tooltip
                      formatter={(v) => '$' + (+v).toLocaleString()}
                      contentStyle={{
                        backgroundColor: '#ffffff',
                        border: '1px solid #E5E7EB',
                        borderRadius: 4,
                      }}
                      labelStyle={{ color: '#000000' }}
                      itemStyle={{ color: '#000000' }}
                    />
                    <Bar dataKey="pl" isAnimationActive={false}>
                      {charts.daily_pl.map((entry, idx) => (
                        <Cell
                          key={idx}
                          fill={entry.pl < 0 ? '#EF4444' : '#10B981'}
                        />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* 3) Allocation */}
              <div className="chart small">
                <h2 className="chart-title">Allocation</h2>
                <ResponsiveContainer width="100%" height={200}>
                  <PieChart>
                    <Tooltip
                      formatter={(value, name) => [
                        `${(+value).toFixed(1)}%`,
                        name,
                      ]}
                      contentStyle={{
                        backgroundColor: '#ffffff',
                        border: '1px solid #E5E7EB',
                        borderRadius: 4,
                      }}
                      labelStyle={{ color: '#000000' }}
                      itemStyle={{ color: '#000000' }}
                    />
                    <Pie
                      data={charts.allocation}
                      dataKey="share_percent"
                      nameKey="name"
                      innerRadius={60}
                      outerRadius={100}
                      labelLine={false}
                      labelPosition="outside"
                      offset={8}
                      label={({ name, share_percent }) =>
                        `${name} (${(+share_percent).toFixed(1)}%)`
                      }
                    >
                      {charts.allocation.map((_, idx) => {
                        const COLORS = ['#6366F1', '#10B981'];
                        return (
                          <Cell
                            key={idx}
                            fill={COLORS[idx % COLORS.length]}
                          />
                        );
                      })}
                    </Pie>
                  </PieChart>
                </ResponsiveContainer>

                <div className="allocation-legend">
                  {charts.allocation.map((entry, idx) => {
                    const COLORS = ['#6366F1', '#10B981'];
                    return (
                      <div key={idx} className="legend-item">
                        <span
                          className="legend-dot"
                          style={{ backgroundColor: COLORS[idx] }}
                        ></span>
                        <span className="legend-text">
                          {entry.name} (
                          {(+entry.share_percent).toFixed(1)}%)
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>
            </>
          ) : (
            <Skel h={260} />
          )}
        </section>

        {/* BOTTOM ROW: Portfolios You Hold + Latest Transactions */}
        <section className="bottom-row">
          <div className="portfolios-block">
            <h2 className="section-title">Portfolios You Hold</h2>

            {ports ? (
              <table className="dash-table">
                <thead>
                  <tr>
                    <th style={{ textAlign: 'left' }}>Name</th>
                    <th style={{ textAlign: 'right' }}>Value</th>
                    <th style={{ textAlign: 'right' }}>Gain&nbsp;%</th>
                    <th style={{ width: 60, textAlign: 'center' }}>Spark</th>
                  </tr>
                </thead>
                <tbody>
                  {ports.map((p) => (
                    <tr key={p.id}>
                      <td
                        className="portfolio-name"
                        style={{ textAlign: 'left' }}
                      >
                        {p.name}
                      </td>
                      <td style={{ textAlign: 'right' }}>
                        {fmtMoney(p.value)}
                      </td>
                      <td
                        className={colored(p.gain_pct)}
                        style={{ textAlign: 'right' }}
                      >
                        {'+' + (+p.gain_pct).toFixed(1) + ' %'}
                      </td>
                      <td style={{ textAlign: 'center' }}>
                        <SparklineIcon data={p.sparkline} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <Skel h={120} />
            )}
          </div>

          <div className="tx-block">
            <h2 className="section-title">Latest Transactions</h2>
            {tx ? (
              <ul className="tx-list">
                {tx.map((t, i) => (
                  <li key={i}>
                    <span>{dayjs(t.date).format('DD MMM')}</span>
                    <span>{t.type}</span>
                    <span className={colored(t.amount)}>
                      {(t.amount >= 0 ? '+' : '') +
                        fmtMoney(Math.abs(t.amount))}
                    </span>
                    <span className="tx-note">{t.note}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <Skel h={120} />
            )}
          </div>
        </section>
      </main>
    </div>
  );
}
