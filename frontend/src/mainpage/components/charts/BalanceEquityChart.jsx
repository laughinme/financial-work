
import React from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function BalanceEquityChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={220}>
      <AreaChart data={data}>
        <XAxis dataKey="date" tick={{ fontSize: 11 }} />
        <YAxis tick={{ fontSize: 11 }} />
        <Tooltip />
        <Legend />
        <Area
          type="monotone"
          dataKey="balance"
          name="Balance"
          stroke="#10b981"
          fill="#d1fae5"
          strokeWidth={2}
        />
        <Area
          type="monotone"
          dataKey="equity"
          name="Equity"
          stroke="#3b82f6"
          fill="#dbeafe"
          strokeWidth={2}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
