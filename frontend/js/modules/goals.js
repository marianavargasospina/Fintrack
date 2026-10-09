import {apiRequest,getJson,escapeHtml} from './api.js';
const money=value=>new Intl.NumberFormat('es-CO',{style:'currency',currency:'COP',maximumFractionDigits:0}).format(value);
export async function loadGoals(){const goals=await getJson('/goals');document.querySelector('#goals-list').innerHTML=goals.map(goal=>{const percentage=Math.min(100,Math.max(0,Number(goal.percentage)));return `<article><div><strong>${escapeHtml(goal.name)}</strong><p>${money(goal.current_amount)} de ${money(goal.target_amount)} · ${percentage.toFixed(1)}%</p><div class="progress" aria-label="${percentage}% completado"><span style="width:${percentage}%"></span></div></div><button class="progress-button" data-id="${escapeHtml(goal.id)}" type="button">Registrar avance</button></article>`}).join('');document.querySelectorAll('.progress-button').forEach(button=>button.addEventListener('click',async()=>{const value=prompt('Nuevo monto acumulado');if(value!==null){await apiRequest(`/goals/${button.dataset.id}/progress`,{method:'POST',body:JSON.stringify({current_amount:value})});await loadGoals();}}));}
export async function createGoal(data){
	await apiRequest('/goals',{method:'POST',body:JSON.stringify({...data,current_amount:data.current_amount||0})});
	return loadGoals();
}
