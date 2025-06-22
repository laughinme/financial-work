// src/mainpage/components/ProfilePage.jsx
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import dayjs from "dayjs";

import Sidebar from "./Sidebar";
import "../dashboard.css";
import "./profilePage.css";

import MoneyModal from "./ui/MoneyModal";          // ← NEW

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
import { clearCurrent } from "../../auth/storage";

const fmtMoney = (n) => "$" + (+n).toLocaleString();
const colored = (n) => (+n >= 0 ? "text-green-600" : "text-red-600");

export default function ProfilePage() {
  const navigate = useNavigate();

  /* ── summary ── */
  const [summary, setSummary] = useState(null);
  useEffect(() => {
    getSummary().then(setSummary).catch(console.error);
  }, []);

  /* ── balance ── */
  const [payBalance, setPayBalance] = useState(null);
  const fetchBalance = () =>
    getBalance().then(setPayBalance).catch(console.error);

  useEffect(() => {
    fetchBalance().then(() => setTimeout(fetchBalance, 5000));
  }, []);

  /* ── invest portfolios ── */
  const { invested } = usePortfolio();

  /* ── transactions ── */
  const [tx, setTx] = useState(null);
  useEffect(() => {
    listTransactions(50, 1).then(setTx).catch(console.error);
  }, []);

  const [showAll, setShowAll] = useState(false);
  const visibleTx = tx ? (showAll ? tx : tx.slice(0, 5)) : [];

  /* ── Deposit / Withdraw modals ── */
  const [modal, setModal] = useState({ open: false, type: null });

  const doDeposit = async (amountUsd) => {
    const { url } = await createDeposit(amountUsd);
    window.location.href = url;
  };

  const doWithdraw = async (amountUsd) => {
    try {
      await createWithdraw(amountUsd);
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

  /* ── logout ── */
  const handleLogout = async () => {
    try {
      await logoutApi();
    } catch {}
    clearCurrent();
    navigate("/", { replace: true });
  };

  if (!summary) return null;

  const portfolioCnt =
    summary.num_portfolios != null
      ? summary.num_portfolios
      : invested.length;

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

          {/* Transactions */}
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
                      <span className="tx-note">
                        {t.comment || t.note}
                      </span>
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
