export const strategies = [
    {
      id: 3,
      name: 'Quantum Risk',
      currency: 'EUR',
      broker : 'RoboForex',
      risk   : 2,
      equity : 25_000,
      navPrice    : 2.5000,
      gainPercent : 30,
      maxDD       : -12.5,
  
      balanceEquity: [
        { date:'2025-05-25', balance:20000, equity:20000 },
        { date:'2025-05-30', balance:24000, equity:23800 },
        { date:'2025-06-04', balance:25000, equity:24900 },
      ],
      drawdown: [
        { date:'2025-05-25', drawdown:  0 },
        { date:'2025-05-30', drawdown:-6 },
        { date:'2025-06-04', drawdown:-12.5 },
      ],
      dailyPL: [
        { date:'2025-06-02', pl: 200 },
        { date:'2025-06-03', pl:-100 },
        { date:'2025-06-04', pl: 300 },
      ],
      allocation: [
        { name:'Crypto', value:60 },
        { name:'FX',     value:40 },
      ],
      invested:false,      // personal block hidden until invested
      unitsOwned : 0,
      sharePct   : 0,
      currentValue:0,
      netPL:0,
      description:`
  ### Trading style
  • Quant models on FX & Crypto  
  • Target DD ≤ **15 %**  
  • Avg trades/day ≈ 8
  `,
    },
  
    {
      id: 4,
      name: 'Green Energy',
      currency: 'USD',
      broker : 'RoboForex',
      risk   : 2,
      equity : 18_000,
      navPrice    : 1.8000,
      gainPercent : 18,
      maxDD       : -5.1,
  
      balanceEquity: [
        { date:'2025-05-27', balance:12000, equity:12000 },
        { date:'2025-06-01', balance:16000, equity:15900 },
        { date:'2025-06-05', balance:18000, equity:17950 },
      ],
      drawdown: [
        { date:'2025-05-27', drawdown:0 },
        { date:'2025-06-01', drawdown:-3 },
        { date:'2025-06-05', drawdown:-5.1 },
      ],
      dailyPL: [
        { date:'2025-06-03', pl:  90 },
        { date:'2025-06-04', pl: 110 },
        { date:'2025-06-05', pl: 130 },
      ],
      allocation:[
        { name:'Solar', value:70 },
        { name:'Wind',  value:30 },
      ],
      invested:false,
      unitsOwned :0,
      sharePct   :0,
      currentValue:0,
      netPL:0,
      description:`
  ### Trading style
  • Long-only green-energy stocks  
  • Target DD ≤ **7 %**  
  • Avg trades/day ≈ 3
  `,
    },
  ];
  