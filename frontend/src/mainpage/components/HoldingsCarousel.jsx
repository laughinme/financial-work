import React from 'react';
import { Link } from 'react-router-dom';
import SparklineChart from './charts/SparklineChart';
import './holdingsCarousel.css';

/**
 * @param {{data:{id:number,name:string,percentage:number,spark?:object[]}[], onShow:(name,data)=>void}} props
 */
export default function HoldingsCarousel({ data = [], onShow = () => {} }) {
  if (!data.length) return null;

  return (
    <div className="holdings-scroll">
      {data.map((h) => (
        <Link
          to={`/portfolio/${h.id}`}
          key={h.id}
          className="holding-card"
        >
          <div
            className="spark-box"
            onClick={(e) => {          // отдельный клик по графику → modal
              e.preventDefault();      // не переходить по ссылке
              onShow(h.name, h.spark || []);
            }}
          >
            <SparklineChart data={h.spark || []}/>
          </div>

          <p className="h-title">{h.name}</p>
          <p className="h-share">{(+h.percentage).toFixed(1)}%</p>
        </Link>
      ))}
    </div>
  );
}
