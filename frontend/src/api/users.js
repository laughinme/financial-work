
import http from './http';

/** GET /api/v1/users/me/ */
export const getMe = () => http.get('/api/v1/users/me/');

/**
 * POST /api/v1/users/me/auth_methods/telegram
 * @param {object} payload  – object provided by the Telegram widget
 * @param {boolean} replace – ?replace_fields=false|true
 */
export const linkTelegram = (payload, replace = false) =>
  http.post(
    `/api/v1/users/me/auth_methods/telegram?replace_fields=${replace}`,
    payload,
  );
