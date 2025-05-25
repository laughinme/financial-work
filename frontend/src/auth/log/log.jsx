import React, { useState } from 'react';
import './log.css';


function Log({ onSwitch }) {
  const [emailr, setEmailr] = useState('');
  const [passwordr, setPasswordr] = useState('');


  const handleLogin = () => {
 
    alert(`Почта: ${emailr}\nПароль: ${passwordr}`);
   
  };

  return (
    <div className='container'>
      <div className='regplace'>
        <h1 className='header'>Log in</h1>
        <input
          className='email'
          type="email"
          placeholder='Email/Телефон'
          value={emailr}
          onChange={e => setEmailr(e.target.value)}
        />
        <input
          className='email'
          type="password"
          placeholder='Пароль'
          value={passwordr}
          onChange={e => setPasswordr(e.target.value)}
        />
        <div className='btns'>
          <button className='reg' type="button" onClick={handleLogin}>Log in</button>
          <button className='login' type="button" onClick={onSwitch}>Create an account</button>
        </div>
      </div>
    </div>
  );
}

export default Log;
