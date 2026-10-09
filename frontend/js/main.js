import {login,register,logout,isAuthenticated} from './modules/auth.js';
import {escapeHtml} from './modules/api.js';
import {loadDashboard} from './modules/dashboard.js';
import {loadAccounts,createAccount} from './modules/accounts.js';
import {loadCategories,createCategory} from './modules/categories.js';
import {loadTransactions,createTransaction,exportTransactions} from './modules/transactions.js';
import {loadBudgets,createBudget} from './modules/budgets.js';
import {loadGoals,createGoal} from './modules/goals.js';

const authView=document.querySelector('#auth-view');
const appView=document.querySelector('#app-view');
const message=document.querySelector('#app-message');
const authMessage=document.querySelector('#auth-message');
const today=new Date().toISOString().slice(0,10);

function showApp(){authView.hidden=true;appView.hidden=false;loadDashboard().catch(showError);}
function showLogin(){authView.hidden=false;appView.hidden=true;}
function showError(error){message.textContent=error.message;}
function formDataObject(form){return Object.fromEntries(new FormData(form).entries());}
function removeEmptyValues(data){return Object.fromEntries(Object.entries(data).filter(([,value])=>value!==''));}
function fillSelect(selector,items,placeholder){
  const select=document.querySelector(selector);
  if(!select)return;
  select.innerHTML=`<option value="">${escapeHtml(placeholder)}</option>`+items.map(item=>`<option value="${escapeHtml(item.id)}">${escapeHtml(item.name)}</option>`).join('');
}
async function loadReferenceData(){
  const [accounts,categories]=await Promise.all([loadAccounts(),loadCategories()]);
  fillSelect('#transaction-form select[name="account_id"]',accounts,'Cuenta de origen');
  fillSelect('#transaction-form select[name="destination_account_id"]',accounts,'Cuenta destino (transferencia)');
  fillSelect('#transaction-form select[name="category_id"]',categories,'Categoría');
  fillSelect('#budget-form select[name="category_id"]',categories.filter(category=>category.type==='expense'),'Categoría');
}
function setDefaultDates(){
  document.querySelector('#transaction-form [name="transaction_date"]').value=today;
  const date=new Date();
  const start=new Date(date.getFullYear(),date.getMonth(),1).toISOString().slice(0,10);
  const end=new Date(date.getFullYear(),date.getMonth()+1,0).toISOString().slice(0,10);
  document.querySelector('#budget-form [name="start_date"]').value=start;
  document.querySelector('#budget-form [name="end_date"]').value=end;
}

document.querySelector('#login-form').addEventListener('submit',async event=>{
  event.preventDefault();
  try{const data=formDataObject(event.currentTarget);await login(data.email,data.password);showApp();}
  catch(error){authMessage.textContent=error.message;}
});
document.querySelector('#register-form').addEventListener('submit',async event=>{
  event.preventDefault();
  try{const data=formDataObject(event.currentTarget);await register(data.name,data.email,data.password);await login(data.email,data.password);showApp();}
  catch(error){authMessage.textContent=error.message;}
});
document.querySelector('#auth-toggle').addEventListener('click',event=>{
  const registerMode=document.querySelector('#register-form').hidden;
  document.querySelector('#register-form').hidden=!registerMode;
  document.querySelector('#login-form').hidden=registerMode;
  event.currentTarget.textContent=registerMode?'Ya tengo una cuenta':'Crear una cuenta';
  authMessage.textContent='';
});
document.querySelector('#logout').addEventListener('click',logout);
window.addEventListener('auth-expired',showLogin);

document.querySelectorAll('.tab').forEach(tab=>tab.addEventListener('click',async()=>{
  document.querySelectorAll('.tab').forEach(item=>item.classList.toggle('active',item===tab));
  document.querySelectorAll('.view').forEach(view=>view.hidden=view.id!==tab.dataset.section);
  const loaders={dashboard:loadDashboard,accounts:loadReferenceData,categories:loadCategories,transactions:loadReferenceData,budgets:loadBudgets,goals:loadGoals};
  try{await loaders[tab.dataset.section]();}catch(error){showError(error);}
}));

document.querySelector('#account-form').addEventListener('submit',async event=>{event.preventDefault();try{await createAccount(formDataObject(event.currentTarget));event.currentTarget.reset();await loadReferenceData();}catch(error){showError(error);}});
document.querySelector('#category-form').addEventListener('submit',async event=>{event.preventDefault();try{await createCategory(formDataObject(event.currentTarget));event.currentTarget.reset();await loadReferenceData();}catch(error){showError(error);}});
document.querySelector('#transaction-form').addEventListener('submit',async event=>{event.preventDefault();try{await createTransaction(removeEmptyValues(formDataObject(event.currentTarget)));event.currentTarget.reset();setDefaultDates();await loadReferenceData();}catch(error){showError(error);}});
document.querySelector('#budget-form').addEventListener('submit',async event=>{event.preventDefault();try{await createBudget(formDataObject(event.currentTarget));event.currentTarget.reset();setDefaultDates();await loadBudgets();}catch(error){showError(error);}});
document.querySelector('#goal-form').addEventListener('submit',async event=>{event.preventDefault();try{await createGoal(formDataObject(event.currentTarget));event.currentTarget.reset();await loadGoals();}catch(error){showError(error);}});
document.querySelector('#transaction-filters').addEventListener('submit',event=>{event.preventDefault();loadTransactions(removeEmptyValues(formDataObject(event.currentTarget))).catch(showError);});
document.querySelector('#export-button').addEventListener('click',()=>exportTransactions().catch(showError));
document.querySelector('#theme-toggle').addEventListener('click',event=>{const dark=document.documentElement.dataset.theme!=='dark';document.documentElement.dataset.theme=dark?'dark':'light';event.currentTarget.setAttribute('aria-pressed',dark);localStorage.setItem('fintrack_theme',document.documentElement.dataset.theme);});
document.documentElement.dataset.theme=localStorage.getItem('fintrack_theme')||'';
setDefaultDates();
if(isAuthenticated())showApp();
