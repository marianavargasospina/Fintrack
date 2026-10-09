import {apiRequest,getJson,escapeHtml} from './api.js';
export async function loadAccounts(){const accounts=await getJson('/accounts');document.querySelector('#accounts-list').innerHTML=accounts.map(account=>`<article><strong>${escapeHtml(account.name)}</strong><span>${escapeHtml(account.currency)} ${escapeHtml(account.current_balance)}</span></article>`).join('');return accounts;}
export async function createAccount(data){await apiRequest('/accounts',{method:'POST',body:JSON.stringify(data)});return loadAccounts();}
