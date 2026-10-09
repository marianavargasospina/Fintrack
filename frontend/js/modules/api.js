export const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

export async function apiRequest(path, options = {}) {
  const token = localStorage.getItem("fintrack_token");
  const headers = new Headers(options.headers || {});
  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (options.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  const response = await fetch(`${API_BASE_URL}${path}`, {...options, headers});
  if (response.status === 401) { localStorage.removeItem("fintrack_token"); window.dispatchEvent(new Event("auth-expired")); }
  if (!response.ok) throw new Error((await response.json().catch(() => ({}))).detail || "No se pudo completar la solicitud");
  return response;
}
export const getJson = path => apiRequest(path).then(response => response.json());
