import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  FiHome,
  FiPackage,
  FiBarChart2,
  FiMessageSquare,
  FiSettings,
} from 'react-icons/fi';

import AvatarMenu from './AvatarMenu';
import { createDeposit, createWithdraw } from '../../api/payments';

import './sidebar.css';

const nav = [
  { to: '/dashboard',  icon: FiHome,        text: 'Dashboard'  },
  { to: '/portfolio',  icon: FiPackage,     text: 'Portfolios' },
  { to: '/analytics',  icon: FiBarChart2,   text: 'Analytics'  },
  { to: '/messages',   icon: FiMessageSquare, text: 'Messages' },
  { to: '/settings',   icon: FiSettings,    text: 'Settings'   },
];

export default function Sidebar() {
  /* ── быстрые действия ── */
  const handleDeposit = async () => {
    const raw = prompt('Enter amount to DEPOSIT (USD)', '100');
    const amount = Number(raw);
    if (!amount) return;
    try {
      const { url } = await createDeposit(amount);
      window.location.href = url;
    } catch { alert('Deposit failed'); }
  };

  const handleWithdraw = async () => {
    const raw = prompt('Enter amount to WITHDRAW (USD)', '100');
    const amount = Number(raw);
    if (!amount) return;
    try {
      await createWithdraw(amount);
      alert('Withdraw request accepted');
    } catch { alert('Withdraw failed'); }
  };

  return (
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
            className={({ isActive }) => `nav-btn${isActive ? ' active' : ''}`}
          >
            <Icon size={20} />
            <span className="nav-label">{text}</span>
          </NavLink>
        ))}
      </nav>

      {/* кнопки Deposit / Withdraw */}
      <div className="sidebar-actions">
        <button className="side-btn primary" onClick={handleDeposit}>
          Deposit
        </button>
        <button className="side-btn" onClick={handleWithdraw}>
          Withdraw
        </button>
      </div>
    </aside>
  );
}
