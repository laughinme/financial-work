// src/mainpage/dashboard.jsx
import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import dayjs from "dayjs";

import "../global.css";
import "./dashboard.css";

import Sidebar from "./components/Sidebar";
import SparklineChart from "./components/charts/SparklineChart";
import { FiX } from "react-icons/fi";

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
} from "recharts";

import { usePortfolio } from "../contexts/PortfolioContext";
import { clearCurrent } from "../auth/storage";

import { getMe }             from "../api/users";
import { getSummary }        from "../api/dashboard";
import { getBalance,
         createDeposit }     from "../api/payments";
import { logout as logoutApi } from "../api/auth";
import { listTransactions }   from "../api/transactions";

/* ─── helpers ─────────────────────────────────────────────── */
const fmtMoney = (n) => "$" + (+n).toLocaleString();
const colored  = (n) => (+n >= 0 ? "text-green-600" : "text-red-600");

/* mini-sparkline in table */
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

/* modal with large sparkline */
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

/* ─── component ───────────────────────────────────────────── */
export default function DashboardPage() {
  const navigate = useNavigate();

  /* ——— Auth check ——— */
  const [authorized, setAuthorized] = useState(null);
  useEffect(() => {
    getMe().then(() => setAuthorized(true)).catch(() => setAuthorized(false));
  }, []);

  /* redirect if not authorized */
  useEffect(() => {
    if (authorized === false) {
      clearCurrent();
      navigate("/", { replace: true });
    }
  }, [authorized, navigate]);

  /* ——— Summary (P/L, equity, etc.) ——— */
  const [summary, setSummary] = useState(null);
  useEffect(() => {
    if (authorized) getSummary().then(setSummary).catch(console.error);
  }, [authorized]);

  /* ——— Payments balance ——— */
  const [payBalance, setPayBalance] = useState(null);
  const fetchBalance = () =>
    getBalance().then(setPayBalance).catch(console.error);

  useEffect(() => {
    if (!authorized) return;
    fetchBalance().then(() => {
      /* second attempt 5 s later → успевает прийти Stripe-webhook */
      setTimeout(fetchBalance, 5000);
    });
  }, [authorized]);

  /* ——— Transactions ——— */
  const [tx, setTx] = useState(null);
  useEffect(() => {
    if (authorized) {
      listTransactions(10, 1)
        .then((rows) =>
          rows.map((t) => ({
            id:     t.id,
            date:   t.created_at,
            type:   t.type,
            amount: +t.amount,
            note:   t.comment || "",
          }))
        )
        .then(setTx)
        .catch(console.error);
    }
  }, [authorized]);

  /* sparkline modal */
  const [modal, setModal] = useState({ open: false, data: null, name: "" });

  /* portfolios data */
  const { invested, aggCharts } = usePortfolio();
  const balanceEquityData = aggCharts.balanceEquity;
  const dailyPLData       = aggCharts.dailyPL;

  /* KPI */
  const totalEquity = +summary?.total_equity || 0;
  const totalPnl    = +summary?.total_pnl    || 0;
  const todayPnl    = +summary?.today_pnl    || 0;

  /* ——— Deposit ——— */
  const handleDeposit = async () => {
    const raw = prompt("Enter amount to deposit (USD)", "100");
    const amount = Number(raw);
    if (!amount || amount <= 0) return;
    try {
      const { url } = await createDeposit(amount, "USD");
      window.location.href = url;          // Stripe Checkout
    } catch {
      alert("Failed to create deposit");
    }
  };

  /* ——— Logout ——— */
  const handleLogout = async () => {
    try { await logoutApi(); } catch {}
    clearCurrent();
    navigate("/", { replace: true });
  };

  if (authorized === null || summary === null) return null;

  /* ─── JSX ─── */
  return (
    <>
      <div className="dashboard">
        <Sidebar />

        <main className="main-content">
          {/* ███ HEADER ███ */}
          <header className="dash-header">
            <span>
              Total Equity:&nbsp;<b>{fmtMoney(totalEquity)}</b>
            </span>

            <span>
              Balance:&nbsp;
              <b>{payBalance ? fmtMoney(+payBalance.balance) : "…"}</b>
            </span>

            <span>
              P/L Today:&nbsp;
              <b className={colored(todayPnl)}>
                {todayPnl >= 0 ? "+" : ""}
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

          {/* ███ KPI GRID ███ */}
          <section className="kpi-grid">
            <div className="kpi-card">
              <p>Total P/L</p>
              <h3 className={colored(totalPnl)}>
                {totalPnl >= 0 ? "+" : ""}
                {fmtMoney(totalPnl)}
              </h3>
            </div>

            <div className="kpi-card">
              <p>Today P/L</p>
              <h3 className={colored(todayPnl)}>
                {todayPnl >= 0 ? "+" : ""}
                {fmtMoney(todayPnl)}
              </h3>
            </div>

            <div className="kpi-card">
              <p>Balance</p>
              <h3>{payBalance ? fmtMoney(+payBalance.balance) : "…"}</h3>
            </div>

            <div className="kpi-card">
              <p># Portfolios</p>
              <h3>{invested.length}</h3>
            </div>
          </section>

          {/* ███ CHARTS ███ */}
          <section className="charts">
            {/* Portfolio Value */}
            <div className="chart large">
              <h2 className="chart-title">Portfolio Value vs Time</h2>
              {invested.length && balanceEquityData.length ? (
                <ResponsiveContainer width="100%" height={240}>
                  <LineChart data={balanceEquityData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                    <XAxis dataKey="date" stroke="#6B7280" tick={{ fontSize: 12 }} />
                    <YAxis stroke="#6B7280" tick={{ fontSize: 12 }} domain={[0, "auto"]} />
                    <Tooltip formatter={(v) => "$" + (+v).toLocaleString()} />
                    <Line
                      type="monotone"
                      dataKey="balance"
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

            {/* Daily P/L */}
            <div className="chart small">
              <h2 className="chart-title">Daily P/L</h2>
              {invested.length && dailyPLData.length ? (
                <ResponsiveContainer width="100%" height={240}>
                  <BarChart data={dailyPLData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                    <XAxis dataKey="date" stroke="#6B7280" tick={{ fontSize: 12 }} />
                    <YAxis stroke="#6B7280" tick={{ fontSize: 12 }} domain={[0, "auto"]} />
                    <Tooltip formatter={(v) => "$" + (+v).toLocaleString()} />
                    <Bar dataKey="pl" isAnimationActive={false}>
                      {dailyPLData.map((d, i) => (
                        <Cell key={i} fill={d.pl < 0 ? "#EF4444" : "#10B981"} />
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
              {invested.length ? (
                (() => {
                  const total = invested.reduce((s, p) => s + p.equity, 0);
                  if (!total) return <div className="no-data">No data</div>;
                  const alloc = invested.map((p) => ({
                    name: p.name,
                    share_percent: (p.equity / total) * 100,
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
                              <Cell
                                key={i}
                                fill={i % 2 ? "#10B981" : "#6366F1"}
                              />
                            ))}
                          </Pie>
                        </PieChart>
                      </ResponsiveContainer>

                      <div className="allocation-legend">
                        {alloc.map((e, i) => (
                          <div key={i} className="legend-item">
                            <span
                              className="legend-dot"
                              style={{
                                background: i % 2 ? "#10B981" : "#6366F1",
                              }}
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
          </section>

          {/* ███ BOTTOM ROW (Portfolios + Transactions) ███ */}
          <section className="bottom-row">
            {/* Portfolios */}
            <div className="portfolios-block">
              <h2 className="section-title">Portfolios You Hold</h2>

              {invested.length ? (
                <table className="dash-table">
                  <colgroup>
                    <col style={{ width: "40%" }} />
                    <col style={{ width: "20%" }} />
                    <col style={{ width: "20%" }} />
                    <col style={{ width: "20%" }} />
                  </colgroup>

                  <thead>
                    <tr>
                      <th className="text-left">Name</th>
                      <th className="text-right">Value</th>
                      <th className="text-right">Gain %</th>
                      <th className="text-center">Spark</th>
                    </tr>
                  </thead>

                  <tbody>
                    {invested.map((p) => (
                      <tr key={p.id}>
                        <td>
                          <Link to={`/portfolio/${p.id}`} className="table-link">
                            {p.name}
                          </Link>
                        </td>

                        <td className="text-right">{fmtMoney(p.equity)}</td>

                        <td className={`text-right ${colored(p.gain_percent)}`}>
                          {(p.gain_percent >= 0 ? "+" : "") +
                            p.gain_percent.toFixed(1)}
                          %
                        </td>

                        <td className="spark-cell">
                          <SparkMini
                            data={p.sparkline_gain}
                            onClick={() =>
                              setModal({
                                open: true,
                                data: p.sparkline_gain,
                                name: p.name,
                              })
                            }
                          />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <div className="no-data">No data</div>
              )}
            </div>

            {/* Transactions */}
            <div className="tx-block">
              <h2 className="section-title">Latest Transactions</h2>
              {tx ? (
                <ul className="tx-list">
                  {tx.map((t) => (
                    <li key={t.id}>
                      <span>{dayjs(t.date).format("DD MMM")}</span>
                      <span>{t.type}</span>
                      <span className={colored(t.amount)}>
                        {(t.amount >= 0 ? "+" : "") +
                          fmtMoney(Math.abs(t.amount))}
                      </span>
                      <span className="tx-note">{t.note}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <div className="no-data">Loading…</div>
              )}
            </div>
          </section>
        </main>
      </div>

      {/* sparkline modal */}
      <SparkModal
        open={modal.open}
        onClose={() => setModal({ open: false, data: null, name: "" })}
        data={modal.data}
        title={modal.name}
      />
    </>
  );
}
