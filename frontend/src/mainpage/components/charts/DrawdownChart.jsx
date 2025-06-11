import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts';

export default function DrawdownChart({ data }) {
  if (!data || data.length === 0) return null;

  return (
    <ResponsiveContainer width="100%" height={180}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />

        <XAxis
          dataKey="date"
          stroke="#6B7280"
          tick={{ fontSize: 11 }}
          tickLine={false}
        />

       
        <YAxis
          domain={['dataMin', 'dataMax']}
          stroke="#6B7280"
          tick={{ fontSize: 11 }}
          tickLine={false}
        />

        <Tooltip
          formatter={(v) => v + '%'}
          contentStyle={{
            background: '#fff',
            border: '1px solid #E5E7EB',
            borderRadius: 4,
            fontSize: 12,
          }}
        />

        <Bar dataKey="drawdown" fill="#EF4444" isAnimationActive={false} />
      </BarChart>
    </ResponsiveContainer>
  );
}
