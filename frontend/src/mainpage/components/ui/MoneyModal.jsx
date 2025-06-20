// src/ui/MoneyModal.jsx
import React, { useState } from "react";
import "./moneyModal.css";

/**
 * Универсальная модалка для ввода числа (USD, units и т.п.)
 *
 * props:
 *  open      – boolean
 *  title     – string         (заголовок)
 *  label     – string         (placeholder для инпута)
 *  onClose   – ()=>void       (закрыть без действия)
 *  onSubmit  – (value:number)=>Promise<void>|void
 */
export default function MoneyModal({
  open,
  title = "Enter amount",
  label = "Amount (USD)",
  onClose = () => {},
  onSubmit = () => {},
}) {
  const [val, setVal] = useState("");

  if (!open) return null;

  const handleOk = async () => {
    const num = Number(val);
    if (!num || num <= 0) {
      alert("Enter a positive number");
      return;
    }
    try {
      await onSubmit(num);
      onClose();
    } catch (e) {
      alert(e?.message || "Request failed");
    }
  };

  return (
    <div className="mm-overlay" onClick={onClose}>
      <div
        className="mm-box"
        onClick={(e) => e.stopPropagation()} // не закрывать при клике по модалке
      >
        <h2 className="mm-title">{title}</h2>

        <input
          type="number"
          className="mm-input"
          placeholder={label}
          value={val}
          onChange={(e) => setVal(e.target.value)}
          min={0}
          step="any"
        />

        <div className="mm-actions">
          <button className="mm-btn" onClick={onClose}>
            Cancel
          </button>
          <button className="mm-btn primary" onClick={handleOk}>
            OK
          </button>
        </div>
      </div>
    </div>
  );
}
