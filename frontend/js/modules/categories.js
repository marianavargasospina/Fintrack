import {apiRequest,getJson,escapeHtml} from './api.js';

export async function loadCategories(){
  const categories=await getJson('/categories');
  const list=document.querySelector('#categories-list');
  if(list){list.innerHTML=categories.map(category=>`<article><strong>${escapeHtml(category.name)}</strong><span>${escapeHtml(category.type)}</span></article>`).join('');}
  return categories;
}

export async function createCategory(data){
  await apiRequest('/categories',{method:'POST',body:JSON.stringify(data)});
  return loadCategories();
}
