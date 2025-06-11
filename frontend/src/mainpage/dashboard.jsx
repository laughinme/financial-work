import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
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

import { fetchCharts, fetchTx } from '../mock/api';
import { usePortfolio } from '../contexts/PortfolioContext';

/** ═══════════ helpers ═══════════ */
const fmtMoney = (n) => '$' + (+n).toLocaleString();
const colored  = (n) => (+n >= 0 ? 'text-green-600' : 'text-red-600');
const Skel = ({ h = 24 }) => (
  <div className="animate-pulse bg-gray-200/60 rounded-lg" style={{ height: h }} />
);

function SparklineIcon({ data }) {
  const [show, setShow] = useState(false);
  const series = Array.isArray(data)
    ? data.slice(0, 30).map((p) => ({ date: p.date, gain_percent: p.gain_percent }))
    : [];
  return (
    <span
      className="spark-container"
      onMouseEnter={() => setShow(true)}
      onMouseLeave={() => setShow(false)}
    >
      <FiBarChart2 size={18} className="spark-icon" />
      <div className="spark-tooltip">
        {show && series.length > 0 && (
          <ResponsiveContainer width="100%" height="100%">
            <SparklineChart data={series} full />
          </ResponsiveContainer>
        )}
      </div>
    </span>
  );
}

/** ═══════════ DashboardPage ═══════════ */
export default function DashboardPage() {
  const { summary, invested, aggCharts } = usePortfolio();

  const [mockCharts, setMockCharts] = useState(null);
  const [tx,         setTx]         = useState(null);

  useEffect(() => { fetchCharts().then(setMockCharts); }, []);
  useEffect(() => { fetchTx().then(setTx);             }, []);

  // есть ли реальные портфели?
  const hasInvested = invested.length > 0;

  // Для графиков Balance/Equity и Daily P/L делаем единый источник
  const balanceEquityData = hasInvested
    ? aggCharts.balanceEquity
    : mockCharts?.portfolio_value.map((p) => ({
        date: p.date,
        balance: p.value,
        equity:  p.value,
      })) || [];

  const dailyPLData = hasInvested
    ? aggCharts.dailyPL
    : mockCharts?.daily_pl.map((p) => ({
        date: p.date,
        pl:   p.pl,
      })) || [];

  return (
    <div className="dashboard">
      <Sidebar />

      <main className="main-content">
        {/* HEADER */}
        <header className="dash-header">
          <div className="logo-circle" />

          {hasInvested || mockCharts ? (
            <>
              <span>
                Total Equity:&nbsp;
                <b>{fmtMoney(summary.total_equity)}</b>
              </span>
              <span>
                P/L Today:&nbsp;
                <b className={colored(summary.today_pl)}>
                  {'+' + fmtMoney(summary.today_pl)}
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
          {hasInvested || mockCharts ? (
            <>
              <div className="kpi-card">
                <p>Total P/L</p>
                <h3 className={colored(summary.total_pnl)}>
                  {'+' + fmtMoney(summary.total_pnl)}
                </h3>
              </div>
              <div className="kpi-card">
                <p>Today P/L</p>
                <h3 className={colored(summary.today_pl)}>
                  {'+' + fmtMoney(summary.today_pl)}
                </h3>
              </div>
              <div className="kpi-card">
                <p># Portfolios</p>
                <h3>{summary.num_portfolios}</h3>
              </div>
              <div className="kpi-card">
                <p>Last Sync</p>
                <h3>{dayjs().format('HH:mm:ss')}</h3>
              </div>
            </>
          ) : (
            Array.from({ length: 4 }).map((_, i) => <Skel key={i} h={88} />)
          )}
        </section>

        {/* MAIN CHARTS */}
        <section className="charts">
          {(hasInvested || mockCharts) ? (
            <>
              {/* Portfolio Value */}
              <div className="chart large">
                <h2 className="chart-title">Portfolio Value vs Time</h2>
                <ResponsiveContainer width="100%" height={240}>
                  <LineChart data={balanceEquityData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                    <XAxis dataKey="date" stroke="#6B7280" tick={{ fontSize: 12 }} />
                    <YAxis stroke="#6B7280" tick={{ fontSize: 12 }} domain={[0, 'auto']} />
                    <Tooltip
                      formatter={(v) => '$' + (+v).toLocaleString()}
                      contentStyle={{ background: '#fff', border: '1px solid #E5E7EB', borderRadius: 4 }}
                    />
                    <Line type="monotone" dataKey="balance" stroke="#2563EB" strokeWidth={2} dot={false} />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              {/* Daily P/L */}
              <div className="chart small">
                <h2 className="chart-title">Daily P/L</h2>
                <ResponsiveContainer width="100%" height={240}>
                  <BarChart data={dailyPLData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                    <XAxis dataKey="date" stroke="#6B7280" tick={{ fontSize: 12 }} />
                    <YAxis stroke="#6B7280" tick={{ fontSize: 12 }} domain={[0, 'auto']} />
                    <Tooltip
                      formatter={(v) => '$' + (+v).toLocaleString()}
                      contentStyle={{ background: '#fff', border: '1px solid #E5E7EB', borderRadius: 4 }}
                    />
                    <Bar dataKey="pl" isAnimationActive={false}>
                      {dailyPLData.map((d, i) => (
                        <Cell key={i} fill={d.pl < 0 ? '#EF4444' : '#10B981'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Allocation */}
              <div className="chart small">
                <h2 className="chart-title">Allocation</h2>

                {invested.length ? (
                  (() => {
                    const total = invested.reduce((a, s) => a + s.equity, 0);
                    const alloc = invested.map((s) => ({
                      name: s.name,
                      share_percent: (s.equity / total) * 100,
                    }));
                    return (
                      <>
                        <ResponsiveContainer width="100%" height={200}>
                          <PieChart>
                            <Tooltip
                              formatter={(v, n) => [`${(+v).toFixed(1)}%`, n]}
                              contentStyle={{ background: '#fff', border: '1px solid #E5E7EB', borderRadius: 4 }}
                            />
                            <Pie
                              data={alloc}
                              dataKey="share_percent"
                              nameKey="name"
                              innerRadius={60}
                              outerRadius={100}
                              labelLine={false}
                              label={({ name, share_percent }) =>
                                `${name} (${share_percent.toFixed(1)}%)`
                              }
                            >
                              {alloc.map((_, i) => (
                                <Cell key={i} fill={i % 2 ? '#10B981' : '#6366F1'} />
                              ))}
                            </Pie>
                          </PieChart>
                        </ResponsiveContainer>

                        <div className="allocation-legend">
                          {alloc.map((e, i) => (
                            <div key={i} className="legend-item">
                              <span
                                className="legend-dot"
                                style={{ backgroundColor: i % 2 ? '#10B981' : '#6366F1' }}
                              />
                              <span className="legend-text">
                                {e.name} ({e.share_percent.toFixed(1)}%)
                              </span>
                            </div>
                          ))}
                        </div>
                      </>
                    );
                  })()
                ) : (
                  <div className="flex items-center justify-center h-[200px] text-gray-500">
                    No data
                  </div>
                )}
              </div>
            </>
          ) : (
            <Skel h={260} />
          )}
        </section>

        {/* PORTFOLIOS YOU HOLD */}
        <section className="bottom-row">
          <div className="portfolios-block">
            <h2 className="section-title">Portfolios You Hold</h2>
            {invested.length ? (
              <table className="dash-table">
                <thead>
                  <tr>
                    <th style={{ textAlign: 'left' }}>Name</th>
                    <th style={{ textAlign: 'right' }}>Value</th>
                    <th style={{ textAlign: 'right' }}>Gain %</th>
                    <th style={{ width: 60, textAlign: 'center' }}>Spark</th>
                  </tr>
                </thead>
                <tbody>
                  {invested.map((p) => (
                    <tr key={p.id}>
                      <td className="portfolio-name">
                        <Link to={`/portfolio/${p.id}`} className="table-link">
                          {p.name}
                        </Link>
                      </td>
                      <td style={{ textAlign: 'right' }}>
                        {fmtMoney(p.equity)}
                      </td>
                      <td className={colored(p.gain_percent)} style={{ textAlign: 'right' }}>
                        {(p.gain_percent >= 0 ? '+' : '') +
                          (+p.gain_percent).toFixed(1)} %
                      </td>
                      <td style={{ textAlign: 'center' }}>
                        <SparklineIcon data={p.sparkline_gain} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <Skel h={120} />
            )}
          </div>

          {/* Latest Transactions */}
          <div className="tx-block">
            <h2 className="section-title">Latest Transactions</h2>
            {tx ? (
              <ul className="tx-list">
                {tx.map((t, i) => (
                  <li key={i}>
                    <span>{dayjs(t.date).format('DD MMM')}</span>
                    <span>{t.type}</span>
                    <span className={colored(t.amount)}>
                      {(t.amount >= 0 ? '+' : '') + fmtMoney(Math.abs(t.amount))}
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
