// src/api/auth.js
import http from "./http";
import { setAccessToken, clearTokens } from "../auth/storage";

/** POST /api/v1/auth/login  */
export const login = async (email, password) => {
  const res = await http.post("/api/v1/auth/login", { email, password });
  setAccessToken(res.access_token);
  return res;
};

/** POST /api/v1/auth/register */
export const register = async (email, password) => {
  const res = await http.post("/api/v1/auth/register", { email, password });
  setAccessToken(res.access_token);
  return res;
};

/** POST /api/v1/auth/logout */
export const logout = async () => {
  try {
    await http.post("/api/v1/auth/logout");
  } finally {
    clearTokens();
  }
};

export const refresh = () => http.post("/api/v1/auth/refresh");

/** POST /api/v1/auth/external/telegram/callback */
export const loginWithTelegram = (payload) =>
  http.post("/api/v1/auth/external/telegram/callback", payload);
