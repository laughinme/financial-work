import React, { useState } from 'react'
import { createRoot } from 'react-dom/client'
import Reg from './auth/reg/reg.jsx'
import Log from './auth/log/log.jsx'
import Reset from './auth/log/reset.jsx';
function AuthSwitcher() {
  const [mode, setMode] = useState('login');

  return (
    <div className="block">
      {mode === 'login' && (
        <Log
          onSwitch={() => setMode('register')}
          onReset={()  => setMode('reset')}
        />
      )}

      {mode === 'register' && (
        <Reg onSwitch={() => setMode('login')} />
      )}

      {mode === 'reset' && (
        <Reset onBack={() => setMode('login')} />
      )}
    </div>
  );
}

createRoot(document.getElementById('root')).render(<AuthSwitcher />);