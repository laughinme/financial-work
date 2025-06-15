import React from "react";
import dayjs from "dayjs";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

const formatDate = (d) => dayjs(d).format("DD MMM");

export default function BalanceEquityChart({ data }) {
  if (!Array.isArray(data) || data.length === 0) return null;

  return (
    <ResponsiveContainer width="100%" height="100%">
      <AreaChart data={data} margin={{ top: 24, right: 20, left: 0, bottom: 6 }}>
     
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
          tick={{ fontSize: 11 }}
          stroke="#6B7280"
          tickLine={false}
          axisLine={{ stroke: "#D1D5DB" }}
          domain={[0, "auto"]}
        />

        <Tooltip
          formatter={(v) => (+v).toLocaleString()}
          labelFormatter={(v) => `Дата: ${formatDate(v)}`}
          contentStyle={{
            background: "#ffffff",
            border: "1px solid #E5E7EB",
            borderRadius: 4,
            fontSize: 12,
          }}
        />

  
        <Legend
          verticalAlign="top"
          height={20}
          iconType="circle"
          wrapperStyle={{ fontSize: 12 }}
        />


        <Area
          type="monotone"
          dataKey="balance"
          name="Balance"
          stroke="#10b981"
          fill="#d1fae5"
          strokeWidth={2}
          isAnimationActive={true}
        />
        <Area
          type="monotone"
          dataKey="equity"
          name="Equity"
          stroke="#3b82f6"
          fill="#dbeafe"
          strokeWidth={2}
          isAnimationActive={true}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
