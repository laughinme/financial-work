const API_URL = import.meta.env.VITE_API_URL || '';

const request = async (method, url, body) => {
  const res = await fetch(`${API_URL}${url}`, {
    method,
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  });

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
