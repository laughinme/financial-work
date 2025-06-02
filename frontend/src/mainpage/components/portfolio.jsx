import React from 'react';
import { FiSearch, FiPlus, FiStar, FiMoreHorizontal } from 'react-icons/fi';
import Sidebar from './Sidebar';
import "../../global.css";
import './portfolio.css';

const rows=[
  {id:'P-67234',avatar:'/img/avatars/a1.png',name:'Alpha Growth',email:'alpha@example.com',date:'12 Dec 2023',status:'complete'},
  {id:'P-67235',avatar:'/img/avatars/a2.png',name:'Beta Momentum',email:'beta@example.com', date:'10 Dec 2023',status:'pending'},
  {id:'P-67236',avatar:'/img/avatars/a3.png',name:'Gamma Value', email:'gamma@example.com',date:'08 Dec 2023',status:'cancel'},
];
const statusLabel={complete:'Complete',pending:'Pending',cancel:'Cancel'};

export default function PortfolioPage(){
  return(
    <div className="layout">
      <Sidebar/>

      <main className="portfolios">

        <header className="portfolios__header">
          <h1 className="portfolios__title">Portfolio List</h1>
          <div className="portfolios__right">
            <div className="search"><FiSearch size={16}/><input placeholder="Search"/></div>
            <button className="btn-primary"><FiPlus size={16}/>Add New</button>
          </div>
        </header>


        <table className="pf-table">
          <thead>
            <tr><th><input type="checkbox"/></th><th>ID #</th><th>Name</th><th>E-mail</th><th>Date</th><th>Status</th><th/></tr>
          </thead>
          <tbody>
            {rows.map(r=>(
              <tr key={r.id}>
                <td><input type="checkbox"/></td>
                <td className="muted">{r.id}</td>
                <td className="pf-name"><img src={r.avatar} alt=""/>{r.name}</td>
                <td className="email">{r.email}</td>
                <td className="muted">{r.date}</td>
                <td><span className={`badge badge--${r.status}`}>{statusLabel[r.status]}</span></td>
                <td className="actions"><FiStar size={18}/><FiMoreHorizontal size={20}/></td>
              </tr>
            ))}
          </tbody>
        </table>
      </main>
    </div>
  );
}
