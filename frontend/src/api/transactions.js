// src/api/transactions.js
import http from "./http";

/**
 * GET /api/v1/transactions
 * @param {number} size  default = 10
 * @param {number} page  default = 1
 */
export const listTransactions = (size = 10, page = 1) =>
  http.get(`/api/v1/transactions/?size=${size}&page=${page}`);

/** GET /api/v1/transactions/{id} */
export const getTransaction = (id) =>
  http.get(`/api/v1/transactions/${id}/`);
