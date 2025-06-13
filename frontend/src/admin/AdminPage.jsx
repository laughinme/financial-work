import React, { useEffect, useState, useCallback } from "react";
import dayjs from "dayjs";
import Sidebar from "../mainpage/components/Sidebar";
import { clearCurrent } from "../auth/storage";
import { listSettlements, createIntent } from "../api/admin";
import "./admin.css";

const money = (v) => (+v).toLocaleString("en-US") + " $";

export default function AdminPage() {
  const [rows, setRows] = useState(null);
  const [loading, setLoading] = useState(false);

  const load = useCallback(() => {
    setLoading(true);
    listSettlements(5)
      .then(setRows)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  useEffect(load, [load]);

  const handleIntent = async (pid) => {
    setLoading(true);
    try {
      await createIntent(pid);
      await load();
    } catch (e) {
      alert("Request failed");
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    clearCurrent();
    localStorage.removeItem("currentEmail");
    window.location.replace("/");
  };

  return (
    <div className="layout">
      <Sidebar />

      <main className="admin-content">
        <header className="admin-header">
          <h1 className="admin-title">Settlements</h1>
          <button className="btn-logout" onClick={logout}>
            Logout
          </button>
        </header>

        {!rows ? (
          <div className="admin-loading">Loading…</div>
        ) : (
          <table className="settle-table">
            <thead>
              <tr>
                <th>Портфель</th>
                <th>Δ (IN – OUT)</th>
                <th>5 последних заявок</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((s) => {
                const delta = Number(s.delta);
                const btnLabel = delta >= 0 ? "Пополнить" : "Вывести";
                return (
                  <tr key={s.portfolio_id}>
                    <td className="name-cell">{s.name}</td>
                    <td className={delta >= 0 ? "pos" : "neg"}>
                      {delta >= 0 ? "+" : "–"} {money(Math.abs(delta))}
                    </td>
                    <td>
                      <ul className="orders-list">
                        {s.orders.map((o) => (
                          <li key={o.id}>
                            <span className="order-user">{o.user_id.slice(0, 6)}…</span>
                            <span className="order-amount">
                              {o.direction === "invest" ? "+" : "–"} {money(o.amount)}
                            </span>
                            <span className={`order-status ${o.status}`}>
                              ({o.status})
                            </span>
                            <span className="order-date">
                              {dayjs(o.created_at).format("DD MMM")}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </td>
                    <td>
                      <button
                        className="btn-action"
                        disabled={loading}
                        onClick={() => handleIntent(s.portfolio_id)}
                      >
                        {btnLabel}
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </main>
    </div>
  );
}
