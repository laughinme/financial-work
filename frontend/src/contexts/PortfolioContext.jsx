import React, {
  createContext, useContext, useMemo, useState, useEffect,
} from 'react';

import { getCurrent, updateInvested } from '../auth/storage';

/* ---------- стратегии (ваши исходные) ---------- */
const initialStrategies = [
  {
    id: 1,
    name: 'Aggressive',
    currency: 'USD',
    risk: 3,
    nav_price: 100,
    equity: 51503,
    maxDD: 52.4,
    gain_percent: -48.5,
    net_profit: -48497,
    invested: false,
    balanceEquity: [
      { date: '2025-05-26', balance: 80000, equity: 80000 },
      { date: '2025-05-27', balance: 72000, equity: 71500 },
      { date: '2025-05-28', balance: 60000, equity: 59000 },
    ],
    drawdown: [
      { date: '2025-05-26', drawdown: 0 },
      { date: '2025-05-27', drawdown: -10 },
      { date: '2025-05-28', drawdown: -20 },
    ],
    dailyPL: [
      { date: '2025-05-27', pl: -8000 },
      { date: '2025-05-28', pl: -12000 },
    ],
    sparkline_gain: [],
  },
  {
    id: 2,
    name: 'Conservative',
    currency: 'USD',
    risk: 1,
    nav_price: 50,
    equity: 10000,
    maxDD: 0.6,
    gain_percent: 0.35,
    net_profit: 35,
    invested: false,
    balanceEquity: [
      { date: '2025-06-01', balance: 10000, equity: 10000 },
      { date: '2025-06-02', balance: 10100, equity: 10080 },
      { date: '2025-06-03', balance: 10150, equity: 10120 },
    ],
    drawdown: [
      { date: '2025-06-01', drawdown: 0 },
      { date: '2025-06-02', drawdown: -0.5 },
      { date: '2025-06-03', drawdown: -0.6 },
    ],
    dailyPL: [
      { date: '2025-06-02', pl: 100 },
      { date: '2025-06-03', pl: 50 },
    ],
    sparkline_gain: [],
  },
  {
    id: 3,
    name: 'Quantum Risk',
    currency: 'EUR',
    risk: 2,
    nav_price: 200,
    equity: 25000,
    maxDD: 12.5,
    gain_percent: 30,
    net_profit: 7500,
    invested: false,
    balanceEquity: [
      { date: '2025-06-01', balance: 22000, equity: 21900 },
      { date: '2025-06-02', balance: 23500, equity: 23300 },
      { date: '2025-06-03', balance: 25000, equity: 24900 },
    ],
    drawdown: [
      { date: '2025-06-01', drawdown: 0 },
      { date: '2025-06-02', drawdown: -5 },
      { date: '2025-06-03', drawdown: -12.5 },
    ],
    dailyPL: [
      { date: '2025-06-02', pl: 300 },
      { date: '2025-06-03', pl: 400 },
    ],
    sparkline_gain: [],
  },
  {
    id: 4,
    name: 'Green Energy',
    currency: 'USD',
    risk: 2,
    nav_price: 150,
    equity: 18000,
    maxDD: 5.1,
    gain_percent: 18,
    net_profit: 3240,
    invested: false,
    balanceEquity: [
      { date: '2025-06-01', balance: 15000, equity: 14900 },
      { date: '2025-06-02', balance: 16000, equity: 15900 },
      { date: '2025-06-03', balance: 18000, equity: 17950 },
    ],
    drawdown: [
      { date: '2025-06-01', drawdown: 0 },
      { date: '2025-06-02', drawdown: -3 },
      { date: '2025-06-03', drawdown: -5.1 },
    ],
    dailyPL: [
      { date: '2025-06-02', pl: 200 },
      { date: '2025-06-03', pl: 300 },
    ],
    sparkline_gain: [],
  },
];

/* ---------- контекст ---------- */
const PortfolioContext = createContext();

export function PortfolioProvider({ children }) {
  const [strategies, setStrategies] = useState(initialStrategies);

  useEffect(() => {
    const email = getCurrent();
    if (!email) return;
    const accounts = JSON.parse(localStorage.getItem('accounts') || '[]');
    const ids = accounts.find((u) => u.email === email)?.investedIds ?? [];
    setStrategies((prev) =>
      prev.map((s) => ({ ...s, invested: ids.includes(s.id) })),
    );
  }, []);

  const toggleInvest = (id) => {
    setStrategies((prev) => {
      const updated = prev.map((s) =>
        s.id === id ? { ...s, invested: !s.invested } : s,
      );

      /* update localStorage */
      const email = getCurrent();
      if (email) {
        const investedIds = updated.filter((s) => s.invested).map((s) => s.id);
        updateInvested(email, investedIds);
      }
      return updated;
    });
  };

  const invested = strategies.filter((s) => s.invested);

  /* aggregated charts */
  const aggCharts = useMemo(() => {
    const be = new Map();
    const pl = new Map();
    invested.forEach((s) => {
      s.balanceEquity.forEach(({ date, balance, equity }) => {
        const cur = be.get(date) || { balance: 0, equity: 0 };
        be.set(date, { balance: cur.balance + balance, equity: cur.equity + equity });
      });
      s.dailyPL.forEach(({ date, pl: val }) => {
        pl.set(date, (pl.get(date) || 0) + val);
      });
    });
    return {
      balanceEquity: Array.from(be, ([date, v]) => ({ date, ...v })),
      dailyPL:       Array.from(pl, ([date, v]) => ({ date, pl: v })),
    };
  }, [invested]);

  /* KPI summary */
  const summary = useMemo(() => {
    const total_equity = invested.reduce((a, s) => a + s.equity, 0);
    const total_pnl    = invested.reduce((a, s) => a + s.net_profit, 0);
    return {
      total_equity,
      total_pnl,
      today_pl: 0,
      num_portfolios: invested.length,
    };
  }, [invested]);

  return (
    <PortfolioContext.Provider
      value={{ strategies, invested, toggleInvest, summary, aggCharts }}
    >
      {children}
    </PortfolioContext.Provider>
  );
}

export const usePortfolio = () => useContext(PortfolioContext);
