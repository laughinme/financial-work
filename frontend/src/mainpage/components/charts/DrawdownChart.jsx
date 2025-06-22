import React from "react";
import dayjs from "dayjs";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell,
} from "recharts";

const formatDate = (d) => dayjs(d).format("DD MMM");

export default function DrawdownChart({ data }) {
  if (!Array.isArray(data) || data.length === 0) return null;

  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 6 }}>
        <CartesianGrid stroke="#E5E7EB" strokeDasharray="3 3" />

        <XAxis
          dataKey="date"
          tickFormatter={formatDate}
          tick={{ fontSize: 11 }}
          stroke="#6B7280"
          tickLine={false}
          axisLine={{ stroke: "#D1D5DB" }}
          interval="preserveStartEnd"
        />
        <YAxis
          domain={["dataMin", "dataMax"]}
          tick={{ fontSize: 11 }}
          stroke="#6B7280"
          tickLine={false}
          axisLine={{ stroke: "#D1D5DB" }}
        />

        <Tooltip
          formatter={(v) => v + "%"}
          labelFormatter={(v) => `Date: ${formatDate(v)}`}
          contentStyle={{
            background: "#ffffff",
            border: "1px solid #E5E7EB",
            borderRadius: 4,
            fontSize: 12,
          }}
        />

        <Bar dataKey="drawdown" isAnimationActive={true}>
          {data.map((_, i) => (
            <Cell key={i} fill="#EF4444" />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
