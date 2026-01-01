from __future__ import annotations

from inventory_service import InventoryService


def main() -> None:
    service = InventoryService()
    service.seed_sample_data()
    print(f"Datos de ejemplo generados en {service.data_path}")


if __name__ == "__main__":
    main()

