// src/contexts/PortfolioContext.jsx
import React, {
  createContext,
  useContext,
  useEffect,
  useState,
  useMemo,
} from "react";
import {
  listPortfolios,
  invest as investApi,
  withdraw as withdrawApi,
  getHistory,
  getHolding,
} from "../api/portfolios";

const PortfolioContext = createContext();

/* нормализация чисел из API */
const toNum = (v) => (v == null ? null : +v);

export function PortfolioProvider({ children }) {
  const [strategies, setStrategies] = useState([]); // все портфели

  /* ---------- 1. первичная загрузка ---------- */
  useEffect(() => {
    listPortfolios(50, 1, true)
      .then((res) => {
        const norm = res.map((p) => ({
          id: p.id,
          name: p.name,
          description: p.description,
          broker: p.broker,
          currency: p.currency,
          risk: p.risk === "aggressive" ? 3 : p.risk === "moderate" ? 2 : 1,
          nav_price: toNum(p.nav_price),
          balance: toNum(p.balance),
          equity: toNum(p.equity),
          drawdown: toNum(p.drawdown),
          gain_percent: toNum(p.gain_percent),
          net_profit: toNum(p.net_profit),
          deposit: toNum(p.deposit),
          holders: p.holders,
          duration: p.duration,
          invested: Boolean(p.invested_by_user),
          sparkline_gain: p.sparkline_gain || [],
        }));
        setStrategies(norm);
      })
      .catch((e) => console.error("Failed to load portfolios:", e));
  }, []);

  /* ---------- 2. инвест / вывод по клику в списке ---------- */
  const toggleInvest = async (id) => {
    setStrategies((prev) =>
      prev.map((s) => (s.id === id ? { ...s, invested: !s.invested } : s))
    );

    try {
      const target = strategies.find((s) => s.id === id);
      if (!target) return;

      if (target.invested) {
        await withdrawApi(id, target.unitsOwned ?? 0);
      } else {
        await investApi(id, target.nav_price ?? 0);
      }
    } catch (e) {
      console.error("Invest/Withdraw error:", e);
    }
  };

  /* ---------- 3. helper: освежить один портфель ---------- */
  const refreshOne = (id, patch) =>
    setStrategies((prev) =>
      prev.map((s) => (s.id === id ? { ...s, ...patch } : s))
    );

  /* ---------- 4. инвестиции пользователя ---------- */
  const invested = strategies.filter((s) => s.invested);

  /* ---------- 5. агрегированные графики ---------- */
  const aggCharts = useMemo(() => {
    const be = new Map();
    const pl = new Map();
    invested.forEach((s) => {
      (s.balanceEquity || []).forEach(({ date, balance, equity }) => {
        const cur = be.get(date) || { balance: 0, equity: 0 };
        be.set(date, {
          balance: cur.balance + +balance,
          equity: cur.equity + +equity,
        });
      });
      (s.dailyPL || []).forEach(({ date, pl: val }) => {
        pl.set(date, (pl.get(date) || 0) + +val);
      });
    });
    return {
      balanceEquity: Array.from(be, ([date, v]) => ({ date, ...v })),
      dailyPL: Array.from(pl, ([date, v]) => ({ date, pl: v })),
    };
  }, [invested]);

  /* ---------- 6. KPI summary ---------- */
  const summary = useMemo(() => {
    const total_equity = invested.reduce((a, s) => a + (s.equity || 0), 0);
    const total_pnl = invested.reduce((a, s) => a + (s.net_profit || 0), 0);
    return {
      total_equity,
      total_pnl,
      today_pl: 0,
      num_portfolios: invested.length,
    };
  }, [invested]);

  return (
    <PortfolioContext.Provider
      value={{
        strategies,
        invested,
        toggleInvest,
        refreshOne,
        summary,
        aggCharts,
        getHistory,
        getHolding,
      }}
    >
      {children}
    </PortfolioContext.Provider>
  );
}

export const usePortfolio = () => useContext(PortfolioContext);
