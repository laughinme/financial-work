import React, { useEffect } from 'react';
import './chartModal.css';


export default function ChartModal({ open, title, onClose, children }) {
 
  useEffect(() => {
    const esc = (e) => e.key === 'Escape' && onClose();
    if (open) window.addEventListener('keydown', esc);
    return () => window.removeEventListener('keydown', esc);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="cm-overlay" onClick={onClose}>
      <div className="cm-box" onClick={(e) => e.stopPropagation()}>
        <header className="cm-head">
          <h2>{title}</h2>
          <button className="cm-close" onClick={onClose}>✕</button>
        </header>
        <div className="cm-body">
          {children}
        </div>
      </div>
    </div>
  );
}
