import http from "./http";

export const DASHBOARD_URL = `${window.location.origin}/dashboard`;

/* ───────── Deposit ───────── */
export const createDeposit = (amount, currency = "USD") =>
  http.post("/api/v1/payments/deposit", {
    amount,
    currency,
    description: `Deposit $${amount}`,
    action: "deposit",
    action_id: "",
    success_url: DASHBOARD_URL,
    cancel_url : DASHBOARD_URL,
  });

/* ───────── Withdraw ───────── */
export const createWithdraw = (amount) =>
  http.post("/api/v1/payments/withdraw", { amount });

/* ───────── Stripe onboarding ───────── */
export const getOnboardingLink = () =>
  http.post("/api/v1/users/me/stripe/connect/onboarding-link", {
    refresh_url: DASHBOARD_URL,
    return_url : DASHBOARD_URL,
  });                     

/* ───────── Balance ───────── */
export const getBalance = () => http.get("/api/v1/payments/balance");
