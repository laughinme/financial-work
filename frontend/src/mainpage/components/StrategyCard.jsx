import React from 'react';
import { FiUsers, FiZap } from 'react-icons/fi';
import SparklineChart from './charts/SparklineChart';
import './strategyCard.css';


function fmt(n, digits = 0) {
  const num = parseFloat(n);
  if (isNaN(num)) return '—';

  return num.toFixed(digits).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
}


function riskIcons(risk) {
  const parsed = parseInt(risk, 10);
  let cnt = 3;
  if (!isNaN(parsed) && parsed >= 1 && parsed <= 3) {
    cnt = parsed;
  }
  return Array.from({ length: cnt }, (_, i) => <FiZap key={i} size={14} />);
}

export default function StrategyCard({ strategy }) {
  const {
    name,
    currency,
    risk,
    nav_price,
    balance,
    equity,
    drawdown,
    gain_percent,
    net_profit,
    deposit,
    holders,
    duration,
    sparkline_gain,

    color = '#1f1f23',
  } = strategy;


  const gainPct = (() => {
    const gp = parseFloat(gain_percent);
    return isNaN(gp) ? '—' : gp.toFixed(1);
  })();

 
  const netProfit = (() => {
    const np = parseFloat(net_profit);
    if (isNaN(np)) return '—';
    return np > 0 ? `+${np.toFixed(2)}` : np.toFixed(2);
  })();

 
  const drawdownPct = (() => {
    const dd = parseFloat(drawdown);
    return isNaN(dd) ? '—' : `${dd.toFixed(1)}%`;
  })();

  return (
    <article className="card-strategy">

      <div className="card-strategy__cover" style={{ background: color }}>
        <div className="cover-content">

          <div className="pill">
            {riskIcons(risk)}
            <span className="pill-text">Риск</span>
          </div>


          <div className="main-text">
            <p className="forecast">
              {gainPct === '—'
                ? 'Прогноз — в год'
                : `Прогноз ${gainPct}% в год`}
            </p>
            <p className="since">
              {netProfit === '—'
                ? '— за всё время'
                : `${netProfit}% за всё время`}
            </p>
          </div>


          <div className="sparkline-container">
            <SparklineChart data={(sparkline_gain || []).slice(0, 10)} />
          </div>


          <h2 className="cover-title">{name}</h2>
        </div>
      </div>


      <div className="card-strategy__body">
  
        <div className="metrics-row">
          <span>
            <span className="label">Мин.&nbsp;вклад</span>
            <b>
              {nav_price != null ? `${fmt(nav_price, 2)} ${currency}` : '—'}
            </b>
          </span>
          <span>
            <span className="label">Баланс</span>
            <b>{balance != null ? fmt(balance, 0) : '—'}</b>
          </span>
          <span>
            <span className="label">Equity</span>
            <b>{equity != null ? fmt(equity, 0) : '—'}</b>
          </span>
        </div>


        <div className="metrics-row">
          <span>
            <span className="label">Просадка</span>
            <b>{drawdownPct}</b>
          </span>
          <span>
            <span className="label">Депозитов</span>
            <b>{deposit != null ? fmt(deposit, 0) : '—'}</b>
          </span>
          <span>
            <span className="label">Холдеров</span>
            <b>{holders != null ? holders : '—'}</b>
          </span>
          <span>
            <span className="label">Дней&nbsp;в&nbsp;работе</span>
            <b>{duration != null ? duration : '—'}</b>
          </span>
        </div>

 
        <div className="card-bottom">
          <FiUsers size={16} />
          <span>256 пользователей</span>
        </div>
      </div>
    </article>
  );
}
