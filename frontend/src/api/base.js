
import axios from "axios";

/**
 * Единая точка для всех REST-запросов.
 * baseURL берётся из VITE_API_URL, которую мы прокидываем в Dockerfile.
 */
export const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  withCredentials: true,      // чтобы куки ходили вместе с запросами
  timeout: 15000,
});

// перехват 401 
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
