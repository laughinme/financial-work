import React, { useState, useEffect } from "react";
import { FiEye, FiEyeOff } from "react-icons/fi";
import './reg.css';

import { createUser, setCurrent, findUser } from "../storage";

const API_URL = import.meta.env.VITE_API_URL || "";

export default function Reg({ onSwitch }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showPass, setShow] = useState(false);

    /* Telegram-виджет оставляем как был */
    useEffect(() => {
        window.onTelegramAuth = (user) => {
            alert(
                `Logged in as ${user.first_name} ${user.last_name} (${user.id})`
            );
        };
        const script = document.createElement("script");
        script.async = true;
        script.src = "https://telegram.org/js/telegram-widget.js?22";
        script.setAttribute("data-telegram-login", "niperybot");
        script.setAttribute("data-size", "large");
        script.setAttribute("data-onauth", "onTelegramAuth(user)");
        script.setAttribute("data-request-access", "write");

        const container = document.getElementById("telegram-login-button-reg");
        if (container) container.appendChild(script);
        return () => {
            if (container) container.innerHTML = "";
            delete window.onTelegramAuth;
        };
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const res = await fetch(`${API_URL}/api/v1/auth/register`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify({ email, password }),
            });

            if (!res.ok) {
                alert("Registration failed");
                return;
            }

            if (!findUser(email)) {
                createUser(email, password);
            }
            setCurrent(email);
            window.location.href = "/main.html";
        } catch (err) {
            alert("Registration failed");
        }
    };

    return (
        <form className="login-card" onSubmit={handleSubmit}>
            <h1 className="form-title">Registration</h1>

            <label className="field-label" htmlFor="email">
                Email Address
            </label>
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

            <label className="field-label" htmlFor="password">
                Password
            </label>
            <div className="input-wrapper password">
                <input
                    id="password"
                    type={showPass ? "text" : "password"}
                    placeholder="••••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    minLength={6}
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

            <button type="submit" className="primary-btn">
                Create an account
            </button>

            <div
                id="telegram-login-button-reg"
                style={{
                    display: "flex",
                    justifyContent: "center",
                    margin: "20px 0",
                }}
            />

            <p className="footer">
                Already have an account?
                <button type="button" className="link" onClick={onSwitch}>
                    Log&nbsp;in
                </button>
            </p>
        </form>
    );
}
