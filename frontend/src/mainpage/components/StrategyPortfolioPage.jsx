
import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { FiZap, FiChevronLeft } from "react-icons/fi";
import dayjs from "dayjs";
import { marked } from "marked";

import Sidebar from "./Sidebar";
import BalanceEquityChart from "./charts/BalanceEquityChart";
import SparklineChart from "./charts/SparklineChart";
import MoneyModal from "./ui/MoneyModal";

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

import "./strategyPortfolio.css";
import { usePortfolio } from "../../contexts/PortfolioContext";
import {
  invest as investApi,
  withdraw as withdrawApi,
  getPortfolio,
  getHistory,
} from "../../api/portfolios";

const CHART_HEIGHT = 240;
const fmt = (n, d = 2) =>
  Number(n).toLocaleString("en-US", {
    minimumFractionDigits: d,
    maximumFractionDigits: d,
  });

export default function StrategyPortfolioPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { strategies, refreshOne } = usePortfolio();

  const strat = strategies.find((s) => s.id.toString() === id);
  if (!strat) return <div style={{ padding: 32 }}>Loading…</div>;


  const [charts, setCharts] = useState(null);
  const [modal, setModal] = useState({ open: false, type: null }); 

  /* ───────── load charts ───────── */
  useEffect(() => {
    getHistory(id, 90).then(setCharts).catch(console.error);
  }, [id]);

  /* ───────── Invest / Withdraw ───────── */
  const handleInvest = async (usd) => {
    await investApi(id, usd);    
    await refreshOne(+id);
  };

  const handleWithdraw = async (units) => {
    await withdrawApi(id, units); 
    await refreshOne(+id);
  };

  /* ───────── fetch fresh data on mount ───────── */
  useEffect(() => {
    getPortfolio(id)
      .then(() => refreshOne(+id))
      .catch(() => {});
  }, [id, refreshOne]);

  /* ───────── helpers ───────── */
  const investedNow = strat.invested;
  const riskIcons = Array.from({ length: strat.risk }, (_, i) => (
    <FiZap key={i} size={14} />
  ));
  const NoData = () => <div className="nodata">No&nbsp;data</div>;

  /* ───────── charts ───────── */
  const balanceData = charts?.balance_equity || [];
  const drawdownData =
    charts?.drawdown?.map((d) => ({ ...d, drawdown: -+d.drawdown })) || [];
  const plData =
    charts?.sparkline?.map((d) => ({
      date: d.date,
      gain_percent: d.gain_percent,
    })) || [];

  /* ───────── render ───────── */
  return (
    <>
      <div className="layout">
        <Sidebar />

        <main className="strat-page">
          {/* ---------------- Header ---------------- */}
          <header className="strat-header">
            <button className="back-btn" onClick={() => navigate(-1)}>
              <FiChevronLeft size={18} /> Back
            </button>

            <div className="title-block">
              <h1 className="strat-title">
                {strat.name} ({strat.currency})
              </h1>
              <span className="risk-pill">{riskIcons}</span>
              <span className="broker">Broker: {strat.broker}</span>
            </div>

            {/* -------- Invest (USD) -------- */}
            <button
              className="action-btn"
              onClick={() => setModal({ open: true, type: "invest" })}
            >
              Invest
            </button>

            {/* -------- Withdraw (units) -------- */}
            <button
              className="action-btn"
              style={{ right: 140 }}
              onClick={() => setModal({ open: true, type: "withdraw" })}
              disabled={!investedNow}
            >
              Withdraw
            </button>
          </header>

          {/* ---------------- KPI ---------------- */}
          <section className="kpi-grid">
            <div className="kpi-card">
              <p className="kpi-label">Equity</p>
              <h3>{fmt(strat.equity, 0)}</h3>
            </div>
            <div className="kpi-card">
              <p className="kpi-label">NAV price</p>
              <h3>{fmt(strat.nav_price, 4)}</h3>
            </div>
            <div className="kpi-card">
              <p className="kpi-label">Gain %</p>
              <h3 className={strat.gain_percent >= 0 ? "pos" : "neg"}>
                {strat.gain_percent >= 0 ? "+" : ""}
                {fmt(strat.gain_percent, 2)}%
              </h3>
            </div>
            <div className="kpi-card">
              <p className="kpi-label">Max DD</p>
              <h3 className="neg">{fmt(strat.drawdown, 1)}%</h3>
            </div>
            <div className="kpi-card">
              <p className="kpi-label">Invested</p>
              <h3>
                {investedNow && strat.user_value != null
                  ? fmt(strat.user_value, 0) + " $"
                  : "—"}
              </h3>
            </div>
          </section>

          {/* ---------------- Charts ---------------- */}
          <section className="chart-row">
            {/* Balance / Equity */}
            <div className="chart-box">
              <h3 className="chart-title">Balance / Equity</h3>
              <div className="chart-wrapper" style={{ height: CHART_HEIGHT }}>
                {balanceData.length ? (
                  <BalanceEquityChart data={balanceData} />
                ) : (
                  <NoData />
                )}
              </div>
            </div>

            {/* Drawdown */}
            <div className="chart-box">
              <h3 className="chart-title">Drawdown</h3>
              <div className="chart-wrapper" style={{ height: CHART_HEIGHT }}>
                {drawdownData.length ? (
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={drawdownData}>
                      <CartesianGrid stroke="#E5E7EB" strokeDasharray="3 3" />
                      <XAxis
                        dataKey="date"
                        tickFormatter={(d) => dayjs(d).format("DD MMM")}
                        tick={{ fontSize: 11 }}
                        stroke="#6B7280"
                        tickLine={false}
                        axisLine={{ stroke: "#D1D5DB" }}
                        interval="preserveStartEnd"
                      />
                      <YAxis
                        domain={[-100, 0]}
                        tickFormatter={(v) => Math.abs(v)}
                        tick={{ fontSize: 11 }}
                        stroke="#6B7280"
                        tickLine={false}
                        axisLine={{ stroke: "#D1D5DB" }}
                      />
                      <Tooltip
                        formatter={(v) => `${Math.abs(v)}%`}
                        labelFormatter={(d) =>
                          `Date: ${dayjs(d).format("DD MMM")}`
                        }
                      />
                      <Bar dataKey="drawdown" baseValue={0} barSize={4}>
                        {drawdownData.map((_, i) => (
                          <Cell key={i} fill="#EF4444" />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                ) : (
                  <NoData />
                )}
              </div>
            </div>

            {/* Daily P/L */}
            <div className="chart-box">
              <h3 className="chart-title">Daily P/L</h3>
              <div className="chart-wrapper" style={{ height: CHART_HEIGHT }}>
                {plData.length ? (
                  <SparklineChart data={plData} full />
                ) : (
                  <NoData />
                )}
              </div>
            </div>
          </section>

          {/* ---------------- Description ---------------- */}
          <section className="description">
            <h3>Strategy description</h3>
            <div
              className="md"
              dangerouslySetInnerHTML={{
                __html: marked.parse(strat.description || ""),
              }}
            />
          </section>
        </main>
      </div>

      {/* ---------- MoneyModal ---------- */}
      <MoneyModal
        open={modal.open}
        title={modal.type === "withdraw" ? "Withdraw units" : "Invest USD"}
        label={modal.type === "withdraw" ? "Units" : "Amount (USD)"}
        mode={modal.type === "withdraw" ? "withdraw" : "invest"}
        navPrice={strat.nav_price}
        onClose={() => setModal({ open: false, type: null })}
        onSubmit={modal.type === "withdraw" ? handleWithdraw : handleInvest}
      />
    </>
  );
}
