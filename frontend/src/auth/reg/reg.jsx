import React, { useState } from 'react';
import { FiEye, FiEyeOff } from 'react-icons/fi';
import './Reg.css';

function Reg({ onSwitch }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPass, setShowPass] = useState(false);

  const handleSave = e => {
    e.preventDefault();
    localStorage.setItem('email', email);
    localStorage.setItem('password', password);
    alert('Сохранено в LocalStorage (для теста)');
  };

  return (
    <form className="login-card" onSubmit={handleSave}>
   
      <h1 className="form-title">Registration</h1>


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


      <label className="field-label" htmlFor="password">Password</label>
      <div className="input-wrapper password">
        <input
          id="password"
          type={showPass ? 'text' : 'password'}
          placeholder="••••••••••"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
          minLength={6}
        />
        <button
          type="button"
          className="toggle-pass"
          onClick={() => setShowPass(!showPass)}
          aria-label={showPass ? 'Hide password' : 'Show password'}
        >
          {showPass ? <FiEyeOff /> : <FiEye />}
        </button>
      </div>


      <button type="submit" className="primary-btn">Create an account</button>

      <p className="footer">
        Already have an account?
        <button type="button" className="link" onClick={onSwitch}> Log&nbsp;in</button>
      </p>
    </form>
  );
}

export default Reg;
