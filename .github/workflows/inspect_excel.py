import pandas as pd
from pathlib import Path

try:
    # Use temp file to avoid lock
    file_path = Path("datos/temp_data.xlsx")
    
    # Check sheets first
    xl = pd.ExcelFile(file_path)
    print(f"Sheets: {xl.sheet_names}")
    
    # Read REPORTE_WMS
    df = pd.read_excel(file_path, sheet_name="REPORTE_WMS", nrows=5)
    print("\nColumns:")
    print(df.columns.tolist())
    
    print("\nSample Data:")
    print(df.head(2).to_string())
except Exception as e:
    print(f"Error: {e}")
