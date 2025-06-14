import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";

import Log   from "./auth/log/log.jsx";
import Reg   from "./auth/reg/reg.jsx";
import Reset from "./auth/log/reset.jsx";

import { getMe } from "./api/users";          

function AuthSwitcher() {
  const [mode, setMode] = useState("loading"); 

  /* ───── проверяем cookie-сессию ───── */
  useEffect(() => {
    getMe()
      .then(() => {
        // сессия валидна сразу на дашборд
        window.location.href = "/main.html#/dashboard";
      })
      .catch(() => {
        // 401 / 403 
        setMode("login");
      });
  }, []);

  /* пока ждём ответа — ничего не рендерим */
  if (mode === "loading") return null;

  return (
    <div className="block">
      {mode === "login" && (
        <Log
          onSwitch={() => setMode("register")}
          onReset={() => setMode("reset")}
        />
      )}

      {mode === "register" && <Reg onSwitch={() => setMode("login")} />}

      {mode === "reset" && <Reset onBack={() => setMode("login")} />}
    </div>
  );
}

createRoot(document.getElementById("root")).render(<AuthSwitcher />);
