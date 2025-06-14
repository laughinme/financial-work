// src/mainpage/dashboard.jsx
/* eslint-disable react-hooks/exhaustive-deps */

import React, { useEffect, useState } from "react";
import { Link, useNavigate }          from "react-router-dom";
import dayjs                          from "dayjs";

import "../global.css";
import "./dashboard.css";

import Sidebar         from "./components/Sidebar";
import SparklineChart  from "./components/charts/SparklineChart";
import { FiBarChart2 } from "react-icons/fi";

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

import { usePortfolio }             from "../contexts/PortfolioContext";
import { clearCurrent }             from "../auth/storage";
import { getMe }                    from "../api/users";
import {
  getSummary,
  getAllocation,      // <-- NEW API
  getCashflow,        // <-- NEW API
  getPortfolioValue,  // <-- NEW API
} from "../api/dashboard";
import { logout as logoutApi }      from "../api/auth";
import { listTransactions }         from "../api/transactions";
import { createDeposit }            from "../api/payments";

/* ─── Helpers ───────────────────────────────────────────────────────────── */
const fmtMoney = (n) => "$" + (+n).toLocaleString();
const colored  = (n) => (+n >= 0 ? "text-green-600" : "text-red-600");

const Skel = ({ h = 24 }) => (
  <div className="animate-pulse bg-gray-200/60 rounded-lg" style={{ height: h }} />
);

const NoData = ({ h = 240 }) => (
  <div
    className="flex items-center justify-center text-gray-500"
    style={{ height: h }}
  >
    No&nbsp;data
  </div>
);

function SparklineIcon({ data }) {
  const [show, setShow] = useState(false);
  const series = (data || []).map((p) => ({
    date: p.date,
    gain_percent: p.gain_percent,
  }));
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

/* ─── Component ─────────────────────────────────────────────────────────── */
export default function DashboardPage() {
  const navigate = useNavigate();

  /* ─────── Session check ─────────────────────── */
  const [authorized, setAuthorized] = useState(null);
  useEffect(() => {
    getMe()
      .then(() => setAuthorized(true))
      .catch(() => setAuthorized(false));
  }, []);

  /* ─────── Summary (total equity / PnL etc.) ─── */
  const [summary, setSummary] = useState(null);
  useEffect(() => {
    if (authorized) {
      getSummary().then(setSummary).catch(console.error);
    }
  }, [authorized]);

  /* ─────── NEW API data (allocation / value / cash-flow) ─── */
  const [allocation, setAllocation]       = useState(null);
  const [portfolioValue, setPortfValue]   = useState(null);
  const [cashflow, setCashflow]           = useState(null);

  useEffect(() => {
    if (!authorized) return;

    getAllocation().then(setAllocation).catch(console.error);
    getPortfolioValue(90)        // default period
      .then(setPortfValue)
      .catch(console.error);
    getCashflow(90)
      .then(setCashflow)
      .catch(console.error);
  }, [authorized]);

  /* ─────── Transactions list ─────────────────── */
  const [tx, setTx] = useState(null);
  useEffect(() => {
    if (!authorized) return;
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
  }, [authorized]);

  /* ─────── Redirect if unauthorized ──────────── */
  useEffect(() => {
    if (authorized === false) {
      clearCurrent();
      navigate("/", { replace: true });
    }
  }, [authorized, navigate]);

  /* ─────── Wait initial fetches ───────────────── */
  if (authorized === null || authorized === false || summary === null) {
    return null; // could show splash screen
  }

  /* ─────── Context-driven aggregates (old logic) */
  const { invested, aggCharts } = usePortfolio();
  const hasInvested       = invested.length > 0;

  /* prefer API portfolio-value if it arrived */
  const balanceEquityData = portfolioValue?.length
    ? portfolioValue.map((d) => ({
        date: dayjs(d.date).format("YYYY-MM-DD"),
        balance: +d.value || +d.deposits || 0, // fallback if schema differs
      }))
    : aggCharts.balanceEquity;

  /* prefer API cash-flow for Daily P/L */
  const dailyPLData = cashflow?.length
    ? cashflow.map((d) => ({
        date: dayjs(d.date).format("YYYY-MM-DD"),
        pl: (+d.deposits || 0) - (+d.withdrawals || 0),
      }))
    : aggCharts.dailyPL;

  /* ─────── KPIs ───────────────────────────────── */
  const totalEquity   = Number(summary.total_equity);
  const totalPnl      = Number(summary.total_pnl);
  const todayPnl      = Number(summary.today_pnl);
  const portfoliosNum = invested.length;

  /* ─────── Deposit handler ───────────────────── */
  const handleDeposit = async () => {
    const raw = prompt("Enter amount to deposit (USD)", "100");
    const amount = Number(raw);
    if (!amount || amount <= 0) return;

    try {
      const { url } = await createDeposit(amount, "USD", `Deposit $${amount}`);
      window.location.href = url;
    } catch {
      alert("Failed to create deposit");
    }
  };

  /* ─────── Allocation dataset : API → UI format */
  const allocForChart = allocation?.length
    ? allocation.map((a) => ({
        name: a.name,
        share_percent: Number(a.percentage),
      }))
    : null;

  /* ─────── Render ─────────────────────────────── */
  return (
    <div className="dashboard">
      <Sidebar />

      <main className="main-content">
        {/* HEADER */}
        <header className="dash-header">
          <div className="logo-circle" />

          <span>
            Total Equity:&nbsp;<b>{fmtMoney(totalEquity)}</b>
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

          <button
            className="btn-deposit logout"
            onClick={async () => {
              try {
                await logoutApi();
              } finally {
                clearCurrent();
                window.location.href = "/";
              }
            }}
          >
            Logout
          </button>
        </header>

        {/* KPI GRID */}
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
            <p># Portfolios</p>
            <h3>{portfoliosNum}</h3>
          </div>
          <div className="kpi-card">
            <p>Last Sync</p>
            <h3>{dayjs().format("HH:mm:ss")}</h3>
          </div>
        </section>

        {/* MAIN CHARTS */}
        <section className="charts">
          {/* Portfolio Value */}
          <div className="chart large">
            <h2 className="chart-title">Portfolio Value vs&nbsp;Time</h2>
            {hasInvested && balanceEquityData.length ? (
              <ResponsiveContainer width="100%" height={240}>
                <LineChart data={balanceEquityData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                  <XAxis
                    dataKey="date"
                    stroke="#6B7280"
                    tick={{ fontSize: 12 }}
                  />
                  <YAxis
                    stroke="#6B7280"
                    tick={{ fontSize: 12 }}
                    domain={[0, "auto"]}
                  />
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
              <NoData />
            )}
          </div>

          {/* Daily P/L */}
          <div className="chart small">
            <h2 className="chart-title">Daily&nbsp;P/L</h2>
            {hasInvested && dailyPLData.length ? (
              <ResponsiveContainer width="100%" height={240}>
                <BarChart data={dailyPLData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                  <XAxis
                    dataKey="date"
                    stroke="#6B7280"
                    tick={{ fontSize: 12 }}
                  />
                  <YAxis
                    stroke="#6B7280"
                    tick={{ fontSize: 12 }}
                    domain={[0, "auto"]}
                  />
                  <Tooltip formatter={(v) => "$" + (+v).toLocaleString()} />
                  <Bar dataKey="pl" isAnimationActive={false}>
                    {dailyPLData.map((d, i) => (
                      <Cell
                        key={i}
                        fill={d.pl < 0 ? "#EF4444" : "#10B981"}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <NoData />
            )}
          </div>

          {/* Allocation */}
          <div className="chart small">
            <h2 className="chart-title">Allocation</h2>
            {allocForChart ? (
              (() => {
                if (!allocForChart.length) return <NoData h={200} />;

                return (
                  <>
                    <ResponsiveContainer width="100%" height={200}>
                      <PieChart>
                        <Tooltip
                          formatter={(v, n) => [`${(+v).toFixed(1)}%`, n]}
                        />
                        <Pie
                          data={allocForChart}
                          dataKey="share_percent"
                          nameKey="name"
                          innerRadius={60}
                          outerRadius={100}
                          labelLine={false}
                          label={({ name, percent }) =>
                            `${name} ${(percent * 100).toFixed(0)}%`
                          }
                        >
                          {allocForChart.map((_, i) => (
                            <Cell
                              key={i}
                              fill={i % 2 ? "#10B981" : "#6366F1"}
                            />
                          ))}
                        </Pie>
                      </PieChart>
                    </ResponsiveContainer>

                    <div className="allocation-legend">
                      {allocForChart.map((e, i) => (
                        <div key={i} className="legend-item">
                          <span
                            className="legend-dot"
                            style={{
                              backgroundColor: i % 2 ? "#10B981" : "#6366F1",
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
              <Skel h={200} />
            )}
          </div>
        </section>

        {/* PORTFOLIOS YOU HOLD & TRANSACTIONS */}
        <section className="bottom-row">
          {/* Portfolios You Hold */}
          <div className="portfolios-block">
            <h2 className="section-title">Portfolios You Hold</h2>
            {invested.length ? (
              <table className="dash-table">
                <thead>
                  <tr>
                    <th style={{ textAlign: "left" }}>Name</th>
                    <th style={{ textAlign: "right" }}>Value</th>
                    <th style={{ textAlign: "right" }}>Gain&nbsp;%</th>
                    <th style={{ width: 60, textAlign: "center" }}>Spark</th>
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
                      <td style={{ textAlign: "right" }}>
                        {fmtMoney(p.equity)}
                      </td>
                      <td
                        className={colored(p.gain_percent)}
                        style={{ textAlign: "right" }}
                      >
                        {(p.gain_percent >= 0 ? "+" : "") +
                          (+p.gain_percent).toFixed(1)}
                        %
                      </td>
                      <td style={{ textAlign: "center" }}>
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
              <Skel h={120} />
            )}
          </div>
        </section>
      </main>
    </div>
  );
}
