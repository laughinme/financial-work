// frontend/src/mock/api.js
const delay = (ms = 200) => new Promise(r => setTimeout(r, ms));

/* ───── 0.  GET /dashboard/summary ───── */
export async function fetchSummary() {
  await delay();
  // Now we have two strategies: id:3 and id:4
  // Let their equity be 25,000 + 18,000 = 43,000
  return {
    total_equity   : 43000,    // sum of equity of both strategies
    today_pl       : 18.44,
    total_pnl      : 5000,     // just a demo value
    num_portfolios : 2,        // now there are 2 portfolios
    last_sync      : '2025-06-05T10:34:21Z',
  };
}

/* ───── 1.  GET /dashboard/charts ───── */
export async function fetchCharts() {
  await delay();
  return {
    // Demo data — unchanged
    portfolio_value: [
      { date:'2025-06-01', value: 12000 },
      { date:'2025-06-02', value: 22000 },
      { date:'2025-06-03', value: 30000 },
      { date:'2025-06-04', value: 43000 },
    ],
    daily_pl: [
      { date:'2025-06-01', pl:  500 },
      { date:'2025-06-02', pl: 1000 },
      { date:'2025-06-03', pl:  800 },
      { date:'2025-06-04', pl: 1300 },
    ],
    allocation: [
      { name:'Quantum Risk', value: 25000, share_percent: 58.1 },
      { name:'Green Energy',  value: 18000, share_percent: 41.9 },
    ],
  };
}

/* ───── 2.  GET /dashboard/portfolios ───── */
export async function fetchPortfolios() {
  await delay();
  return [
    {
      id        : 3,
      name      : 'Quantum Risk',
      value     : 25000,
      gain_pct  : 30,
      sparkline : [10000,12500,15000,18000,20000,22000,23000,24000,24500,25000],
    },
    {
      id        : 4,
      name      : 'Green Energy',
      value     : 18000,
      gain_pct  : 18,
      sparkline : [10000,11000,12500,14000,15000,15500,16000,16800,17400,18000],
    },
  ];
}

/* ───── 3.  GET /dashboard/transactions ───── */
export async function fetchTx() {
  await delay();
  return [
    { date:'2025-06-04', type:'Deposit', amount:  500,   note:'YooKassa #119' },
    { date:'2025-06-03', type:'PNL',     amount: 1300,  note:'Daily reval'       },
    { date:'2025-06-02', type:'Invest',  amount: -250,  note:'Quantum Risk'     },
    { date:'2025-06-01', type:'Invest',  amount: -150,  note:'Green Energy'     },
  ];
}
