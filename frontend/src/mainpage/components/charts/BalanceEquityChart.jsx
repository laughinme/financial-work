
import React, { useMemo } from 'react';
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  Area,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
} from 'recharts';
import dayjs from 'dayjs';


const fmtNum = (v) => {
  if (v === 0) return '0';
  if (Math.abs(v) >= 1_000_000) return (v / 1_000_000).toFixed(1) + ' m';
  if (Math.abs(v) >= 1_000)     return (v / 1_000).toFixed(1) + ' k';
  return v.toString();
};

export default function BalanceEquityChart({ data, full = false }) {
 
  const prepared = useMemo(
    () => data.map((d) => ({
      ...d,
      ts: new Date(d.date).getTime(),
      balance: +d.balance,
      equity : +d.equity,
    })),
    [data],
  );

  if (!prepared.length) return null;

  return (
    <ResponsiveContainer width="100%" height="100%">
      <ComposedChart
        data={prepared}
        margin={{ top: 16, right: 24, bottom: 0, left: 64 }}
      >
        <CartesianGrid stroke="#E5E7EB" strokeDasharray="3 3" />

        <XAxis
          dataKey="ts"
          type="number"
          domain={['dataMin', 'dataMax']}
          tickFormatter={(ts) => dayjs(ts).format(full ? 'DD MMM YY' : 'DD MMM')}
          tick={{ fontSize: 12 }}
          tickLine={false}
          axisLine={{ stroke: '#D1D5DB' }}
          interval="preserveStartEnd"
          minTickGap={20}
        />

        <YAxis
          tickFormatter={fmtNum}
          tickLine={false}
          axisLine={{ stroke: '#D1D5DB' }}
          tick={{ fontSize: 12 }}
          tickMargin={10}
        />

        <Tooltip
          formatter={(v) => (+v).toLocaleString('en-US')}
          labelFormatter={(ts) => dayjs(ts).format('DD MMM YYYY')}
        />

        <Legend verticalAlign="top" height={24} iconSize={10} />

        {/* Заливка под Equity */}
        <Area
          type="monotone"
          dataKey="equity"
          stroke="none"
          fill="#2563EB"
          fillOpacity={0.08}
        />

        {/* Линии */}
        <Line
          type="monotone"
          dataKey="balance"
          stroke="#059669"
          strokeWidth={2}
          dot={false}
          name="Balance"
        />
        <Line
          type="monotone"
          dataKey="equity"
          stroke="#2563EB"
          strokeWidth={2}
          dot={false}
          name="Equity"
        />
      </ComposedChart>
    </ResponsiveContainer>
  );
}
