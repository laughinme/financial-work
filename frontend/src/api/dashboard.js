
import { API } from "./base";   

export const getSummary = () =>
  API.get("/api/v1/dashboard/summary").then(r => r.data);

export const getAllocation = () =>
  API.get("/api/v1/dashboard/allocation").then(r => r.data);

export const getCashflow = (days = 90) =>
  API.get("/api/v1/dashboard/cashflow", { params: { days } }).then(r => r.data);

export const getPortfolioValue = (days = 90) =>
  API.get("/api/v1/dashboard/portfolio-value", { params: { days } })
     .then(r => r.data);
