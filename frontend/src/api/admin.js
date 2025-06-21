
import http from "./http";




export const listSettlements = (ordersQty = 5) =>
  http.get(
    `/api/v1/admins/settlements?orders_quantity=${ordersQty}`
  );

export const createIntent = (portfolioId) =>
  http.post(
    `/api/v1/admins/${portfolioId}/intent`
  );
