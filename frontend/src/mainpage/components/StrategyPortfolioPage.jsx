
   import React, { useEffect, useState } from 'react';
   import { useParams, useNavigate }     from 'react-router-dom';
   import { FiZap, FiChevronLeft }       from 'react-icons/fi';
   import dayjs                          from 'dayjs';
   import { marked }                     from 'marked';
   
   import Sidebar            from './Sidebar';
   import BalanceEquityChart from './charts/BalanceEquityChart';
   import SparklineChart     from './charts/SparklineChart';
   
   import {
     ResponsiveContainer,
     BarChart,
     Bar,
     Cell,
     CartesianGrid,
     XAxis,
     YAxis,
     Tooltip,
   } from 'recharts';
   
   import './strategyPortfolio.css';
   import { usePortfolio }   from '../../contexts/PortfolioContext';
   
   const CHART_HEIGHT = 240;
   const fmt = (n,d=2)=>Number(n).toLocaleString('en-US',
     {minimumFractionDigits:d,maximumFractionDigits:d});
   
   export default function StrategyPortfolioPage () {
     const { id }        = useParams();
     const navigate      = useNavigate();
     const {
       strategies, toggleInvest, getHistory, getHolding,
     } = usePortfolio();
   
     const [history,setHistory] = useState(null);
     const [holding,setHolding] = useState(null);
   
     const data = strategies.find(s=>s.id.toString()===id);
     if (!data) return <div style={{padding:32}}>Loading…</div>;
   
     useEffect(()=>{
       getHistory(id,90).then(setHistory).catch(console.error);
       getHolding(id)   .then(setHolding).catch(()=>setHolding(null));
     },[id,getHistory,getHolding]);
   
     /* графики */
     const balanceData  = history?.balance_equity || [];
     const rawDrawdown  = history?.drawdown        || [];
     const plData       = history?.sparkline?.map(d=>(
       {date:d.date,gain_percent:d.gain_percent})) || [];
   
    
     const step   = rawDrawdown.length>60 ? Math.ceil(rawDrawdown.length/60) : 1;
     const drawdownData = rawDrawdown.filter((_,i)=>i%step===0);
   
     const riskIcons = Array.from({length:data.risk},(_,i)=><FiZap key={i} size={14}/>);
     const NoData = ()=><div className="nodata">No&nbsp;data</div>;
   
     return (
       <div className="layout">
         <Sidebar/>
   
         <main className="strat-page">
           {/* ─ Header ─ */}
           <header className="strat-header">
             <button className="back-btn" onClick={()=>navigate(-1)}>
               <FiChevronLeft size={18}/> Back
             </button>
   
             <div className="title-block">
               <h1 className="strat-title">
                 {data.name} ({data.currency})
               </h1>
               <span className="risk-pill">{riskIcons}</span>
               <span className="broker">Broker: {data.broker}</span>
             </div>
   
             <p className="subtitle">{data.description}</p>
   
             <button
               className={`action-btn${data.invested?' invested':''}`}
               onClick={()=>toggleInvest(data.id)}
             >
               {data.invested?'Invested':'Invest'}
             </button>
           </header>
   
           {/* ─ KPI ─ */}
           <section className="kpi-grid">
             <div className="kpi-card"><p className="kpi-label">Equity</p>
               <h3>{fmt(data.equity,0)}</h3></div>
             <div className="kpi-card"><p className="kpi-label">NAV price</p>
               <h3>{fmt(data.nav_price,4)}</h3></div>
             <div className="kpi-card"><p className="kpi-label">Gain %</p>
               <h3 className={data.gain_percent>=0?'pos':'neg'}>
                 {data.gain_percent>=0?'+':''}{data.gain_percent}%</h3></div>
             <div className="kpi-card"><p className="kpi-label">Max DD</p>
               <h3 className="neg">{fmt(data.drawdown,1)}%</h3></div>
           </section>
   
           {/* ─ Charts row ─ */}
           <section className="chart-row">
             {/* Balance / Equity */}
             <div className="chart-box">
               <h3 className="chart-title">Balance / Equity</h3>
               <div className="chart-wrapper" style={{height:CHART_HEIGHT}}>
                 {balanceData.length
                   ? <BalanceEquityChart data={balanceData}/>
                   : <NoData/>}
               </div>
             </div>
   
             {/* Drawdown   ─────────── */}
             <div className="chart-box">
               <h3 className="chart-title">Drawdown</h3>
               <div className="chart-wrapper" style={{height:CHART_HEIGHT}}>
                 {drawdownData.length ? (
                   <ResponsiveContainer width="100%" height="100%">
                     <BarChart data={drawdownData}
                               margin={{top:10,right:20,left:0,bottom:6}}>
                       <CartesianGrid stroke="#E5E7EB" strokeDasharray="3 3"/>
                       <XAxis dataKey="date"
                              tickFormatter={d=>dayjs(d).format('DD MMM')}
                              tick={{fontSize:11}} stroke="#6B7280"
                              tickLine={false} axisLine={{stroke:'#D1D5DB'}}
                              interval="preserveStartEnd"/>
                       <YAxis domain={['dataMin','dataMax']}
                              tick={{fontSize:11}} stroke="#6B7280"
                              tickLine={false} axisLine={{stroke:'#D1D5DB'}}/>
                       <Tooltip formatter={v=>`${v}%`}
                                labelFormatter={d=>`Date: ${dayjs(d).format('DD MMM')}`}/>
                       <Bar dataKey="drawdown" barSize={4} barCategoryGap={1}
                            isAnimationActive={false}>
                         {drawdownData.map((_,i)=><Cell key={i} fill="#EF4444"/>)}
                       </Bar>
                     </BarChart>
                   </ResponsiveContainer>
                 ) : <NoData/>}
               </div>
             </div>
   
             {/* Daily P/L */}
             <div className="chart-box">
               <h3 className="chart-title">Daily&nbsp;P/L</h3>
               <div className="chart-wrapper" style={{height:CHART_HEIGHT}}>
                 {plData.length ? <SparklineChart data={plData} full/> : <NoData/>}
               </div>
             </div>
           </section>
   
           {/* ─ Personal block ─ */}
           {data.invested && holding && (
             <section className="personal">
               <h3>Your position</h3>
               <p>You own <b>{fmt(holding.units,3)} u</b></p>
               <p>Current value <b>${fmt(holding.current_value)}</b></p>
               <p className="pl-line">Net P/L&nbsp;<b>{fmt(holding.pnl)}</b></p>
               <div className="btn-row">
                 <button className="btn-alt" onClick={()=>toggleInvest(data.id)}>
                   Withdraw
                 </button>
               </div>
             </section>
           )}
   
           {/* ─ Description ─ */}
           <section className="description">
             <h3>Strategy description</h3>
             <div className="md"
                  dangerouslySetInnerHTML={{__html:marked.parse(data.description||'')}}/>
           </section>
         </main>
       </div>
     );
   }
   