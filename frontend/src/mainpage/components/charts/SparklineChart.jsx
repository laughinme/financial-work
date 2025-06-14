// src/mainpage/components/charts/SparklineChart.jsx
import React from "react";
import dayjs from "dayjs";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

/* удобный формат для дат на оси X */
const formatDate = (d) => dayjs(d).format("DD MMM");

/**
 * Мини-график / полноразмерный график.
 *
 * @param {{date:string,gain_percent:number|string}[]} data
 * @param {boolean} full – если true → оси, сетка, анимация
 */
export default function SparklineChart({ data, full = false }) {
  if (!Array.isArray(data) || data.length === 0) return null;

  const values      = data.map((d) => +d.gain_percent);
  const minValue    = Math.min(...values);
  const maxValue    = Math.max(...values);
  const lastValue   = values[values.length - 1];
  const strokeColor = lastValue >= 0 ? "#34d399" : "#f87171";

  const margin = full
    ? { top: 10, right: 20, left: -10, bottom: 6 }
    : { top: 0, right: 0, left: 0, bottom: 0 };

  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={data} margin={margin}>
        {full && (
          <CartesianGrid stroke="#E5E7EB" strokeDasharray="3 3" />
        )}

        <XAxis
          dataKey="date"
          hide={!full}
          tick={{ fontSize: 11 }}
          stroke="#6B7280"
          tickLine={false}
          axisLine={{ stroke: "#D1D5DB" }}
          tickFormatter={formatDate}   /* ← здесь форматируем */
          interval="preserveStartEnd"  /* не обрезаем крайние подписи */
        />

        <YAxis
          domain={[minValue, maxValue]}
          hide={!full}
          tick={{ fontSize: 11 }}
          stroke="#6B7280"
          tickLine={false}
          axisLine={{ stroke: "#D1D5DB" }}
        />

        <Tooltip
          isAnimationActive={false}
          labelFormatter={(v) => `Дата: ${formatDate(v)}`}
          formatter={(v) => [`${v}%`, "Gain"]}
          contentStyle={{
            background: "#ffffff",
            border: "1px solid #E5E7EB",
            borderRadius: 4,
            fontSize: 12,
          }}
          itemStyle={{ color: "#111827" }}
          labelStyle={{ color: "#111827" }}
        />

        <Line
          type="monotone"
          dataKey="gain_percent"
          stroke={strokeColor}
          strokeWidth={full ? 3 : 2}
          dot={false}
          isAnimationActive={full}
          animationDuration={800}
          activeDot={{
            r: 4,
            strokeWidth: 2,
            stroke: strokeColor,
            fill: "#ffffff",
          }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
