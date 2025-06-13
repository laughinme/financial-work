// src/api/portfolios.js
import http from "./http";

/**
 * GET /api/v1/portfolios
 * @param {number} size  – сколько карточек на страницу
 * @param {number} page  – номер страницы
 * @param {boolean} withCharts – добавить sparkline
 */
export const listPortfolios = (size = 5, page = 1, withCharts = false) =>
  http.get(
    `/api/v1/portfolios/?size=${size}&page=${page}&with_charts=${withCharts}`
  );

/** GET /api/v1/portfolios/{id} */
export const getPortfolio = (id) => http.get(`/api/v1/portfolios/${id}/`);

/**
 * GET /api/v1/portfolios/{id}/history
 * @param {number} days – период (≥3)
 */
export const getHistory = (id, days = 30) =>
  http.get(`/api/v1/portfolios/${id}/history?days=${days}`);

/** POST /api/v1/portfolios/{id}/invest  { amount } */
export const invest = (id, amount) =>
  http.post(`/api/v1/portfolios/${id}/invest`, { amount });

/** POST /api/v1/portfolios/{id}/withdraw  { units } */
export const withdraw = (id, units) =>
  http.post(`/api/v1/portfolios/${id}/withdraw`, { units });

/** GET /api/v1/portfolios/{id}/user_holding */
export const getHolding = (id) =>
  http.get(`/api/v1/portfolios/${id}/user_holding`);
