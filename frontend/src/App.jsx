import React from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import DashboardPage        from "./mainpage/dashboard";
import PortfolioPage        from "./mainpage/components/portfolio";
import StrategyPage         from "./mainpage/components/StrategyPortfolioPage";
import ProfilePage          from "./mainpage/components/ProfilePage";
import AdminPage            from "./admin/AdminPage";
import { PortfolioProvider } from "./contexts/PortfolioContext";

const isAdmin = () =>
  localStorage.getItem("currentEmail") === "admin@example.com";

function UserOnly({ children }) {
  if (isAdmin()) return <Navigate to="/admin" replace />;
  return children;
}

function AdminOnly({ children }) {
  if (!isAdmin()) return <Navigate to="/dashboard" replace />;
  return children;
}

function RootRedirect() {
  return <Navigate to={isAdmin() ? "/admin" : "/dashboard"} replace />;
}

export default function App() {
  return (
    <PortfolioProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<RootRedirect />} />

          <Route
            path="/admin"
            element={
              <AdminOnly>
                <AdminPage />
              </AdminOnly>
            }
          />

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
          <Route
            path="/profile"
            element={
              <UserOnly>
                <ProfilePage />
              </UserOnly>
            }
          />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </PortfolioProvider>
  );
}
