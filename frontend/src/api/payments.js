// src/api/payments.js
import http from "./http";

/**
 * POST /api/v1/payments/deposit
 * @param {number}  amount      – сумма в валюте
 * @param {string}  currency    – “USD” | “EUR” …
 * @param {string}  description – подпись в эквайринге
 * @param {string}  actionId    – произвольный ID (можно оставить "")
 * @returns {Promise<{url:string}>}
 */
export const createDeposit = (
  amount,
  currency = "USD",
  description = "Balance top-up",
  actionId = ""
) =>
  http.post("/api/v1/payments/deposit", {
    amount,
    currency,
    description,
    action: "deposit",
    action_id: actionId,
  });
