import React, { useEffect, useState } from "react";
import "./moneyModal.css";

export default function MoneyModal({
  open,
  title = "Enter amount",
  label = "Amount",
  navPrice = null,
  mode = "invest",        
  onClose = () => {},
  onSubmit = () => {},
}) {
  const [val, setVal] = useState("");

  
  useEffect(() => {
    if (open) setVal("");
  }, [open]);

  if (!open) return null;

 
  let hint = null;
  const num = Number(val) || 0;

  if (navPrice && num > 0) {
    if (mode === "invest") {
      const units = num / navPrice;
      hint = (
        <>
          <div>{`$${num.toFixed(2)} ≈ ${units.toFixed(6)} u`}</div>
          <div>{`1 u = $${navPrice}`}</div>
        </>
      );
    } else {
      const usd = navPrice * num;
      hint = (
        <>
          <div>{`${num} u ≈ $${usd.toFixed(2)}`}</div>
          <div>{`1 u = $${navPrice}`}</div>
        </>
      );
    }
  }


  const handleOk = async () => {
    const n = Number(val);
    if (!n || n <= 0) {
      alert("Enter a positive number");
      return;
    }
    try {
      await onSubmit(n);
      onClose();
    } catch (e) {
      alert(e?.message || "Request failed");
    }
  };


  return (
    <div className="mm-overlay" onClick={onClose}>
      <div className="mm-box" onClick={(e) => e.stopPropagation()}>
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

        {hint && <div className="mm-hint">{hint}</div>}

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
