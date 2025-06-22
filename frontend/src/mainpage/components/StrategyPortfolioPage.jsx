import React, { useEffect, useState, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { FiZap, FiChevronLeft } from 'react-icons/fi';
import dayjs from 'dayjs';
import { marked } from 'marked';

import Sidebar from './Sidebar';
import BalanceEquityChart from './charts/BalanceEquityChart';
import SparklineChart from './charts/SparklineChart';
import MoneyModal from './ui/MoneyModal';
import ChartModal from './pages/ChartModal';

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  Cell,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
} from 'recharts';

import './strategyPortfolio.css';
import { usePortfolio } from '../../contexts/PortfolioContext';
import {
  invest as investApi,
  withdraw as withdrawApi,
  getPortfolio,
  getHistory,
} from '../../api/portfolios';

/* ───────────────────────── helpers ───────────────────────── */
const CHART_HEIGHT = 240;
const fmt = (n, d = 2) =>
  Number(n).toLocaleString('en-US', {
    minimumFractionDigits: d,
    maximumFractionDigits: d,
  });

/* ───────────────────────── component ───────────────────────── */
export default function StrategyPortfolioPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { strategies, refreshOne } = usePortfolio();

  const strat = strategies.find((s) => s.id.toString() === id);
  if (!strat) return <div style={{ padding: 32 }}>Loading…</div>;

  /* state */
  const [charts, setCharts] = useState(null);
  const [moneyModal, setMoneyModal] = useState({ open: false, type: null });

  /* big-chart pop-up */
  const [popup, setPopup] = useState({ open: false, title: '', chart: null });
  const openChart = useCallback(
    (title, chart) => setPopup({ open: true, title, chart }),
    []
  );
  const closeChart = () => setPopup({ open: false, title: '', chart: null });

  /* load history */
  useEffect(() => {
    getHistory(id, 90)
      .then(setCharts)
      .catch(console.error);
  }, [id]);

  /* refresh portfolio at mount */
  useEffect(() => {
    getPortfolio(id)
      .then(() => refreshOne(+id))
      .catch(() => {});
  }, [id, refreshOne]);

  /* Invest / Withdraw handlers */
  const handleInvest = async (usd) => {
    await investApi(id, usd);
    await refreshOne(+id);
  };
  const handleWithdraw = async (units) => {
    await withdrawApi(id, units);
    await refreshOne(+id);
  };

  const investedNow = strat.invested;
  const riskIcons = Array.from({ length: strat.risk }, (_, i) => (
    <FiZap key={i} size={14} />
  ));
  const NoData = () => <div className="nodata">No&nbsp;data</div>;

  /* chart data */
  const balanceData = charts?.balance_equity || [];
  const drawdownRaw =
    charts?.drawdown?.map((d) => ({ ...d, drawdown: -+d.drawdown })) || [];
  const plData =
    charts?.sparkline?.map((d) => ({
      date: d.date,
      gain_percent: d.gain_percent,
    })) || [];

  /*Drawdown */
  const ddMin = Math.min(...drawdownRaw.map((d) => d.drawdown), 0);
  const drawdownDomain = [ddMin * 1.05, 0]; 

  /* ───────────────────────── render ───────────────────────── */
  return (
    <>
      <div className="layout">
        <Sidebar />

        <main className="strat-page">
          {/* ---------- Header ---------- */}
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

            <button
              className="action-btn"
              onClick={() => setMoneyModal({ open: true, type: 'invest' })}
            >
              Invest
            </button>
            <button
              className="action-btn"
              style={{ right: 140 }}
              onClick={() => setMoneyModal({ open: true, type: 'withdraw' })}
              disabled={!investedNow}
            >
              Withdraw
            </button>
          </header>

          {/* ---------- KPI ---------- */}
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
              <p className="kpi-label">Gain&nbsp;%</p>
              <h3 className={strat.gain_percent >= 0 ? 'pos' : 'neg'}>
                {strat.gain_percent >= 0 ? '+' : ''}
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
                  ? fmt(strat.user_value, 0) + ' $'
                  : '—'}
              </h3>
            </div>
          </section>

          {/* ---------- Charts ---------- */}
          <section className="chart-row">
            {/* Balance / Equity (clickable) */}
            <div
              className="chart-box clickable"
              onClick={() =>
                openChart('Balance / Equity', (
                  <BalanceEquityChart data={balanceData} full />
                ))
              }
            >
              <h3 className="chart-title">Balance / Equity</h3>
              <div className="chart-wrapper" style={{ height: CHART_HEIGHT }}>
                {balanceData.length ? (
                  <BalanceEquityChart data={balanceData} />
                ) : (
                  <NoData />
                )}
              </div>
            </div>

            {/* Drawdown (clickable) */}
            <div
              className="chart-box clickable"
              onClick={() =>
                openChart(
                  'Drawdown',
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={drawdownRaw}>
                      <CartesianGrid stroke="#E5E7EB" strokeDasharray="3 3" />
                      <XAxis
                        dataKey="date"
                        tickFormatter={(d) => dayjs(d).format('DD MMM')}
                        tick={{ fontSize: 11 }}
                        stroke="#6B7280"
                        tickLine={false}
                        axisLine={{ stroke: '#D1D5DB' }}
                        interval="preserveStartEnd"
                      />
                      <YAxis
                        width={58}
                        domain={drawdownDomain}
                        tickFormatter={(v) => `${Math.abs(v).toFixed(1)}%`}
                        tick={{ fontSize: 11 }}
                        stroke="#6B7280"
                        tickLine={false}
                        axisLine={{ stroke: '#D1D5DB' }}
                      />
                      <Tooltip
                        formatter={(v) => `${Math.abs(v)}%`}
                        labelFormatter={(d) =>
                          `Date: ${dayjs(d).format('DD MMM')}`
                        }
                      />
                      <Bar dataKey="drawdown" baseValue={0} barSize={4}>
                        {drawdownRaw.map((_, i) => (
                          <Cell key={i} fill="#EF4444" />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                )
              }
            >
              <h3 className="chart-title">Drawdown</h3>
              <div className="chart-wrapper" style={{ height: CHART_HEIGHT }}>
                {drawdownRaw.length ? (
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={drawdownRaw}>
                      <CartesianGrid stroke="#E5E7EB" strokeDasharray="3 3" />
                      <XAxis
                        dataKey="date"
                        tickFormatter={(d) => dayjs(d).format('DD MMM')}
                        tick={{ fontSize: 11 }}
                        stroke="#6B7280"
                        tickLine={false}
                        axisLine={{ stroke: '#D1D5DB' }}
                        interval="preserveStartEnd"
                      />
                      <YAxis
                        width={58}
                        domain={drawdownDomain}
                        tickFormatter={(v) => `${Math.abs(v).toFixed(1)}%`}
                        tick={{ fontSize: 11 }}
                        stroke="#6B7280"
                        tickLine={false}
                        axisLine={{ stroke: '#D1D5DB' }}
                      />
                      <Tooltip
                        formatter={(v) => `${Math.abs(v)}%`}
                        labelFormatter={(d) =>
                          `Date: ${dayjs(d).format('DD MMM')}`
                        }
                      />
                      <Bar dataKey="drawdown" baseValue={0} barSize={4}>
                        {drawdownRaw.map((_, i) => (
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

            {/* Daily P/L (clickable) */}
            <div
              className="chart-box clickable"
              onClick={() =>
                openChart('Daily P/L', <SparklineChart data={plData} full />)
              }
            >
              <h3 className="chart-title">Daily P/L</h3>
              <div className="chart-wrapper" style={{ height: CHART_HEIGHT }}>
                {plData.length ? <SparklineChart data={plData} full /> : <NoData />}
              </div>
            </div>
          </section>

          {/* ---------- Description ---------- */}
          <section className="description">
            <h3>Strategy description</h3>
            <div
              className="md"
              dangerouslySetInnerHTML={{
                __html: marked.parse(strat.description || ''),
              }}
            />
          </section>
        </main>
      </div>

      {/* Money-modal */}
      <MoneyModal
        open={moneyModal.open}
        title={moneyModal.type === 'withdraw' ? 'Withdraw units' : 'Invest USD'}
        label={moneyModal.type === 'withdraw' ? 'Units' : 'Amount (USD)'}
        mode={moneyModal.type === 'withdraw' ? 'withdraw' : 'invest'}
        navPrice={strat.nav_price}
        onClose={() => setMoneyModal({ open: false, type: null })}
        onSubmit={moneyModal.type === 'withdraw' ? handleWithdraw : handleInvest}
      />

      {/* full-screen chart pop-up */}
      <ChartModal open={popup.open} title={popup.title} onClose={closeChart}>
        {popup.chart}
      </ChartModal>
    </>
  );
}
