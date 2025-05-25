import React, { useState } from 'react'
import { createRoot } from 'react-dom/client'
import './auth.css'
import Reg from './auth/reg/reg.jsx'
import Log from './auth/log/log.jsx'


function AuthSwitcher() {
    const [isLogin, setIsLogin] = useState(false);
  
    return (
      <div className="block">
        {isLogin ? (
          <Log onSwitch={() => setIsLogin(false)} />
        ) : (
          <Reg onSwitch={() => setIsLogin(true)} />
        )}
      </div>
    );
  }
  
  createRoot(document.getElementById("root")).render(<AuthSwitcher />);