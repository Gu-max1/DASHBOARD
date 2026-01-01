from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, List

import pandas as pd


DEFAULT_INVENTORY_COLUMNS = [
    "codigo",
    "nombre",
    "categoria",
    "cantidad",
    "precio",
    "ubicacion",
    "minimo",
]

DEFAULT_MOVEMENTS_COLUMNS = ["codigo", "tipo", "cantidad", "fecha"]
DEFAULT_COUNTS_COLUMNS = ["codigo", "conteo", "fecha"]


class InventoryService:
    """Small helper to manage the Excel-based inventory file."""

    def __init__(self, data_path: Path | None = None) -> None:
        base_dir = Path(__file__).resolve().parent
        self.data_path = data_path or base_dir / "data" / "inventario.xlsx"
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        if self.data_path.exists():
            return

        self._write_workbook(
            inventory_rows=self._default_inventory_rows(),
            movement_rows=self._default_movement_rows(),
            count_rows=self._default_count_rows(),
            config_rows={"version": ["1.0"], "generated_at": [datetime.utcnow()]},
        )

    def _write_workbook(
        self,
        inventory_rows: List[Dict[str, object]],
        movement_rows: List[Dict[str, object]],
        count_rows: List[Dict[str, object]],
        config_rows: Dict[str, List[object]],
    ) -> None:
        inventory_df = pd.DataFrame(inventory_rows, columns=DEFAULT_INVENTORY_COLUMNS)
        movement_df = pd.DataFrame(movement_rows, columns=DEFAULT_MOVEMENTS_COLUMNS)
        counts_df = pd.DataFrame(count_rows, columns=DEFAULT_COUNTS_COLUMNS)
        config_df = pd.DataFrame(config_rows)

        with pd.ExcelWriter(self.data_path, engine="openpyxl") as writer:
            inventory_df.to_excel(writer, sheet_name="Inventario", index=False)
            movement_df.to_excel(writer, sheet_name="Movimientos", index=False)
            counts_df.to_excel(writer, sheet_name="Conteos", index=False)
            config_df.to_excel(writer, sheet_name="Configuracion", index=False)

    def _default_inventory_rows(self) -> List[Dict[str, object]]:
        return [
            {
                "codigo": "PRD-001",
                "nombre": "Laptop",
                "categoria": "Tecnologia",
                "cantidad": 12,
                "precio": 950.0,
                "ubicacion": "A1",
                "minimo": 5,
            },
            {
                "codigo": "PRD-002",
                "nombre": "Mouse Inalambrico",
                "categoria": "Accesorios",
                "cantidad": 45,
                "precio": 25.5,
                "ubicacion": "B3",
                "minimo": 10,
            },
            {
                "codigo": "PRD-003",
                "nombre": "Silla Ergonomica",
                "categoria": "Oficina",
                "cantidad": 18,
                "precio": 120.0,
                "ubicacion": "C2",
                "minimo": 6,
            },
        ]

    def _default_movement_rows(self) -> List[Dict[str, object]]:
        now = datetime.utcnow().isoformat()
        return [
            {"codigo": "PRD-001", "tipo": "entrada", "cantidad": 5, "fecha": now},
            {"codigo": "PRD-002", "tipo": "salida", "cantidad": 2, "fecha": now},
            {"codigo": "PRD-003", "tipo": "entrada", "cantidad": 4, "fecha": now},
        ]

    def _default_count_rows(self) -> List[Dict[str, object]]:
        now = datetime.utcnow().date().isoformat()
        return [
            {"codigo": "PRD-001", "conteo": 12, "fecha": now},
            {"codigo": "PRD-002", "conteo": 45, "fecha": now},
            {"codigo": "PRD-003", "conteo": 18, "fecha": now},
        ]

    def load_workbook(self) -> Dict[str, pd.DataFrame]:
        return pd.read_excel(self.data_path, sheet_name=None)

    def load_inventory(self) -> pd.DataFrame:
        workbook = self.load_workbook()
        inventory_df = workbook.get("Inventario")
        if inventory_df is None:
            inventory_df = pd.DataFrame(columns=DEFAULT_INVENTORY_COLUMNS)
        return inventory_df

    def save_inventory(self, inventory_df: pd.DataFrame) -> None:
        workbook = self.load_workbook()
        workbook["Inventario"] = inventory_df[DEFAULT_INVENTORY_COLUMNS]

        with pd.ExcelWriter(self.data_path, engine="openpyxl") as writer:
            for sheet_name, df in workbook.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    def add_item(self, item_data: Dict[str, object]) -> Dict[str, object]:
        inventory_df = self.load_inventory()
        if "codigo" not in item_data:
            raise ValueError("El campo 'codigo' es obligatorio")

        code = str(item_data["codigo"])
        if not code:
            raise ValueError("El codigo no puede estar vacio")

        if code in inventory_df["codigo"].astype(str).values:
            raise ValueError(f"Ya existe un producto con codigo {code}")

        new_row = {
            "codigo": code,
            "nombre": item_data.get("nombre", ""),
            "categoria": item_data.get("categoria", ""),
            "cantidad": int(item_data.get("cantidad", 0)),
            "precio": float(item_data.get("precio", 0)),
            "ubicacion": item_data.get("ubicacion", ""),
            "minimo": int(item_data.get("minimo", 0)),
        }

        inventory_df = pd.concat([inventory_df, pd.DataFrame([new_row])], ignore_index=True)
        self.save_inventory(inventory_df)
        return new_row

    def dashboard(self) -> Dict[str, object]:
        inventory_df = self.load_inventory()
        total_items = len(inventory_df)
        total_quantity = int(inventory_df["cantidad"].sum()) if total_items else 0
        total_value = float((inventory_df["cantidad"] * inventory_df["precio"]).sum()) if total_items else 0.0

        low_stock_df = inventory_df[inventory_df["cantidad"] <= inventory_df["minimo"]]
        low_stock_count = len(low_stock_df)

        return {
            "total_items": total_items,
            "total_quantity": total_quantity,
            "stock_value": round(total_value, 2),
            "low_stock_count": low_stock_count,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def seed_sample_data(self) -> None:
        self._write_workbook(
            inventory_rows=self._default_inventory_rows(),
            movement_rows=self._default_movement_rows(),
            count_rows=self._default_count_rows(),
            config_rows={"version": ["1.0"], "generated_at": [datetime.utcnow()]},
        )

