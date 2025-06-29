import axios from "axios";
import { getAccessToken, setAccessToken, clearTokens } from "../auth/storage";

/**
 * Unified entry point for all REST requests.
 * baseURL is taken from VITE_API_URL passed in the Dockerfile.
 */
export const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 15000,
  withCredentials: true,
});

API.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) config.headers["Authorization"] = `Bearer ${token}`;
  return config;
});

// intercept 401
API.interceptors.response.use(
  (r) => r,
  async (err) => {
    if (err?.response?.status === 401) {
      try {
        const { data } = await API.post("/api/v1/auth/refresh");
        setAccessToken(data.access_token);
        err.config.headers["Authorization"] = `Bearer ${data.access_token}`;
        return API.request(err.config);
      } catch {
        clearTokens();
        localStorage.removeItem("currentEmail");
        if (window.location.pathname !== "/login") {
          window.location.href = "/login";
        }
      }
    }
    return Promise.reject(err);
  }
);
