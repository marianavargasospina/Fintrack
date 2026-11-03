import {apiRequest,getJson,escapeHtml} from './api.js';

export async function loadCategories(){
  const categories=await getJson('/categories');
  const list=document.querySelector('#categories-list');
  if(list){list.innerHTML=categories.map(category=>`<article><div><strong>${escapeHtml(category.name)}</strong><span>${escapeHtml(category.type)}</span></div><button class="delete-button" data-id="${escapeHtml(category.id)}" type="button" title="Eliminar categoría">Eliminar</button></article>`).join('');}
  document.querySelectorAll('#categories-list .delete-button').forEach(button=>button.addEventListener('click',async()=>{if(!confirm('¿Eliminar esta categoría? Solo se puede eliminar si no tiene movimientos ni presupuestos.'))return;try{await deleteCategory(button.dataset.id);await loadCategories();window.dispatchEvent(new Event('fintrack-data-changed'));}catch(error){document.querySelector('#app-message').textContent=error.message;}}));
  return categories;
}

export async function createCategory(data){
  await apiRequest('/categories',{method:'POST',body:JSON.stringify(data)});
  return loadCategories();
}

export async function deleteCategory(categoryId){
  return apiRequest(`/categories/${categoryId}`,{method:'DELETE'});
}
