import {getJson} from './api.js';
export async function loadAccounts(){const accounts=await getJson('/accounts');document.querySelector('#accounts-list').innerHTML=accounts.map(account=>`<article><strong>${account.name}</strong><span>${account.currency} ${account.current_balance}</span></article>`).join('');}
