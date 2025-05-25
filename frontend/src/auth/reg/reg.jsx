import React, { useState } from 'react'
import './reg.css'

function Reg({ onSwitch }) {
  const [emailr, setEmailr] = useState('');
  const [passwordr, setPasswordr] = useState('');

 
  const handleSave = () => {
    localStorage.setItem('email', emailr);
    localStorage.setItem('password', passwordr);
    alert("Сохранено в LocalStorage (для теста)");
  };

  return (
    <div className='container'>
      <div className='regplace'>
        <h1 className='header'>Registration</h1>
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
          <button className='reg' type="button" onClick={handleSave}>
            Create an account
          </button>
          <button className='login' type="button" onClick={onSwitch}>
            Log in
          </button>
        </div>
      </div>
    </div>
  )
}

export default Reg
