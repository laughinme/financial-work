import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import {
  FiHome,
  FiPackage,
  FiBarChart2,
  FiMessageSquare,
  FiSettings,
} from "react-icons/fi";

import MoneyModal from "./ui/MoneyModal";
import {
  createDeposit,
  createWithdraw,
  getOnboardingLink,
  DASHBOARD_URL,
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
  const [modal, setModal] = useState({ open: false, type: null }); 

  /* ── API calls ───────────────────────────── */
  const doDeposit = async (amount) => {
    const { url } = await createDeposit(amount);
    window.location.href = url; 
  };

  const doWithdraw = async (amount) => {
    try {
      await createWithdraw(amount);
      alert("Withdraw request accepted");
      window.location.href = DASHBOARD_URL;
    } catch (err) {
      const needOnboard =
        err.status === 412 || /onboarding/i.test(err.message);
      if (needOnboard) {
        const { url } = await getOnboardingLink();
        window.location.href = url;
      } else {
        alert(err.message || "Withdraw failed");
      }
    }
  };

  const onSubmit = modal.type === "deposit" ? doDeposit : doWithdraw;

  /* ── JSX ─────────────────────────────────── */
  return (
    <>
      <aside className="sidebar">
        <AvatarMenu initials="U" />

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

        {/* Quick actions */}
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
