import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

import DashboardPage         from './mainpage/dashboard';
import PortfolioPage         from './mainpage/components/portfolio';
import StrategyPortfolioPage from './mainpage/components/StrategyPortfolioPage';


import { PortfolioProvider } from './contexts/PortfolioContext';

export default function App() {
  return (
    <PortfolioProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/dashboard"     element={<DashboardPage />} />
          <Route path="/portfolio"     element={<PortfolioPage />} />
          <Route path="/portfolio/:id" element={<StrategyPortfolioPage />} />
          <Route path="/"   element={<Navigate to="/dashboard" replace />} />
          <Route path="*"   element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </PortfolioProvider>
  );
}
