import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";

import Log   from "./auth/log/log.jsx";
import Reg   from "./auth/reg/reg.jsx";
import Reset from "./auth/log/reset.jsx";

import { getMe } from "./api/users";
import { getAccessToken, setAccessToken } from "./auth/storage";
import { refresh } from "./api/auth";

function AuthSwitcher() {
  const [mode, setMode] = useState("loading"); 

  /* ───── check refresh cookie ───── */
  useEffect(() => {
    if (getAccessToken()) {
      getMe()
        .then(() => {
          window.location.href = "/main.html#/dashboard";
        })
        .catch(() => setMode("login"));
      return;
    }
    refresh()
      .then((d) => {
        setAccessToken(d.access_token);
        return getMe();
      })
      .then(() => {
        window.location.href = "/main.html#/dashboard";
      })
      .catch(() => setMode("login"));
  }, []);

  /* render nothing while waiting */
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
