import {apiRequest,getJson,escapeHtml} from './api.js';
export async function loadBudgets(){const budgets=await getJson('/budgets');document.querySelector('#budgets-list').innerHTML=budgets.map(item=>`<article><strong>${escapeHtml(item.start_date)} - ${escapeHtml(item.end_date)}</strong><span>Límite: ${escapeHtml(item.amount_limit)}</span></article>`).join('');}
export async function createBudget(data){await apiRequest('/budgets',{method:'POST',body:JSON.stringify(data)});return loadBudgets();}
