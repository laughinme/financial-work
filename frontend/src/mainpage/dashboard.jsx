import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import dayjs from 'dayjs';

import '../global.css';
import './dashboard.css';

import Sidebar          from './components/Sidebar';
import SparklineChart   from './components/charts/SparklineChart';
import HoldingsCarousel from './components/HoldingsCarousel';

import {
  ResponsiveContainer,
  LineChart,
  Line,
  BarChart,
  Bar,
  Cell,
  PieChart,
  Pie,
  Tooltip,
  CartesianGrid,
  XAxis,
  YAxis,
} from 'recharts';

import { usePortfolio } from '../contexts/PortfolioContext';
import { clearCurrent } from '../auth/storage';
import { logout as logoutApi } from '../api/auth';

import {
  getSummary,
  getAllocation,
  getDailyPnl,
  getPortfolioValue,
} from '../api/dashboard';

import { getBalance }       from '../api/payments';
import { listTransactions } from '../api/transactions';

/* helpers */
const fmtMoney = n => '$' + (+n).toLocaleString();
const colored  = n => (+n >= 0 ? 'text-green-600' : 'text-red-600');

export default function DashboardPage () {
  const navigate = useNavigate();

  /* ───── summary / balance ───── */
  const [summary, setSummary] = useState(null);
  const [payBal,  setPayBal]  = useState(null);

  useEffect(() => { getSummary().then(setSummary).catch(console.error); }, []);
  useEffect(() => {
    const load = () => getBalance().then(setPayBal).catch(console.error);
    load(); const t = setInterval(load, 5000);
    return () => clearInterval(t);
  }, []);

  /* ───── charts ───── */
  const [pnlData, setPnl]   = useState([]);
  const [valData, setVal]   = useState([]);
  const [alloc,   setAlloc] = useState([]);

  useEffect(() => {
    getDailyPnl(90)
      .then(r => r.map(d => ({ date: d.date, pl: +d.pnl||0 })))
      .then(setPnl).catch(console.error);

    getPortfolioValue(90)
      .then(r => r.map(d => ({ date: d.date, value: +d.equity||0 })))
      .then(setVal).catch(console.error);

    getAllocation().then(setAlloc).catch(console.error);
  }, []);

  /* ───── transactions ───── */
  const [tx, setTx]        = useState(null);
  const [showAll, setShow] = useState(false);

  useEffect(() => {
    listTransactions(100, 1)
      .then(rows => rows.map(t => ({
        id: t.id,
        date: t.created_at,
        type: t.type,
        amount: +t.amount,
        note: t.comment || '',
      })))
      .then(setTx)
      .catch(console.error);
  }, []);

  const visibleTx = tx ? (showAll ? tx : tx.slice(0, 10)) : [];

  /* ───── modal enlarge spark ───── */
  const [modal, setModal] = useState({ open:false, title:'', data:[] });

  const { invested, strategies } = usePortfolio();

  /* logout */
  const handleLogout = async () => {
    try { await logoutApi(); } catch {}
    clearCurrent(); navigate('/', { replace:true });
  };

  if (!summary) return null;

  /* numbers */
  const totalEquity = +summary.total_equity || 0;
  const totalPnl    = +summary.total_pnl    || 0;
  const todayPnl    = +summary.today_pnl    || 0;

  /* ───── JSX ───── */
  return (
    <div className="layout">
      <Sidebar/>

      <main className="main-content">
        {/* Header */}
        <div className="top-bar">
          <span>Total&nbsp;Equity:&nbsp;<b>{fmtMoney(totalEquity)}</b></span>
          <span>Balance:&nbsp;<b>{payBal?fmtMoney(+payBal.balance):'…'}</b></span>
          <span>P/L&nbsp;Today:&nbsp;
            <b className={colored(todayPnl)}>
              {todayPnl>=0?'+':''}{fmtMoney(todayPnl)}
            </b>
          </span>
          <button className="btn danger" onClick={handleLogout}>Logout</button>
        </div>

        {/* KPI */}
        <section className="kpi-grid">
          <div className="kpi-card"><p>Total P/L</p>
            <h3 className={colored(totalPnl)}>
              {totalPnl>=0?'+':''}{fmtMoney(totalPnl)}</h3></div>
          <div className="kpi-card"><p>Today P/L</p>
            <h3 className={colored(todayPnl)}>
              {todayPnl>=0?'+':''}{fmtMoney(todayPnl)}</h3></div>
          <div className="kpi-card"><p>Balance</p>
            <h3>{payBal?fmtMoney(+payBal.balance):'…'}</h3></div>
          <div className="kpi-card"><p># Portfolios</p>
            <h3>{summary.num_portfolios ?? invested.length}</h3></div>
        </section>

        {/* Daily P/L + Allocation */}
        <section className="charts-row">

          {/* Daily P/L */}
          <div className="chart">
            <h2 className="chart-title">Daily P/L</h2>
            {pnlData.length ? (
              <ResponsiveContainer width="100%" height={240}>
                <BarChart data={pnlData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB"/>
                  <XAxis dataKey="date" stroke="#6B7280" tick={{fontSize:12}}
                         tickFormatter={d=>dayjs(d).format('DD MMM')}/>
                  <YAxis stroke="#6B7280" tick={{fontSize:12}}/>
                  <Tooltip formatter={v=>fmtMoney(v)}/>
                  <Bar dataKey="pl" barSize={10} isAnimationActive={false}>
                    {pnlData.map((d,i)=>(
                      <Cell key={i} fill={d.pl<0?'#EF4444':'#10B981'}/>
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ):<div className="no-data">No data</div>}
          </div>

          {/* Allocation */}
          <div className="chart">
            <h2 className="chart-title">Allocation</h2>
            {alloc.length ? (()=>{
              const data = alloc.map(a=>({name:a.name, share:+a.percentage}));
              return(
                <ResponsiveContainer width="100%" height={240}>
                  <PieChart>
                    <Tooltip formatter={(v,n)=>[`${(+v).toFixed(1)}%`,n]}/>
                    <Pie data={data} dataKey="share" nameKey="name"
                         innerRadius={60} outerRadius={100} labelLine={false}>
                      {data.map((_,i)=><Cell key={i} fill={i%2?'#10B981':'#6366F1'}/>)}
                    </Pie>
                  </PieChart>
                </ResponsiveContainer>
              );
            })():<div className="no-data">No data</div>}
          </div>
        </section>

        {/* Portfolio value */}
        <section className="chart-wide">
          <h2 className="chart-title">Portfolio Value vs Time</h2>
          {valData.length ? (
            <ResponsiveContainer width="100%" height={240}>
              <LineChart data={valData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB"/>
                <XAxis dataKey="date" stroke="#6B7280" tick={{fontSize:12}}
                       tickFormatter={d=>dayjs(d).format('DD MMM')}/>
                <YAxis stroke="#6B7280" tick={{fontSize:12}}/>
                <Tooltip formatter={v=>fmtMoney(v)}/>
                <Line type="monotone" dataKey="value" stroke="#2563EB"
                      strokeWidth={2} dot={false}/>
              </LineChart>
            </ResponsiveContainer>
          ):<div className="no-data">No data</div>}
        </section>

        {/* Holdings & Transactions (vertical) */}
        <section className="bottom-col">

          {/* Holdings */}
          <div className="portfolios-block">
            <h2 className="section-title">Portfolio Holdings</h2>
            <HoldingsCarousel
              data={alloc.map(a=>({
                id:a.id,name:a.name,percentage:a.percentage,
                spark:(strategies.find(s=>s.id===a.id)||{}).sparkline_gain,
              }))}
              onShow={(title,data)=>setModal({open:true,title,data})}
            />
          </div>

          {/* Transactions */}
          <div className="tx-block">
            <h2 className="section-title">Latest Transactions</h2>
            {tx ? tx.length ? (
              <>
                <ul className="tx-list">
                  {visibleTx.map(t=>(
                    <li key={t.id}>
                      <span>{dayjs(t.date).format('DD MMM')}</span>
                      <span>{t.type}</span>
                      <span className={colored(t.amount)}>
                        {(t.amount>=0?'+':'')+fmtMoney(Math.abs(t.amount))}
                      </span>
                      <span className="tx-note">{t.note}</span>
                    </li>
                  ))}
                </ul>
                {tx.length>10&&(
                  <button className="show-btn" onClick={()=>setShow(!showAll)}>
                    {showAll?'Hide':'More'}
                  </button>
                )}
              </>
            ):<div className="no-data">No data</div>
             :<div className="no-data">Loading…</div>}
          </div>
        </section>

        {/* Modal with big spark */}
        {modal.open&&(
          <div className="modal-overlay" onClick={()=>setModal({open:false})}>
            <div className="modal-box" onClick={e=>e.stopPropagation()}>
              <div className="modal-header">
                <h2>{modal.title}</h2>
                <button className="modal-close" onClick={()=>setModal({open:false})}>✕</button>
              </div>
              <div className="modal-body">
                <ResponsiveContainer width="100%" height="100%">
                  <SparklineChart data={modal.data} full/>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}

      </main>
    </div>
  );
}
