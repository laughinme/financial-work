// src/api/dashboard.js
import http from './http';

/**
 * GET /api/v1/dashboard/summary
 * @returns {Promise<{
 *   total_equity: string,
 *   total_pnl:    string,
 *   today_pnl:    string,
 *   portfolios_num: string
 * }>}
 */
export const getSummary = () =>
  http.get('/api/v1/dashboard/summary');
