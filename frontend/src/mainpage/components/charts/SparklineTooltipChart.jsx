
import React from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts';

/**
 * @param {Array<{ date: string, gain_percent: string|number }>} data
 */
export default function SparklineTooltipChart({ data }) {
  if (!Array.isArray(data) || data.length === 0) return null;

  const values = data.map((d) => parseFloat(d.gain_percent));
  const minValue = Math.min(...values);
  const maxValue = Math.max(...values);

  const last = values[values.length - 1];
  const strokeColor = last >= 0 ? '#34D399' : '#F87171';

  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={data} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
        <CartesianGrid stroke="#E5E7EB" strokeDasharray="3 3" />

        <XAxis
          dataKey="date"
          axisLine={{ stroke: '#D1D5DB', strokeWidth: 1 }}
          tick={false}
          tickLine={false}
        />

        <YAxis
          domain={[minValue, maxValue]}
          axisLine={{ stroke: '#D1D5DB', strokeWidth: 1 }}
          tick={false}
          tickLine={false}
        />

        <Tooltip
          isAnimationActive={false}
          labelFormatter={(v) => `Дата: ${v}`}
          formatter={(v) => [`${v}%`, 'Gain']}
          contentStyle={{
            backgroundColor: '#ffffff',
            border: '1px solid #E5E7EB',
            borderRadius: 4,
            fontSize: 12,
          }}
          labelStyle={{ color: '#000000' }}
          itemStyle={{ color: '#000000' }}
        />

        <Line
          type="monotone"
          dataKey="gain_percent"
          stroke={strokeColor}
          strokeWidth={2}
          dot={false}
          isAnimationActive={false}
          activeDot={{
            r: 3,
            strokeWidth: 1,
            stroke: strokeColor,
            fill: '#ffffff',
          }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
