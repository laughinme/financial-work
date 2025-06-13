import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { FiSearch } from 'react-icons/fi';

import Sidebar from './Sidebar';
import StrategyCard from './StrategyCard';

import '../../global.css';
import './portfolio.css';


const mockStrategies = [
  {
    id: 1,
    name: 'Aggressive',
    currency: 'USD',
    risk: 3,
    nav_price: '100',
    balance: '51503.00',
    equity : '51503.00',
    drawdown: '52.370',
    gain_percent: '-48.500',
    net_profit : '-48.497',
    deposit: '0',
    holders: 0,
    duration: 9,
    sparkline_gain: [
      { date:'2025-05-26', gain_percent:'0.000'  },
      { date:'2025-05-27', gain_percent:'-23.000'},
      { date:'2025-05-28', gain_percent:'-30.000'},
      { date:'2025-05-29', gain_percent:'-35.000'},
      { date:'2025-05-30', gain_percent:'-38.000'},
      { date:'2025-05-31', gain_percent:'-41.000'},
      { date:'2025-06-01', gain_percent:'-43.000'},
      { date:'2025-06-02', gain_percent:'-46.000'},
      { date:'2025-06-03', gain_percent:'-48.500'},
      { date:'2025-06-04', gain_percent:'-50.000'},
    ],
  },
  {
    id: 2,
    name: 'Conservative',
    currency: 'USD',
    risk: 1,
    nav_price : '50',
    balance   : '10000.00',
    equity    : '10000.00',
    drawdown  : '0.000',
    gain_percent:'0.000',
    net_profit: '0.00',
    deposit: '0',
    holders: 0,
    duration: 7,
    sparkline_gain: [
      { date:'2025-05-28', gain_percent:'0.000'},
      { date:'2025-05-29', gain_percent:'0.100'},
      { date:'2025-05-30', gain_percent:'0.050'},
      { date:'2025-05-31', gain_percent:'0.150'},
      { date:'2025-06-01', gain_percent:'0.200'},
      { date:'2025-06-02', gain_percent:'0.180'},
      { date:'2025-06-03', gain_percent:'0.220'},
      { date:'2025-06-04', gain_percent:'0.250'},
      { date:'2025-06-05', gain_percent:'0.300'},
      { date:'2025-06-06', gain_percent:'0.350'},
    ],
  },
  {
    id: 3,
    name: 'Quantum Risk',
    currency: 'EUR',
    risk: 2,
    nav_price : '200',
    balance   : '25000.00',
    equity    : '25000.00',
    drawdown  : '12.5',
    gain_percent:'30.000',
    net_profit: '30.00',
    deposit: '0',
    holders: 10,
    duration: 30,
    sparkline_gain: [
      { date:'2025-05-25', gain_percent:'5.000' },
      { date:'2025-05-26', gain_percent:'10.000'},
      { date:'2025-05-27', gain_percent:'15.000'},
      { date:'2025-05-28', gain_percent:'20.000'},
      { date:'2025-05-29', gain_percent:'25.000'},
      { date:'2025-05-30', gain_percent:'27.500'},
      { date:'2025-05-31', gain_percent:'28.500'},
      { date:'2025-06-01', gain_percent:'29.000'},
      { date:'2025-06-02', gain_percent:'29.500'},
      { date:'2025-06-03', gain_percent:'30.000'},
    ],
  },
  {
    id: 4,
    name: 'Green Energy',
    currency: 'USD',
    risk: 2,
    nav_price : '150',
    balance   : '18000.00',
    equity    : '18000.00',
    drawdown  : '5.1',
    gain_percent:'18.000',
    net_profit: '18.00',
    deposit: '0',
    holders: 4,
    duration: 45,
    sparkline_gain: [
      { date:'2025-05-27', gain_percent:'1.000' },
      { date:'2025-05-28', gain_percent:'3.000' },
      { date:'2025-05-29', gain_percent:'5.000' },
      { date:'2025-05-30', gain_percent:'7.500' },
      { date:'2025-05-31', gain_percent:'9.000' },
      { date:'2025-06-01', gain_percent:'10.500'},
      { date:'2025-06-02', gain_percent:'12.000'},
      { date:'2025-06-03', gain_percent:'14.500'},
      { date:'2025-06-04', gain_percent:'16.000'},
      { date:'2025-06-05', gain_percent:'18.000'},
    ],
  },
];


export default function PortfolioPage() {
  const [query, setQuery] = useState('');

  const visible = mockStrategies.filter((s) =>
    s.name.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="layout">
      <Sidebar />

      <main className="strategies">
        <header className="strategies__header">
          <h1 className="strategies__title">Все&nbsp;стратегии</h1>

          <div className="search-bar">
            <FiSearch size={16} />
            <input
              type="text"
              placeholder="Найти стратегию…"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>
        </header>

     
        <div className="card-grid">
          {visible.map((s) => (
            <Link
              key={s.id}
              to={`/portfolio/${s.id}`}
              className="card-link"
            >
              <StrategyCard strategy={s} />
            </Link>
          ))}
        </div>
      </main>
    </div>
  );
}
