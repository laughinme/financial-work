const API_URL = import.meta.env.VITE_API_URL || '';

import { getAccessToken, setAccessToken, clearTokens } from '../auth/storage';

const request = async (method, url, body) => {
  const headers = { 'Content-Type': 'application/json' };
  const token = getAccessToken();
  if (token) headers['Authorization'] = `Bearer ${token}`;

  let res = await fetch(`${API_URL}${url}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
    credentials: 'include',
  });

  if (res.status === 401) {
    try {
      const r = await fetch(`${API_URL}/api/v1/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
      });
      if (r.ok) {
        const data = await r.json();
        setAccessToken(data.access_token);
        headers['Authorization'] = `Bearer ${data.access_token}`;
        res = await fetch(`${API_URL}${url}`, {
          method,
          headers,
          body: body ? JSON.stringify(body) : undefined,
          credentials: 'include',
        });
      } else {
        clearTokens();
      }
    } catch {
      clearTokens();
    }
  }

  /* ——— 401 / 403 ——— */
  if (res.status === 401 || res.status === 403) {
    const err = new Error('unauthorized');
    err.status = res.status;
    throw err;
  }

  /* --- other errors --- */
  if (!res.ok) {
   
    let msg;
    try { msg = JSON.stringify(await res.clone().json()); }
    catch { msg = await res.text(); }

    const err = new Error(msg || res.statusText);
    err.status = res.status;        
    throw err;
  }

  /* 204 No Content */
  return res.status === 204 ? null : res.json();
};

export default {
  get : (u)       => request('GET',    u),
  post: (u, body) => request('POST',   u, body),
  put : (u, body) => request('PUT',    u, body),
  del : (u)       => request('DELETE', u),
};
