// src/App.jsx
import React                   from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import DashboardPage     from "./mainpage/dashboard";
import PortfolioPage     from "./mainpage/components/portfolio";
import StrategyPage      from "./mainpage/components/StrategyPortfolioPage";
import AdminPage         from "./admin/AdminPage";
import { PortfolioProvider } from "./contexts/PortfolioContext";

/* ─── helpers ─────────────────────────────────────────────────────────── */
const isAdmin = () => localStorage.getItem("currentEmail") === "admin@example.com";

/* страницы, запрещённые админу */
function UserOnly({ children }) {
  if (isAdmin()) return <Navigate to="/admin" replace />;
  return children;
}

/* страница, доступная только админу */
function AdminOnly({ children }) {
  if (!isAdmin()) return <Navigate to="/dashboard" replace />;
  return children;
}

/* куда вести при открытии root-URL */
function RootRedirect() {
  return <Navigate to={isAdmin() ? "/admin" : "/dashboard"} replace />;
}

/* ─── App ─────────────────────────────────────────────────────────────── */
export default function App() {
  return (
    <PortfolioProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<RootRedirect />} />

          {/* admin area */}
          <Route
            path="/admin"
            element={
              <AdminOnly>
                <AdminPage />
              </AdminOnly>
            }
          />

          {/* user area */}
          <Route
            path="/dashboard"
            element={
              <UserOnly>
                <DashboardPage />
              </UserOnly>
            }
          />
          <Route
            path="/portfolio"
            element={
              <UserOnly>
                <PortfolioPage />
              </UserOnly>
            }
          />
          <Route
            path="/portfolio/:id"
            element={
              <UserOnly>
                <StrategyPage />
              </UserOnly>
            }
          />

          {/* всё остальное → / */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </PortfolioProvider>
  );
}
