
const ACC_KEY   = 'accounts';       
const CURR_KEY  = 'currentUser';    

export function getAccounts() {
  return JSON.parse(localStorage.getItem(ACC_KEY) || '[]');
}
export function saveAccounts(list) {
  localStorage.setItem(ACC_KEY, JSON.stringify(list));
}

export function setCurrent(email) {
  localStorage.setItem(CURR_KEY, email);
}
export function getCurrent() {
  return localStorage.getItem(CURR_KEY);         
}
export function clearCurrent() {
  localStorage.removeItem(CURR_KEY);
}

export function findUser(email) {
  return getAccounts().find((u) => u.email === email);
}

export function createUser(email, password) {
  const accounts = getAccounts();
  accounts.push({ email, password, investedIds: [] });
  saveAccounts(accounts);
}

export function updateInvested(email, investedIds) {
  const accounts = getAccounts().map((u) =>
    u.email === email ? { ...u, investedIds } : u
  );
  saveAccounts(accounts);
}
