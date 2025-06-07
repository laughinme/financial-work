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
 * @param {Array<{ date: string, gain_percent: string | number }>} data
 */
export default function SparklineChart({ data }) {
  if (!data || data.length === 0) return null;

  
  const values = data.map((d) => parseFloat(d.gain_percent));
  const minValue = Math.min(...values);
  const maxValue = Math.max(...values);

  const last = values[values.length - 1];
  const strokeColor = last >= 0 ? '#34d399' : '#f87171';

  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart
        data={data}
        margin={{ top: 0, right: 0, left: 0, bottom: 0 }} 
      >

        <CartesianGrid
          horizontal={true}
          vertical={false}
          stroke="#ffffff33"     
          strokeDasharray="3 3"  
        />


        <XAxis
          dataKey="date"
          hide={true}
          axisLine={{ stroke: '#ffffff66', strokeWidth: 0.5 }}
          tick={false}
          tickLine={false}
        />
        <YAxis
          domain={[minValue, maxValue]}
          hide={true}
          axisLine={{ stroke: '#ffffff66', strokeWidth: 0.5 }}
          tick={false}
          tickLine={false}
        />

 
        <Tooltip
          isAnimationActive={false}
          labelFormatter={(v) => `Дата: ${v}`}
          formatter={(v) => [`${v}%`, 'Gain']}
          contentStyle={{ fontSize: 12 }}
        />

 
        <Line
          type="monotone"
          dataKey="gain_percent"
          stroke={strokeColor}
          strokeWidth={4}   /* более толстая линия */
          dot={false}       /* обычные точки скрыты */
          isAnimationActive={false}
          activeDot={{
            r: 4,
            strokeWidth: 2,
            stroke: strokeColor,
            fill: '#ffffff', /* белая точка при hover */
          }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
