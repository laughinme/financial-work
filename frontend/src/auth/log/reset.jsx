import React, { useState } from 'react';
import './log.css';

function Reset({ onBack }) {
  const [email, setEmail] = useState('');

  const handleReset = e => {
    e.preventDefault();
    alert(`Password reset link sent to ${email}`);
    onBack();
  };

  return (
    <form className="login-card" onSubmit={handleReset}>
      <h1 className="form-title">Recover</h1>

      <label className="field-label" htmlFor="email">Email Address</label>
      <div className="input-wrapper">
        <input
          id="email"
          type="email"
          placeholder="example@gmail.com"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
        />
      </div>

      <button type="submit" className="primary-btn">Reset Your Password</button>
    </form>
  );
}

export default Reset;
