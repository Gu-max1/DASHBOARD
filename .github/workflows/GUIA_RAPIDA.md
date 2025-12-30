# ⚡ Guía Rápida - Sistema de Control de Inventario

Esta es la guía técnica actualizada para el sistema que hemos construido.

## 🚀 Inicio Automático (Recomendado)

Para usuarios finales, la forma más fácil de iniciar es:

1.  Ve a la carpeta del proyecto.
2.  Doble clic en **`INICIAR_SISTEMA.bat`**.
3.  El sistema abrirá automáticamente el Servidor y el Cliente.

---

## 🛠️ Inicio Manual (Para Desarrolladores)

Si necesitas correr los servicios por separado para depuración:

### 1. Backend (API Python)
El cerebro del sistema. Maneja el Excel y la lógica.
**Puerto**: `8001`

```bash
cd server
# Activar entorno virtual si lo usas, o simplemente:
python main.py
```

### 2. Frontend (React)
La interfaz visual.
**Puerto**: `3000`

```bash
cd client
npm run dev
```

---

## 🔗 URLs del Sistema

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **App Web** | [http://localhost:3000](http://localhost:3000) | Aplicación principal para usuarios |
| **API Docs** | [http://localhost:8001/docs](http://localhost:8001/docs) | Documentación interactiva (Swagger) |
| **Dashboard** | [http://localhost:8001/api/dashboard](http://localhost:8001/api/dashboard) | JSON de métricas en tiempo real |

---

## 💾 Gestión de Datos (Excel)

Todo se guarda en: `data/inventario.xlsx`

### Estructura del Archivo
- **Inventario**: Lista maestra de productos (Código, Nombre, Cantidad, etc.)
- **Movimientos**: Bitácora de entradas y salidas.
- **Conteos**: Registro de auditorías físicas.
- **Configuracion**: Parámetros globales.

> **💡 Tip**: Puedes editar el Excel manualmente si el servidor está apagado. Al encenderlo, el sistema leerá tus cambios.

---

## 🧪 Comandos Útiles

### Poblar con Datos de Prueba
Si la base de datos está vacía o quieres reiniciarla:
```bash
cd server
python seed_data.py
```
*Esto generará 10 productos, movimientos y conteos de ejemplo.*

### Probar API vía Consola (cURL)
```bash
# Ver métricas del dashboard
curl http://localhost:8001/api/dashboard

# Agregar un producto rápido
curl -X POST "http://localhost:8001/api/inventory" ^
  -H "Content-Type: application/json" ^
  -d "{\"codigo\":\"TEST99\",\"nombre\":\"Demo Item\",\"categoria\":\"Test\",\"cantidad\":100,\"precio\":10.5,\"ubicacion\":\"A1\",\"minimo\":5}"
```

---

## ⚠️ Solución de Problemas Comunes

**1. "Port 8001 already in use"**
El servidor ya está corriendo en otra ventana. Busca una ventana negra llamada "Backend Server" y ciérrala, o úsala.

**2. Pantalla Blanca en el Navegador**
- Verifica que el Backend (ventana negra) no tenga errores rojos.
- Presiona `F12` en el navegador para ver si hay errores de conexión.
- Asegúrate de entrar a `http://localhost:3000` y NO al puerto 8001 con el navegador (el 8001 es solo datos).

**3. Error "KeyError" en el Backend**
El archivo Excel tiene columnas viejas. Borra `data/inventario.xlsx` y reinicia el servidor para que se regenere automáticamente.
