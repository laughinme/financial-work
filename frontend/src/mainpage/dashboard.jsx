import React from 'react';
import '../global.css';   
import "./dashboard.css";
import Sidebar from './components/Sidebar';

export default function DashboardPage(){
  return(
    <div className="layout">
      <Sidebar/>

      <main className="main-content">

        <div className="top-bar">
          <h1 className="title">Dashboard</h1>
          <div className="date-filters">
            <input type="date" className="date-input"/>
            <input type="date" className="date-input"/>
          </div>
        </div>


        <div className="summary">
          {[
            {label:'Save Products',  value:'178+', type:'save'},
            {label:'Stock Products', value:'20+',  type:'stock'},
            {label:'Sales Products', value:'190+', type:'sales'},
            {label:'Job Application',value:'12+',  type:'jobs'},
          ].map(c=>(
            <div key={c.label} className="card">
              <div className={`card-icon ${c.type}`}/>
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
            <div className="chart-placeholder"/>
          </section>
          <section className="chart small">
            <h2 className="chart-title">Analytics</h2>
            <div className="chart-placeholder"/>
          </section>
        </div>


        <div className="bottom-panels">
          <section className="orders">
            <h2 className="panel-title">Recent Orders</h2>
            <table className="orders-table">
              <thead>
                <tr><th>Tracking no</th><th>Product Name</th><th>Price</th><th>Total Order</th><th>Total Amount</th></tr>
              </thead>
              <tbody>
                <tr><td>#98760</td><td>Product 1</td><td>$99</td><td>42</td><td>$4,158</td></tr>
              </tbody>
            </table>
          </section>
        </div>
      </main>
    </div>
  );
}
