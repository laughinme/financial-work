import { API } from "./base";

/*KPI SUMMARY*/
export const getSummary = () =>
  API.get("/api/v1/dashboard/summary").then(r => r.data);

/*ALLOCATION*/
export const getAllocation = () =>
  API.get("/api/v1/dashboard/allocation").then(r => r.data);

/*DAILY P/L*/
export const getDailyPnl = (days = 90) =>
  API.get("/api/v1/dashboard/daily-pnl", { params: { days } })
     .then(r => r.data);

/*PORTFOLIO VALUE vs TIM*/
export const getPortfolioValue = (days = 90) =>
  API.get("/api/v1/dashboard/portfolio-value", { params: { days } })
     .then(r => r.data);


