import React, { useState } from 'react';
import { FiEye, FiEyeOff } from 'react-icons/fi';
import './log.css';


function Log({ onSwitch, onReset }) {
  const [email, setEmail]   = useState('');
  const [password, setPass] = useState('');
  const [showPass, setShow] = useState(false);

  const handleSubmit = e => {
    e.preventDefault();
    alert(`Email: ${email}\nPassword: ${password}`);
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
          onChange={e => setPass(e.target.value)}
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
          <input type="checkbox" />
          <span>Remember me</span>
        </label>

        <button
          type="button"
          className="reset"
          onClick={onReset}
        >
          Reset Password?
        </button>
      </div>

      
      <button type="submit" className="primary-btn">Log in</button>


      <p className="footer">
        Don’t have account yet?
        <button
          type="button"
          className="link"
          onClick={onSwitch}
        >
          New&nbsp;Account
        </button>
      </p>
    </form>
  );
}

export default Log;
