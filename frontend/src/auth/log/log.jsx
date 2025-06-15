
import React, { useState, useEffect } from "react";
import { FiEye, FiEyeOff }            from "react-icons/fi";
import "../log/log.css";

import { findUser, createUser, setCurrent } from "../storage";
import { linkTelegram }                      from "../../api/users";
import { login as loginApi }                 from "../../api/auth";

export default function Log({ onSwitch, onReset }) {
  const [email,    setEmail]    = useState("");
  const [password, setPassword] = useState("");
  const [showPass, setShow]     = useState(false);

  /* ───── Telegram-виджет ───── */
  useEffect(() => {
    window.onTelegramAuth = (user) => {
      linkTelegram(user, true)
        .then(() =>
          alert(`Telegram linked: @${user.username || user.id}`)
        )
        .catch(() => alert("Не удалось связать Telegram-аккаунт"));
    };

    const script = document.createElement("script");
    script.async = true;
    script.src   = "https://telegram.org/js/telegram-widget.js?22";
    script.setAttribute("data-telegram-login",    "niperybot");
    script.setAttribute("data-size",               "large");
    script.setAttribute("data-onauth",             "onTelegramAuth(user)");
    script.setAttribute("data-request-access",     "write");

    const container = document.getElementById("telegram-login-button");
    if (container) container.appendChild(script);

    return () => {
      const c = document.getElementById("telegram-login-button");
      if (c) c.innerHTML = "";
      delete window.onTelegramAuth;
    };
  }, []);

  /* ───── отправка формы ───── */
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await loginApi(email, password);

      if (!findUser(email)) createUser(email, password);
      setCurrent(email);
      localStorage.setItem("currentEmail", email);

      if (email === "admin@example.com") {
        window.location.href = "/admin";
      } else {
        window.location.href = "/main.html#/dashboard";
      }
    } catch {
      alert("Wrong email / password");
    }
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
          type={showPass ? "text" : "password"}
          placeholder="••••••••••"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button
          type="button"
          className="toggle-pass"
          onClick={() => setShow(!showPass)}
          aria-label={showPass ? "Hide password" : "Show password"}
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
        style={{ display: "flex", justifyContent: "center", margin: "20px 0" }}
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
