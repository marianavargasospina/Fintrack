import {getJson} from './api.js';
export async function loadBudgets(){const budgets=await getJson('/budgets');document.querySelector('#budgets-list').innerHTML=budgets.map(item=>`<article><strong>${item.start_date} - ${item.end_date}</strong><span>Límite: ${item.amount_limit}</span></article>`).join('');}
