import React from 'react';
import './dashboard.css';
import {
  FiHome,
  FiBarChart2,
  FiPackage,
  FiShoppingCart,
  FiMessageSquare,
  FiSettings,
} from 'react-icons/fi';

const navIcons = [
  FiHome,
  FiBarChart2,
  FiPackage,
  FiShoppingCart,
  FiMessageSquare,
  FiSettings,
];

const DashboardPage = () => (
  <div className="dashboard">


    <aside className="sidebar">
      <div className="sidebar-logo" />
      <nav className="sidebar-nav">
        {navIcons.map((Icon, idx) => (
          <button key={idx} className="nav-btn">
            <Icon size={24} />
          </button>
        ))}
      </nav>
    </aside>


    <main className="main-content">

      <div className="top-bar">
        <h1 className="title">Dashboard</h1>
        <div className="date-filters">
          <input type="date" className="date-input" />
          <input type="date" className="date-input" />
        </div>
      </div>

      <div className="summary">
        {[
          { label: 'Save Products', value: '178+', type: 'save' },
          { label: 'Stock Products', value: '20+',  type: 'stock' },
          { label: 'Sales Products', value: '190+', type: 'sales' },
          { label: 'Job Application', value: '12+', type: 'jobs' },
        ].map((c) => (
          <div key={c.label} className="card">
            <div className={`card-icon ${c.type}`} />
            <div className="card-info">
              <div className="card-label">{c.label}</div>
              <div className="card-value">{c.value}</div>
            </div>
          </div>
        ))}
      </div>


      <div className="charts">
        <section className="chart large">
          <h2 className="chart-title">Reports</h2>
          <div className="chart-placeholder" />
        </section>
        <section className="chart small">
          <h2 className="chart-title">Analytics</h2>
          <div className="chart-placeholder" />
        </section>
      </div>


      <div className="bottom-panels">
        <section className="orders">
          <h2 className="panel-title">Recent Orders</h2>
          <table className="orders-table">
            <thead>
              <tr>
                <th>Tracking no</th>
                <th>Product Name</th>
                <th>Price</th>
                <th>Total Order</th>
                <th>Total Amount</th>
              </tr>
            </thead>
            <tbody>
              {Array.from({ length:1 }).map((_, i) => (
                <tr key={i}>
                  <td>#9876{i}</td>
                  <td>Product {i + 1}</td>
                  <td>$99</td>
                  <td>42</td>
                  <td>$4,158</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="top-products">
          <h2 className="panel-title">Top selling Products</h2>
          <ul className="product-list">
            
          </ul>
        </section>
      </div>
    </main>
  </div>
);

export default DashboardPage;
