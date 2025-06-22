import React, { useState } from "react";
import { Link } from "react-router-dom";
import { FiSearch } from "react-icons/fi";

import Sidebar from "./Sidebar";
import StrategyCard from "./StrategyCard";

import "../../global.css";
import "./portfolio.css";

import { usePortfolio } from "../../contexts/PortfolioContext";

export default function PortfolioPage() {
  const { strategies } = usePortfolio();
  const [query, setQuery] = useState("");

  const visible = strategies.filter((s) =>
    s.name.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="layout">
      <Sidebar />

      <main className="strategies">
        <header className="strategies__header">
          <h1 className="strategies__title">All&nbsp;strategies</h1>

          <div className="search-bar">
            <FiSearch size={16} />
            <input
              type="text"
              placeholder="Find a strategy…"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>
        </header>

        <div className="card-grid">
          {visible.map((s) => (
            <Link key={s.id} to={`/portfolio/${s.id}`} className="card-link">
              <StrategyCard strategy={s} />
            </Link>
          ))}
        </div>
      </main>
    </div>
  );
}
