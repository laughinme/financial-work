
import axios from "axios";

/**
 * Unified entry point for all REST requests.
 * baseURL is taken from VITE_API_URL passed in the Dockerfile.
 */
export const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  withCredentials: true,      // send cookies along with requests
  timeout: 15000,
});

// intercept 401
API.interceptors.response.use(
  (r) => r,
  (err) => {
    if (err?.response?.status === 401) {
      localStorage.removeItem("currentEmail");
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(err);
  }
);
