import React, { useEffect, useState, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import dayjs from "dayjs";

import Sidebar from "./Sidebar";
import "../dashboard.css";
import "./profilePage.css";

import MoneyModal from "./ui/MoneyModal";
import TimeRangeSelector from "./TimeRangeSelector";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  Cell,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

import {
  createDeposit,
  createWithdraw,
  getOnboardingLink,
  getBalance,
  DASHBOARD_URL,
} from "../../api/payments";
import { getSummary } from "../../api/dashboard";
import { listTransactions } from "../../api/transactions";
import { usePortfolio } from "../../contexts/PortfolioContext";
import { logout as logoutApi } from "../../api/auth";
import { clearCurrent, clearTokens } from "../../auth/storage";

const fmtMoney = (n) => "$" + (+n).toLocaleString();
const colored = (n) => (+n >= 0 ? "text-green-600" : "text-red-600");

const RANGES = [
  { label: "1M", days: 30 },
  { label: "3M", days: 90 },
  { label: "6M", days: 180 },
  { label: "1Y", days: 360 },
];

export default function ProfilePage() {
  const navigate = useNavigate();

  /* ─ summary ─ */
  const [summary, setSummary] = useState(null);
  useEffect(() => {
    getSummary().then(setSummary).catch(console.error);
  }, []);

  /* ─ balance ─ */
  const [payBalance, setPayBalance] = useState(null);
  const fetchBalance = () =>
    getBalance().then(setPayBalance).catch(console.error);
  useEffect(() => {
    fetchBalance();
  }, []);

  /* ─ investments count ─ */
  const { invested } = usePortfolio();

  /* ─ transactions ─ */
  const [tx, setTx] = useState(null);
  const [showAll, setShowAll] = useState(false);
  useEffect(() => {
    listTransactions(100, 1).then(setTx).catch(console.error);
  }, []);
  const visibleTx = tx ? (showAll ? tx : tx.slice(0, 5)) : [];

  /* ─ chart transactions over time ─ */
  const [range, setRange] = useState(30);
  // filter and map to chart data
  const chartData = useMemo(() => {
    if (!tx) return [];
    return tx
      .map((t) => ({
        date: t.created_at,
        amount: +t.amount,
      }))
      .filter((d) => dayjs(d.date).isAfter(dayjs().subtract(range, "day")));
  }, [tx, range]);

  /* ─ Deposit / Withdraw modal ─ */
  const [modal, setModal] = useState({ open: false, type: null });
  const doDeposit = async (usd) => {
    const { url } = await createDeposit(usd);
    window.location.href = url;
  };
  const doWithdraw = async (usd) => {
    try {
      await createWithdraw(usd);
      alert("Withdraw request accepted");
      window.location.href = DASHBOARD_URL;
    } catch (err) {
      const needOnboarding =
        err.status === 412 || /onboarding/i.test(err.message);
      if (needOnboarding) {
        const { url } = await getOnboardingLink();
        window.location.href = url;
      } else {
        alert(err.message || "Withdraw failed");
      }
    }
  };
  const onSubmit = modal.type === "deposit" ? doDeposit : doWithdraw;

  /* ─ logout ─ */
  const handleLogout = async () => {
    try {
      await logoutApi();
    } catch {}
    clearTokens();
    clearCurrent();
    navigate("/", { replace: true });
  };

  if (!summary) return null;
  const portfolioCnt =
    summary.num_portfolios != null ? summary.num_portfolios : invested.length;

  return (
    <>
      <div className="layout">
        <Sidebar />

        <main className="main-content profile-container">
          {/* Header */}
          <div className="header-profile">
            <h1 style={{ margin: 0 }}>Profile</h1>
            <button
              className="btn-pill btn-primary"
              onClick={() => setModal({ open: true, type: "deposit" })}
            >
              Deposit
            </button>
            <button
              className="btn-pill btn-primary"
              onClick={() => setModal({ open: true, type: "withdraw" })}
            >
              Withdraw
            </button>
            <div className="spacer" />
            <button className="btn-pill btn-danger" onClick={handleLogout}>
              Logout
            </button>
          </div>

          {/* KPI inline */}
          <div className="kpi-inline">
            <span>
              Total&nbsp;Balance
              <b>
                {payBalance
                  ? fmtMoney(+payBalance.balance)
                  : fmtMoney(summary.total_equity)}
              </b>
            </span>
            <span>
              Total&nbsp;P/L
              <b className={colored(summary.total_pnl)}>
                {(summary.total_pnl >= 0 ? "+" : "") +
                  fmtMoney(summary.total_pnl)}
              </b>
            </span>
            <span>
              Portfolios<b>{portfolioCnt}</b>
            </span>
          </div>

          {/* Transactions chart */}
          <section className="chart">
            <h2 className="chart-title">All Transactions</h2>
            {chartData.length ? (
              <ResponsiveContainer width="100%" height={240}>
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                  <XAxis
                    dataKey="date"
                    stroke="#6B7280"
                    tick={{ fontSize: 12 }}
                    tickFormatter={(d) => dayjs(d).format("DD MMM")}
                  />
                  <YAxis
                    stroke="#6B7280"
                    tick={{ fontSize: 12 }}
                    tickFormatter={(v) => fmtMoney(Math.abs(v))}
                  />
                  <Tooltip
                    formatter={(v, name) => [
                      `${v >= 0 ? "" : "-"}${fmtMoney(Math.abs(v))}`,
                      name,
                    ]}
                    labelFormatter={(d) => dayjs(d).format("DD MMM YYYY")}
                  />
                  <Bar
                    dataKey="amount"
                    name="Amount"
                    barSize={10}
                    isAnimationActive={true}
                    animationDuration={800}
                  >
                    {chartData.map((d, i) => (
                      <Cell
                        key={i}
                        fill={d.amount < 0 ? "#EF4444" : "#10B981"}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="no-data">No data</div>
            )}
            <TimeRangeSelector
              ranges={RANGES}
              value={range}
              onChange={setRange}
            />
          </section>

          {/* Transactions list */}
          <section className="tx-block">
            <h2 className="section-title">Your Transactions</h2>
            {tx ? (
              <>
                <ul className="tx-list">
                  {visibleTx.map((t) => (
                    <li key={t.id}>
                      <span>
                        {dayjs(t.created_at || t.date).format("DD MMM")}
                      </span>
                      <span>{t.type}</span>
                      <span className={colored(t.amount)}>
                        {(t.amount >= 0 ? "+" : "") +
                          fmtMoney(Math.abs(t.amount))}
                      </span>
                      <span className="tx-note">{t.comment || t.note}</span>
                    </li>
                  ))}
                </ul>
                {tx.length > 5 && (
                  <button
                    className="show-btn"
                    onClick={() => setShowAll(!showAll)}
                  >
                    {showAll ? "Hide" : "Show all"}
                  </button>
                )}
              </>
            ) : (
              <div className="no-data">Loading…</div>
            )}
          </section>
        </main>
      </div>

      {/* MoneyModal */}
      <MoneyModal
        open={modal.open}
        title={modal.type === "deposit" ? "Deposit USD" : "Withdraw USD"}
        label="Amount (USD)"
        onClose={() => setModal({ open: false, type: null })}
        onSubmit={onSubmit}
      />
    </>
  );
}
