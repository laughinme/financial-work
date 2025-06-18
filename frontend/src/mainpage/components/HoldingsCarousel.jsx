import React from 'react';
import SparklineChart from './charts/SparklineChart';
import './holdingsCarousel.css';

/**
 * Горизонтальная карусель портфелей пользователя.
 * @param {{data:{id:number,name:string,percentage:number,spark?:object[]}[]}} props
 */
export default function HoldingsCarousel({ data = [] }) {
  if (!data.length) return null;

  return (
    <div className="holdings-scroll">
      {data.map((h) => (
        <div key={h.id} className="holding-card">
          <div className="spark-box">
            <SparklineChart data={h.spark || []} />
          </div>
          <p className="h-title">{h.name}</p>
          <p className="h-share">{(+h.percentage).toFixed(1)}%</p>
        </div>
      ))}
    </div>
  );
}
