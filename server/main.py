from __future__ import annotations

from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from inventory_service import InventoryService

app = FastAPI(title="Inventario API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = InventoryService()


class InventoryItem(BaseModel):
    codigo: str = Field(..., description="Identificador unico del producto")
    nombre: str = Field("", description="Nombre del producto")
    categoria: str = Field("", description="Categoria o familia")
    cantidad: int = Field(0, ge=0, description="Cantidad en stock")
    precio: float = Field(0, ge=0, description="Precio unitario")
    ubicacion: str = Field("", description="Ubicacion en almacen")
    minimo: int = Field(0, ge=0, description="Stock minimo")


@app.get("/api/health")
def healthcheck() -> dict:
    return {"status": "ok"}


@app.get("/api/dashboard")
def dashboard() -> dict:
    return service.dashboard()


@app.get("/api/inventory")
def list_inventory() -> List[dict]:
    df = service.load_inventory()
    return df.to_dict(orient="records")


@app.post("/api/inventory")
def add_inventory_item(item: InventoryItem) -> dict:
    try:
        new_row = service.add_item(item.dict())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"message": "Producto agregado", "item": new_row}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info",
    )

