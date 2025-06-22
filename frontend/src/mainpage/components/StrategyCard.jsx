import React from "react";
import { FiUsers, FiZap } from "react-icons/fi";
import SparklineChart from "./charts/SparklineChart";
import "./strategyCard.css";

const fmt = (n, d = 0) =>
  isNaN(+n) ? "—" : (+n).toFixed(d).replace(/\B(?=(\d{3})+(?!\d))/g, " ");

/* risk icons */
const riskIcons = (risk) => {
  const cnt = Math.min(3, Math.max(1, parseInt(risk, 10) || 3));
  return Array.from({ length: cnt }, (_, i) => <FiZap key={i} size={14} />);
};

export default function StrategyCard({ strategy }) {
  const {
    name,
    currency,
    risk,
    nav_price,
    balance,
    equity,
    drawdown,
    gain_percent,
    net_profit,
    deposit,
    holders,
    duration,
    sparkline_gain,
    color = "#1f1f23",
  } = strategy;

  const gainPct = isNaN(+gain_percent) ? "—" : (+gain_percent).toFixed(1);
  const netProfit = isNaN(+net_profit)
    ? "—"
    : `${+net_profit > 0 ? "+" : ""}${(+net_profit).toFixed(2)}`;
  const drawdownPct = isNaN(+drawdown) ? "—" : `${(+drawdown).toFixed(1)}%`;

  return (
    <article className="card-strategy">
      {/* ───────────── COVER ───────────── */}
      <div className="card-strategy__cover" style={{ background: color }}>
        <div className="cover-content">
          <div className="pill">
            {riskIcons(risk)} <span className="pill-text">Risk</span>
          </div>

          <div className="main-text">
            <p className="forecast">
              {gainPct === "—"
                ? "Forecast — per year"
                : `Forecast ${gainPct}% per year`}
            </p>
            <p className="since">
              {netProfit === "—" ? "— all time" : `${netProfit}% all time`}
            </p>
          </div>

          <div className="sparkline-container">
            <SparklineChart data={(sparkline_gain || []).slice(0, 10)} />
          </div>

          <h2 className="cover-title">{name}</h2>
        </div>
      </div>

      {/* ───────────── BODY ───────────── */}
      <div className="card-strategy__body">
        <div className="metrics-row">
          <span>
            <span className="label">NAV price</span>
            <b>
              {nav_price != null ? `${fmt(nav_price, 2)} ${currency}` : "—"}
            </b>
          </span>
          <span>
            <span className="label">Balance</span>
            <b>{balance != null ? fmt(balance, 0) : "—"}</b>
          </span>
          <span>
            <span className="label">Equity</span>
            <b>{equity != null ? fmt(equity, 0) : "—"}</b>
          </span>
          </div>

        <div className="metrics-row">
          <span>
            <span className="label">Drawdown</span>
            <b>{drawdownPct}</b>
          </span>
          <span>
            <span className="label">Deposits</span>
            <b>{deposit != null ? fmt(deposit, 0) : "—"}</b>
          </span>
         
          <span>
            <span className="label">Days&nbsp;running</span>
            <b>{duration != null ? duration : "—"}</b>
          </span>
        </div>

        <div className="card-bottom">
          <FiUsers size={16} />
          <b>{holders != null ? holders : "—"}</b>
        </div>
      </div>
    </article>
  );
}
