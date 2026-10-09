import {apiRequest} from './api.js';
export async function login(email, password){const response=await apiRequest('/auth/login',{method:'POST',body:JSON.stringify({email,password})});const data=await response.json();localStorage.setItem('fintrack_token',data.access_token);return data;}
export async function register(name, email, password){const response=await apiRequest('/auth/register',{method:'POST',body:JSON.stringify({name,email,password})});return response.json();}
export function logout(){localStorage.removeItem('fintrack_token');window.dispatchEvent(new Event('auth-expired'));}
export const isAuthenticated=()=>Boolean(localStorage.getItem('fintrack_token'));
