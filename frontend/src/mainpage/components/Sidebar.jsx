// src/mainpage/components/Sidebar.jsx
import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import {
  FiHome,
  FiPackage,
  FiBarChart2,
  FiMessageSquare,
  FiSettings,
} from "react-icons/fi";

import MoneyModal from "./ui/MoneyModal";          // ← NEW
import {
  createDeposit,
  createWithdraw,
} from "../../api/payments";

import AvatarMenu from "./AvatarMenu";
import "./sidebar.css";

const nav = [
  { to: "/dashboard", icon: FiHome, text: "Dashboard" },
  { to: "/portfolio", icon: FiPackage, text: "Portfolios" },
  { to: "/analytics", icon: FiBarChart2, text: "Analytics" },
  { to: "/messages", icon: FiMessageSquare, text: "Messages" },
  { to: "/settings", icon: FiSettings, text: "Settings" },
];

export default function Sidebar() {
  /* ── два модальных состояния ── */
  const [modal, setModal] = useState({ open: false, type: null }); // deposit | withdraw

  const handleDeposit = async (amount) => {
    const { url } = await createDeposit(amount);
    window.location.href = url;
  };

  const handleWithdraw = async (amount) => {
    await createWithdraw(amount);
    alert("Withdraw request accepted"); // можно заменить на toast
  };

  const onSubmit =
    modal.type === "deposit" ? handleDeposit : handleWithdraw;

  return (
    <>
      <aside className="sidebar">
        {/* аватар */}
        <AvatarMenu initials="U" />

        {/* навигация */}
        <nav className="sidebar-nav">
          {nav.map(({ to, icon: Icon, text }) => (
            <NavLink
              key={to}
              to={to}
              end
              className={({ isActive }) => `nav-btn${isActive ? " active" : ""}`}
            >
              <Icon size={20} />
              <span className="nav-label">{text}</span>
            </NavLink>
          ))}
        </nav>

        {/* кнопки Deposit / Withdraw */}
        <div className="sidebar-actions">
          <button
            className="side-btn primary"
            onClick={() => setModal({ open: true, type: "deposit" })}
          >
            Deposit
          </button>
          <button
            className="side-btn"
            onClick={() => setModal({ open: true, type: "withdraw" })}
          >
            Withdraw
          </button>
        </div>
      </aside>

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
