import React, { useEffect, useState } from "react";
import { useParams, useNavigate }     from "react-router-dom";
import { FiZap, FiChevronLeft }       from "react-icons/fi";
import { marked }                     from "marked";

import Sidebar            from "./Sidebar";
import BalanceEquityChart from "./charts/BalanceEquityChart";
import DrawdownChart      from "./charts/DrawdownChart";
import SparklineChart     from "./charts/SparklineChart";

import "./strategyPortfolio.css";
import { usePortfolio }   from "../../contexts/PortfolioContext";

export default function StrategyPortfolioPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { strategies, toggleInvest, getHistory, getHolding } = usePortfolio();

  /* локальный state */
  const [history, setHistory] = useState(null);
  const [holding, setHolding] = useState(null);

  /* находим стратегию */
  const data = strategies.find((s) => s.id.toString() === id);
  if (!data) return <div style={{ padding: 32 }}>Loading…</div>;

  /* запрашиваем историю и holding */
  useEffect(() => {
    getHistory(id, 90).then(setHistory).catch(console.error);
    getHolding(id).then(setHolding).catch(() => setHolding(null));
  }, [id, getHistory, getHolding]);

  /* helpers */
  const fmt = (n, d = 2) =>
    Number(n).toLocaleString("en-US", {
      minimumFractionDigits: d,
      maximumFractionDigits: d,
    });

  const riskIcons = Array.from({ length: data.risk }, (_, i) => (
    <FiZap key={i} size={14} />
  ));

  /* данные для графиков */
  const balanceData  = history?.balance_equity || [];
  const drawdownData = history?.drawdown        || [];
  const plData       =
    history?.sparkline?.map((d) => ({
      date: d.date,
      gain_percent: d.gain_percent,
    })) || [];

  /* заглушка “No data” */
  const NoData = ({ h = 240 }) => (
    <div
      style={{
        height: h,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        color: "#6B7280",
      }}
    >
      No&nbsp;data
    </div>
  );

  /* ──────────────────────────── JSX ─────────────────────────── */
  return (
    <div className="layout">
      <Sidebar />

      <main className="strat-page">
        {/* HEADER */}
        <header className="strat-header">
          <button className="back-btn" onClick={() => navigate(-1)}>
            <FiChevronLeft size={18} /> Back
          </button>

          <div className="title-block">
            <h1 className="strat-title">
              {data.name} ({data.currency})
            </h1>
            <span className="risk-pill">{riskIcons}</span>
            <span className="broker">Broker: {data.broker}</span>
          </div>

          <p className="subtitle">{data.description}</p>

          <button
            className={`action-btn${data.invested ? " invested" : ""}`}
            onClick={() => toggleInvest(data.id)}
          >
            {data.invested ? "Invested" : "Invest"}
          </button>
        </header>

        {/* KPI GRID */}
        <section className="kpi-grid">
          <div className="kpi-card">
            <p className="kpi-label">Equity</p>
            <h3>{fmt(data.equity, 0)}</h3>
          </div>
          <div className="kpi-card">
            <p className="kpi-label">NAV price</p>
            <h3>{fmt(data.nav_price, 4)}</h3>
          </div>
          <div className="kpi-card">
            <p className="kpi-label">Gain %</p>
            <h3 className={data.gain_percent >= 0 ? "pos" : "neg"}>
              {data.gain_percent >= 0 ? "+" : ""}
              {data.gain_percent}%
            </h3>
          </div>
          <div className="kpi-card">
            <p className="kpi-label">Max DD</p>
            <h3 className="neg">{fmt(data.drawdown, 1)}%</h3>
          </div>
        </section>

        {/* ─── 3 графика в строку ─── */}
        <section className="chart-row">
          <div className="chart-box">
            <h3 className="chart-title">Balance / Equity</h3>
            {balanceData.length ? (
              <BalanceEquityChart data={balanceData} />
            ) : (
              <NoData />
            )}
          </div>

          <div className="chart-box">
            <h3 className="chart-title">Drawdown</h3>
            {drawdownData.length ? (
              <DrawdownChart data={drawdownData} />
            ) : (
              <NoData />
            )}
          </div>

          <div className="chart-box">
            <h3 className="chart-title">Daily&nbsp;P/L</h3>
            {plData.length ? (
              <SparklineChart data={plData} full />
            ) : (
              <NoData />
            )}
          </div>
        </section>

        {/* PERSONAL BLOCK */}
        {data.invested && holding && (
          <section className="personal">
            <h3>Your position</h3>
            <p>
              You own <b>{fmt(holding.units, 3)} u</b>
            </p>
            <p>
              Current value <b>${fmt(holding.current_value)}</b>
            </p>
            <p className="pl-line">
              Net P/L&nbsp;<b>{fmt(holding.pnl)}</b>
            </p>
            <div className="btn-row">
              <button className="btn-alt" onClick={() => toggleInvest(data.id)}>
                Withdraw
              </button>
            </div>
          </section>
        )}

        {/* DESCRIPTION */}
        <section className="description">
          <h3>Strategy description</h3>
          <div
            className="md"
            dangerouslySetInnerHTML={{
              __html: marked.parse(data.description || ""),
            }}
          />
        </section>
      </main>
    </div>
  );
}
