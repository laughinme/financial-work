import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import DashboardPage   from "./mainpage/dashboard";
import PortfolioPage   from "./mainpage/components/portfolio";
import StrategyPage    from "./mainpage/components/StrategyPortfolioPage";
import AdminPage       from "./admin/AdminPage";

import { PortfolioProvider } from "./contexts/PortfolioContext";

function RootRedirect() {
  const email = localStorage.getItem("currentEmail"); // already saved in Log/Reg
  const isAdmin = email === "admin@example.com";
  return <Navigate to={isAdmin ? "/admin" : "/dashboard"} replace />;
}

export default function App() {
  return (
    <PortfolioProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/dashboard"   element={<DashboardPage />} />
          <Route path="/portfolio"   element={<PortfolioPage />} />
          <Route path="/portfolio/:id" element={<StrategyPage />} />
          <Route path="/admin"       element={<AdminPage />} />
          <Route path="*"            element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </PortfolioProvider>
  );
}
