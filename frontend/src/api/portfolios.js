import http from "./http";


/**
 * GET /api/v1/portfolios/
 * @param {number}  size       
 * @param {number}  page       
 * @param {boolean} withCharts  
 */
export const listPortfolios = (
  size = 5,
  page = 1,
  withCharts = false
) =>
  http.get(
    `/api/v1/portfolios/?size=${size}&page=${page}` +
      `&with_charts=${withCharts ? "true" : "false"}`
  );

/** GET /api/v1/portfolios/{id}/ */
export const getPortfolio = (id) =>
  http.get(`/api/v1/portfolios/${id}/`);

/**
 * GET /api/v1/portfolios/{id}/history
 * @param {number} days – period (≥3)
 */
export const getHistory = (id, days = 30) =>
  http.get(`/api/v1/portfolios/${id}/history?days=${days}`);

/* ---------- user actions ---------- */

/** POST /api/v1/portfolios/{id}/invest   { amount } */
export const invest = (id, amount) =>
  http.post(`/api/v1/portfolios/${id}/invest`, { amount });

/** POST /api/v1/portfolios/{id}/withdraw   { units } */
export const withdraw = (id, units) =>
  http.post(`/api/v1/portfolios/${id}/withdraw`, { units });

/** GET /api/v1/portfolios/{id}/user-holding */
export const getHolding = (id) =>
  http.get(`/api/v1/portfolios/${id}/user-holding`);
