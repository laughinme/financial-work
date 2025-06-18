import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import dayjs from 'dayjs';

import '../global.css';
import './dashboard.css';

import Sidebar from './components/Sidebar';
import SparklineChart from './components/charts/SparklineChart';
import HoldingsCarousel from './components/HoldingsCarousel';

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

import { usePortfolio } from '../contexts/PortfolioContext';
import { clearCurrent } from '../auth/storage';

import { getMe }                         from '../api/users';
import {
  getSummary,
  getAllocation,
  getCashflow,
  getPortfolioValue,
} from '../api/dashboard';
import { getBalance, createDeposit }     from '../api/payments';
import { logout as logoutApi }           from '../api/auth';


const fmtMoney = (n) => '$' + (+n).toLocaleString();
const colored  = (n) => (+n >= 0 ? 'text-green-600' : 'text-red-600');


function SparkMini({ data, onClick }) {
  if (!data?.length) return null;
  return (
    <div className="spark-mini" onClick={onClick}>
      <ResponsiveContainer width="100%" height="100%">
        <SparklineChart data={data} />
      </ResponsiveContainer>
    </div>
  );
}


import { FiX } from 'react-icons/fi';
function SparkModal({ open, onClose, data, title }) {
  if (!open) return null;
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-box" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{title}</h2>
          <button className="modal-close" onClick={onClose}>
            <FiX size={20} />
          </button>
        </div>
        <div className="modal-body">
          <ResponsiveContainer width="100%" height="100%">
            <SparklineChart data={data} full />
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}


export default function DashboardPage() {
  const navigate = useNavigate();

  /* ─── Auth check ─── */
  const [authorized, setAuthorized] = useState(null);
  useEffect(() => {
    getMe().then(() => setAuthorized(true)).catch(() => setAuthorized(false));
  }, []);

  useEffect(() => {
    if (authorized === false) {
      clearCurrent();
      navigate('/', { replace: true });
    }
  }, [authorized, navigate]);

  /* ─── Summary KPI ─── */
  const [summary, setSummary] = useState(null);
  useEffect(() => {
    if (authorized) getSummary().then(setSummary).catch(console.error);
  }, [authorized]);

  /* ─── Stripe balance ─── */
  const [payBalance, setPayBalance] = useState(null);
  const fetchBalance = () =>
    getBalance().then(setPayBalance).catch(console.error);

  useEffect(() => {
    if (!authorized) return;
    fetchBalance().then(() => setTimeout(fetchBalance, 5000));
  }, [authorized]);

  /* ─── графики с бэка ─── */
  const [dailyPLData, setDailyPL]   = useState([]);
  const [valueData,  setValueData]  = useState([]);
  const [allocation, setAllocation] = useState([]);

  useEffect(() => {
    if (!authorized) return;

    /* Daily P/L  (deposits − withdrawals) */
    getCashflow(7)
      .then(rows => rows.map(r => ({
        date: r.date,
        pl  : (+r.deposits) - (+r.withdrawals),
      })))
      .then(setDailyPL)
      .catch(console.error);

    /* Portfolio value */
    getPortfolioValue(90)
      .then(rows => rows.map(r => ({
        date : r.date,
        value: +r.portfolio_value,
      })))
      .then(setValueData)
      .catch(console.error);

    /* Allocation */
    getAllocation().then(setAllocation).catch(console.error);
  }, [authorized]);

  /* portfolios (для спарклайнов) */
  const { invested, strategies } = usePortfolio();

  /* модалка sparkline */
  const [modal, setModal] = useState({ open: false, data: null, name: '' });

  /* KPI числа */
  const totalEquity = +summary?.total_equity || 0;
  const totalPnl    = +summary?.total_pnl    || 0;
  const todayPnl    = +summary?.today_pnl    || 0;

  /* ─── Deposit ─── */
  const handleDeposit = async () => {
    const raw = prompt('Enter amount to deposit (USD)', '100');
    const amount = Number(raw);
    if (!amount || amount <= 0) return;
    try {
      const { url } = await createDeposit(amount, 'USD');
      window.location.href = url;
    } catch { alert('Failed to create deposit'); }
  };

  /* ─── Logout ─── */
  const handleLogout = async () => {
    try { await logoutApi(); } catch {}
    clearCurrent();
    navigate('/', { replace: true });
  };

  if (authorized === null || summary === null) return null;

  /* ─── JSX ─── */
  return (
    <>
      <div className="dashboard">
        <Sidebar />

        <main className="main-content">
          {/* HEADER*/}
          <header className="dash-header">
            <span>
              Total Equity:&nbsp;<b>{fmtMoney(totalEquity)}</b>
            </span>

            <span>
              Balance:&nbsp;
              <b>{payBalance ? fmtMoney(+payBalance.balance) : '…'}</b>
            </span>

            <span>
              P/L Today:&nbsp;
              <b className={colored(todayPnl)}>
                {todayPnl >= 0 ? '+' : ''}
                {fmtMoney(todayPnl)}
              </b>
            </span>

            <button className="btn-deposit" onClick={handleDeposit}>
              Deposit
            </button>

            <button className="btn-deposit logout" onClick={handleLogout}>
              Logout
            </button>

            <span className="brand-name">LocalHost</span>
          </header>

          {/* KPI GRID */}
          <section className="kpi-grid">
            <div className="kpi-card">
              <p>Total P/L</p>
              <h3 className={colored(totalPnl)}>
                {totalPnl >= 0 ? '+' : ''}
                {fmtMoney(totalPnl)}
              </h3>
            </div>

            <div className="kpi-card">
              <p>Today P/L</p>
              <h3 className={colored(todayPnl)}>
                {todayPnl >= 0 ? '+' : ''}
                {fmtMoney(todayPnl)}
              </h3>
            </div>

            <div className="kpi-card">
              <p>Balance</p>
              <h3>{payBalance ? fmtMoney(+payBalance.balance) : '…'}</h3>
            </div>

            <div className="kpi-card">
              <p># Portfolios</p>
              <h3>{summary.num_portfolios ?? invested.length}</h3>
            </div>
          </section>

          {/* CHARTS */}
          <section className="charts">
            {/* Daily P/L */}
            <div className="chart small">
              <h2 className="chart-title">Daily P/L</h2>
              {dailyPLData.length ? (
                <ResponsiveContainer width="100%" height={240}>
                  <BarChart data={dailyPLData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                    <XAxis dataKey="date" stroke="#6B7280" tick={{ fontSize: 12 }} />
                    <YAxis stroke="#6B7280" tick={{ fontSize: 12 }} domain={[0, 'auto']} />
                    <Tooltip formatter={(v) => '$' + (+v).toLocaleString()} />
                    <Bar dataKey="pl" isAnimationActive={false}>
                      {dailyPLData.map((d, i) => (
                        <Cell key={i} fill={d.pl < 0 ? '#EF4444' : '#10B981'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="no-data">No data</div>
              )}
            </div>

            {/* Allocation */}
            <div className="chart small">
              <h2 className="chart-title">Allocation</h2>
              {allocation.length ? (
                (() => {
                  const alloc = allocation.map(a => ({
                    name: a.name,
                    share_percent: +a.percentage,
                  }));
                  return (
                    <>
                      <ResponsiveContainer width="100%" height={200}>
                        <PieChart>
                          <Tooltip formatter={(v, n) => [`${(+v).toFixed(1)}%`, n]} />
                          <Pie
                            data={alloc}
                            dataKey="share_percent"
                            nameKey="name"
                            innerRadius={60}
                            outerRadius={100}
                            labelLine={false}
                            label={({ name, percent }) =>
                              `${name} ${(percent * 100).toFixed(0)}%`
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
                              style={{ background: i % 2 ? '#10B981' : '#6366F1' }}
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
                <div className="no-data">No data</div>
              )}
            </div>

            {/* Portfolio Value */}
            <div className="chart large">
              <h2 className="chart-title">Portfolio Value vs Time</h2>
              {valueData.length ? (
                <ResponsiveContainer width="100%" height={240}>
                  <LineChart data={valueData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                    <XAxis dataKey="date" stroke="#6B7280" tick={{ fontSize: 12 }} />
                    <YAxis stroke="#6B7280" tick={{ fontSize: 12 }} domain={[0, 'auto']} />
                    <Tooltip formatter={(v) => '$' + (+v).toLocaleString()} />
                    <Line
                      type="monotone"
                      dataKey="value"
                      stroke="#2563EB"
                      strokeWidth={2}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div className="no-data">No data</div>
              )}
            </div>
          </section>

          {/* BOTTOM ROW */}
          <section className="bottom-row">
            {/* Portfolio Holdings */}
            <div className="portfolios-block">
              <h2 className="section-title">Portfolio Holdings</h2>
              <HoldingsCarousel
                data={allocation.map(a => ({
                  id: a.id,
                  name: a.name,
                  percentage: a.percentage,
                  spark: (strategies.find(s => s.id === a.id) || {}).sparkline_gain,
                }))}
              />
            </div>

            {/* Latest Transactions */}
            <div className="tx-block">
              <h2 className="section-title">Latest Transactions</h2>
             
              <div className="no-data">No data</div>
            </div>
          </section>
        </main>
      </div>

      {/* модалка sparkline */}
      <SparkModal
        open={modal.open}
        onClose={() => setModal({ open: false, data: null, name: '' })}
        data={modal.data}
        title={modal.name}
      />
    </>
  );
}
