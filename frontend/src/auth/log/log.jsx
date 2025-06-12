import React, { useState, useEffect } from 'react';
import { FiEye, FiEyeOff } from 'react-icons/fi';
import '../log/log.css';

import { findUser, setCurrent } from '../storage';

export default function Log({ onSwitch, onReset }) {
  const [email, setEmail]   = useState('');
  const [password, setPass] = useState('');
  const [showPass, setShow] = useState(false);

  /* Telegram-виджет — без изменений */
  useEffect(() => {
    window.onTelegramAuth = user => {
      alert(
        `Logged in as ${user.first_name} ${user.last_name} (${user.id})`,
      );
    };
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://telegram.org/js/telegram-widget.js?22';
    script.setAttribute('data-telegram-login', 'niperybot');
    script.setAttribute('data-size', 'large');
    script.setAttribute('data-onauth', 'onTelegramAuth(user)');
    script.setAttribute('data-request-access', 'write');

    const container = document.getElementById('telegram-login-button');
    if (container) container.appendChild(script);
    return () => { if (container) container.innerHTML = ''; };
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();

    const user = findUser(email);
    if (!user || user.password !== password) {
      alert('Wrong email / password');
      return;
    }

    setCurrent(email);                 // ← логиним
    window.location.href = '/main.html';
  };

  return (
    <form className="login-card" onSubmit={handleSubmit}>
      <h1 className="form-title">Log in</h1>

      <label className="field-label" htmlFor="email">Email Address</label>
      <div className="input-wrapper">
        <input
          id="email"
          type="email"
          placeholder="example@gmail.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
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
          onChange={(e) => setPass(e.target.value)}
          required
        />
        <button
          type="button"
          className="toggle-pass"
          onClick={() => setShow(!showPass)}
          aria-label={showPass ? 'Hide password' : 'Show password'}
        >
          {showPass ? <FiEyeOff /> : <FiEye />}
        </button>
      </div>

      <div className="options-row">
        <label className="remember">
          <input type="checkbox" /> <span>Remember me</span>
        </label>
        <button type="button" className="reset" onClick={onReset}>
          Reset Password?
        </button>
      </div>

      <button type="submit" className="primary-btn">Log in</button>

      <div
        id="telegram-login-button"
        style={{ display: 'flex', justifyContent: 'center', margin: '20px 0' }}
      />

      <p className="footer">
        Don’t have account yet?
        <button type="button" className="link" onClick={onSwitch}>
          New&nbsp;Account
        </button>
      </p>
    </form>
  );
}
