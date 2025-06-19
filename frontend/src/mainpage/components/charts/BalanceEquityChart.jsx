import React from "react";
import dayjs from "dayjs";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
} from "recharts";

const fmt = (d) => dayjs(d).format("DD MMM");

export default function BalanceEquityChart({ data = [] }) {
  if (!data.length) return null;

  /* авто-диапазон: +5 % сверху, -10 % снизу */
  const vals = data.flatMap((d) => [+d.balance, +d.equity]);
  const ymin = Math.min(...vals) * 0.9;
  const ymax = Math.max(...vals) * 1.05;

  return (
    <ResponsiveContainer width="100%" height="100%">
      <AreaChart data={data} margin={{ top: 24, right: 20, left: 0, bottom: 6 }}>
        <CartesianGrid stroke="#E5E7EB" strokeDasharray="3 3" />

        <XAxis dataKey="date" tickFormatter={fmt}
               tick={{ fontSize: 11 }} stroke="#6B7280"
               tickLine={false} axisLine={{ stroke: "#D1D5DB" }}
               interval="preserveStartEnd" />

        {/* ←-- авто диапазон */}
        <YAxis domain={[ymin, ymax]}
               tick={{ fontSize: 11 }} stroke="#6B7280"
               tickLine={false} axisLine={{ stroke: "#D1D5DB" }} />

        <Tooltip
          formatter={(v) => (+v).toLocaleString()}
          labelFormatter={(v) => fmt(v)}
          contentStyle={{
            background: "#fff",
            border: "1px solid #E5E7EB",
            borderRadius: 4,
            fontSize: 12,
          }}
        />

        <Legend verticalAlign="top" height={20} iconType="circle"
                wrapperStyle={{ fontSize: 12 }} />

        <Area type="monotone" dataKey="balance" name="Balance"
              stroke="#10B981" fill="#d1fae5" strokeWidth={2} />
        <Area type="monotone" dataKey="equity"  name="Equity"
              stroke="#3b82f6" fill="#dbeafe" strokeWidth={2} />
      </AreaChart>
    </ResponsiveContainer>
  );
}
