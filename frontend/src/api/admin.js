// src/api/admin.js
import http from "./http";

/** GET /api/v1/admins/settlements?orders_quantity=5 */
export const listSettlements = (ordersQty = 5) =>
  http.get(`/api/v1/admins/settlements?orders_quantity=${ordersQty}`);

/** POST /api/v1/admins/{portfolio_id}/intent  — 204 NoContent */
export const createIntent = (portfolioId) =>
  http.post(`/api/v1/admins/${portfolioId}/intent`);
