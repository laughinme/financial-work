
import React, { useMemo } from 'react';
import dayjs from 'dayjs';
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

const fmtNum = (v) => {
  if (v === 0) return '0';
  if (Math.abs(v) >= 1_000_000) return (v / 1_000_000).toFixed(1) + ' m';
  if (Math.abs(v) >= 1_000)     return (v / 1_000).toFixed(1) + ' k';
  return v.toString();
};

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;

  return (
    <div
      style={{
        background   : '#fff',
        border       : '1px solid #e5e7eb',
        borderRadius : 10,
        padding      : '0.75rem 1rem',
        fontSize     : 16,
        boxShadow    : '0 4px 12px rgba(0,0,0,.08)',
        lineHeight   : 1.35,
      }}
    >
      <div style={{ marginBottom: 6, fontWeight: 600 }}>
        {dayjs(label).format('DD MMM YYYY')}
      </div>
      {payload
        .filter((p) => p.dataKey !== 'equityArea')
        .map((p) => (
          <div key={p.dataKey} style={{ color: p.color, fontWeight: 600 }}>
            {p.name}&nbsp;:&nbsp;
            {(+p.value).toLocaleString('en-US')}
          </div>
        ))}
    </div>
  );
};

export default function BalanceEquityChart({ data = [], full = false }) {
  const prepared = useMemo(
    () =>
      data.map((d) => {
        const equityVal = +d.equity;
        return {
          ...d,
          ts         : new Date(d.date).getTime(),
          balance    : +d.balance,
          equity     : equityVal,
          equityArea : equityVal,
        };
      }),
    [data]
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
          tickFormatter={(ts) =>
            dayjs(ts).format(full ? 'DD MMM YY' : 'DD MMM')
          }
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
          tickMargin={12}
        />

        <Tooltip content={<CustomTooltip />} />

        <Legend verticalAlign="top" height={28} iconSize={12} />

        <Area
          type="monotone"
          dataKey="equityArea"
          stroke="none"
          fill="#2563EB"
          fillOpacity={0.08}
          name=""
          legendType="none"
          isAnimationActive={true}
          animationDuration={800}
        />

        <Line
          type="monotone"
          dataKey="balance"
          stroke="#059669"
          strokeWidth={2}
          dot={false}
          name="Balance"
          isAnimationActive={true}
          animationDuration={800}
        />
        <Line
          type="monotone"
          dataKey="equity"
          stroke="#2563EB"
          strokeWidth={2}
          dot={false}
          name="Equity"
          isAnimationActive={true}
          animationDuration={800}
        />
      </ComposedChart>
    </ResponsiveContainer>
  );
}
