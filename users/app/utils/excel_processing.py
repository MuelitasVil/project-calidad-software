from openpyxl.cell.cell import Cell
from typing import Any, Tuple


def is_blank(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v.strip() == "")


def get_file_text(v: Any) -> str:
    return "" if v is None else str(v).strip()


def get_value_from_row(row: Tuple[Cell, ...], col_idx: int) -> str:
    # La columna es 1-indexada
    return get_file_text(row[col_idx - 1].value)
