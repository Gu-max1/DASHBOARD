import { useEffect, useMemo, useState } from "react";
import { API_BASE_URL, createInventoryItem, fetchDashboard, fetchInventory } from "./api.js";

const initialForm = {
  codigo: "",
  nombre: "",
  categoria: "",
  cantidad: 0,
  precio: 0,
  ubicacion: "",
  minimo: 0,
};

export default function App() {
  const [dashboard, setDashboard] = useState(null);
  const [inventory, setInventory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [form, setForm] = useState(initialForm);
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      setError("");
      try {
        const [dashData, inventoryData] = await Promise.all([
          fetchDashboard(),
          fetchInventory(),
        ]);
        setDashboard(dashData);
        setInventory(inventoryData);
      } catch (err) {
        setError(err.message || "Error cargando datos");
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({
      ...prev,
      [name]: name === "cantidad" || name === "minimo" ? Number(value) : name === "precio" ? Number(value) : value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setCreating(true);
    try {
      await createInventoryItem(form);
      const [dashData, inventoryData] = await Promise.all([
        fetchDashboard(),
        fetchInventory(),
      ]);
      setDashboard(dashData);
      setInventory(inventoryData);
      setForm(initialForm);
    } catch (err) {
      setError(err.message || "No se pudo crear el producto");
    } finally {
      setCreating(false);
    }
  };

  const lowStockItems = useMemo(
    () => inventory.filter((item) => Number(item.cantidad) <= Number(item.minimo)),
    [inventory]
  );

  return (
    <div className="container">
      <header>
        <div>
          <p className="eyebrow">API: {API_BASE_URL}</p>
          <h1>Dashboard de Inventario</h1>
          <p>Backend en FastAPI (puerto 8001) y frontend en React/Vite (puerto 3000).</p>
        </div>
        <div className="tags">
          <span className="tag">Python FastAPI</span>
          <span className="tag">Excel (openpyxl)</span>
          <span className="tag">React + Vite</span>
        </div>
      </header>

      {error && <div className="alert">{error}</div>}
      {loading ? (
        <p>Cargando datos...</p>
      ) : (
        <>
          {dashboard && (
            <section className="cards">
              <MetricCard title="Productos" value={dashboard.total_items} />
              <MetricCard title="Unidades" value={dashboard.total_quantity} />
              <MetricCard title="Valor inventario" value={`$${dashboard.stock_value}`} />
              <MetricCard title="Bajo stock" value={dashboard.low_stock_count} />
            </section>
          )}

          <section className="grid">
            <div className="panel">
              <div className="panel-header">
                <h2>Inventario</h2>
                <small>{inventory.length} items</small>
              </div>
              <div className="table">
                <div className="table-head">
                  <div>Codigo</div>
                  <div>Nombre</div>
                  <div>Categoria</div>
                  <div>Cantidad</div>
                  <div>Precio</div>
                  <div>Minimo</div>
                </div>
                <div className="table-body">
                  {inventory.map((item) => (
                    <div className="table-row" key={item.codigo}>
                      <div>{item.codigo}</div>
                      <div>{item.nombre}</div>
                      <div>{item.categoria}</div>
                      <div>{item.cantidad}</div>
                      <div>${item.precio}</div>
                      <div>{item.minimo}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="panel">
              <div className="panel-header">
                <h2>Nuevo producto</h2>
                <small>Se guarda directamente en Excel</small>
              </div>
              <form className="form" onSubmit={handleSubmit}>
                <label>
                  Codigo
                  <input name="codigo" value={form.codigo} onChange={handleChange} required />
                </label>
                <label>
                  Nombre
                  <input name="nombre" value={form.nombre} onChange={handleChange} />
                </label>
                <label>
                  Categoria
                  <input name="categoria" value={form.categoria} onChange={handleChange} />
                </label>
                <label>
                  Cantidad
                  <input type="number" name="cantidad" value={form.cantidad} onChange={handleChange} min="0" />
                </label>
                <label>
                  Precio
                  <input type="number" step="0.01" name="precio" value={form.precio} onChange={handleChange} min="0" />
                </label>
                <label>
                  Ubicacion
                  <input name="ubicacion" value={form.ubicacion} onChange={handleChange} />
                </label>
                <label>
                  Minimo
                  <input type="number" name="minimo" value={form.minimo} onChange={handleChange} min="0" />
                </label>
                <button type="submit" disabled={creating}>
                  {creating ? "Guardando..." : "Agregar"}
                </button>
              </form>

              <div className="panel-subsection">
                <h3>Alertas de stock</h3>
                {lowStockItems.length === 0 ? (
                  <p className="muted">No hay alertas en este momento.</p>
                ) : (
                  <ul className="chips">
                    {lowStockItems.map((item) => (
                      <li key={item.codigo} className="chip">
                        {item.codigo} · {item.nombre} ({item.cantidad}/{item.minimo})
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          </section>
        </>
      )}
    </div>
  );
}

function MetricCard({ title, value }) {
  return (
    <div className="card">
      <p className="eyebrow">{title}</p>
      <p className="metric">{value}</p>
    </div>
  );
}
