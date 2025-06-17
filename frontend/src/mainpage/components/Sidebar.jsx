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
import './sidebar.css';

const nav = [
  { to: '/dashboard',  icon: FiHome },
  { to: '/portfolio',  icon: FiPackage },
  { to: '/analytics',  icon: FiBarChart2 },
  { to: '/messages',   icon: FiMessageSquare },
  { to: '/settings',   icon: FiSettings },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      {/* Аватар пользователя */}
      <AvatarMenu initials="U" />

      <nav className="sidebar-nav">
        {nav.map(({ to, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            end
            className={({ isActive }) => `nav-btn${isActive ? ' active' : ''}`}
          >
            <Icon size={22} />
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
