// src/api/auth.js
import http from "./http";

/** POST /api/v1/auth/login  */
export const login = (email, password) =>
  http.post("/api/v1/auth/login", { email, password });

/** POST /api/v1/auth/register */
export const register = (email, password) =>
  http.post("/api/v1/auth/register", { email, password });

/** POST /api/v1/auth/logout */
export const logout = () => http.post("/api/v1/auth/logout");
