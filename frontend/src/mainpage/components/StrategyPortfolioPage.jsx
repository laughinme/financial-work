import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { FiZap, FiChevronLeft } from 'react-icons/fi';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
} from 'recharts';
import { marked } from 'marked';

import Sidebar from './Sidebar';
import BalanceEquityChart from './charts/BalanceEquityChart';
import DrawdownChart      from './charts/DrawdownChart';
import SparklineChart     from './charts/SparklineChart';

import { usePortfolio } from '../../contexts/PortfolioContext';
import './strategyPortfolio.css';

export default function StrategyPortfolioPage() {
  /* ───────── данные ───────── */
  const { id } = useParams();
  const navigate = useNavigate();
  const { strategies, toggleInvest } = usePortfolio();

  const data = strategies.find((s) => s.id.toString() === id);
  if (!data) return <div style={{ padding: 32 }}>Strategy not found</div>;

  /* helpers */
  const fmt = (n, d = 2) =>
    Number(n).toLocaleString('en-US', {
      minimumFractionDigits: d,
      maximumFractionDigits: d,
    });

  const riskIcons = Array.from({ length: data.risk }, (_, i) => (
    <FiZap key={i} size={14} />
  ));

  /* ───────── графики ───────── */
  const balanceData  = data.balanceEquity || [];
  const drawdownData = data.drawdown       || [];
  const plData = (data.dailyPL || []).map((d) => ({
    date: d.date,
    gain_percent: d.pl,
  }));

  const [tab, setTab] = useState('balance');
  const chartArea = {
    balance : <BalanceEquityChart data={balanceData} />,
    drawdown: <DrawdownChart      data={drawdownData} />,
    pl      : <SparklineChart     data={plData} full />,
  }[tab];

  /* ───────── render ───────── */
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
            <span className="broker">Broker: RoboForex</span>
          </div>

          <p className="subtitle">Short description of strategy goes here.</p>

          <button
            className={`action-btn${data.invested ? ' invested' : ''}`}
            onClick={() => toggleInvest(data.id)}
          >
            {data.invested ? 'Invested' : 'Invest'}
          </button>
        </header>

        {/* KPI GRID */}
        <section className="kpi-grid">
          <div className="kpi-card">
            <p className="kpi-label">Equity</p>
            <h3>${fmt(data.equity, 0)}</h3>
          </div>
          <div className="kpi-card">
            <p className="kpi-label">NAV price</p>
            <h3>${fmt(data.nav_price, 4)}</h3>
          </div>
          <div className="kpi-card">
            <p className="kpi-label">Gain %</p>
            <h3 className={data.gain_percent >= 0 ? 'pos' : 'neg'}>
              {data.gain_percent >= 0 ? '+' : ''}
              {data.gain_percent}%
            </h3>
          </div>
          <div className="kpi-card">
            <p className="kpi-label">Max DD</p>
            <h3 className="neg">
              {data.maxDD != null ? `${data.maxDD.toFixed(1)}%` : '—'}
            </h3>
          </div>
        </section>

        {/* CHART SECTION */}
        <section className="chart-section">
          <div className="tabs">
            <button
              onClick={() => setTab('balance')}
              className={`tab-btn${tab === 'balance' ? ' active' : ''}`}
            >
              Balance/Equity
            </button>
            <button
              onClick={() => setTab('drawdown')}
              className={`tab-btn${tab === 'drawdown' ? ' active' : ''}`}
            >
              Drawdown
            </button>
            <button
              onClick={() => setTab('pl')}
              className={`tab-btn${tab === 'pl' ? ' active' : ''}`}
            >
              Daily&nbsp;P/L
            </button>
          </div>

          <div className="chart-area">{chartArea}</div>
        </section>

        {/* ALLOCATION  */}
        {data.allocation && (
          <section className="allocation">
            <h3>Allocation</h3>
            <ResponsiveContainer width="100%" height={240}>
              <PieChart>
                <Tooltip
                  formatter={(v, n) => [`${(+v).toFixed(1)}%`, n]}
                  contentStyle={{
                    background: '#fff',
                    border: '1px solid #E5E7EB',
                    borderRadius: 4,
                    fontSize: 12,
                  }}
                />
                <Pie
                  data={data.allocation}
                  dataKey="value"
                  nameKey="name"
                  innerRadius={60}
                  outerRadius={100}
                  labelLine={false}
                  label={({ name, percent }) =>
                    `${name} ${(percent * 100).toFixed(0)}%`
                  }
                >
                  {data.allocation.map((_, i) => (
                    <Cell key={i} fill={i ? '#60a5fa' : '#fbbf24'} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </section>
        )}

        {/* PERSONAL BLOCK */}
        {data.invested && (
          <section className="personal">
            <h3>Your position</h3>
            <p>
              You own <b>{fmt(data.unitsOwned ?? 0, 3)} u</b> ({data.sharePct ?? 0}%)
            </p>
            <p>
              Current value <b>${fmt(data.currentValue ?? 0)}</b>
            </p>
            <p className="pl-line">
              Net P/L <b>{fmt(data.netPL ?? 0)}</b>
            </p>
            <div className="btn-row">
              <button
                className="btn-alt"
                onClick={() => toggleInvest(data.id)}
              >
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
              __html: marked.parse(data.description || ''),
            }}
          />
        </section>
      </main>
    </div>
  );
}
