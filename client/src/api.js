const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8001";

export async function fetchDashboard() {
  const res = await fetch(`${API_BASE_URL}/api/dashboard`);
  if (!res.ok) throw new Error("No se pudo cargar el dashboard");
  return res.json();
}

export async function fetchInventory() {
  const res = await fetch(`${API_BASE_URL}/api/inventory`);
  if (!res.ok) throw new Error("No se pudo cargar el inventario");
  return res.json();
}

export async function createInventoryItem(item) {
  const res = await fetch(`${API_BASE_URL}/api/inventory`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(item),
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || "No se pudo crear el producto");
  }

  return res.json();
}

export { API_BASE_URL };
