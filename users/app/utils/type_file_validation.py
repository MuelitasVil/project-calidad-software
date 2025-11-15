from fastapi import HTTPException
from io import BytesIO
from fastapi import UploadFile
from openpyxl import load_workbook, Workbook


async def readExcelFile(file: UploadFile) -> Workbook:
    try:
        if not file.filename.endswith((".xlsx", ".xlsm")):
            raise HTTPException(
                status_code=400,
                detail="El archivo debe ser .xlsx o .xlsm"
            )

        contents = await file.read()
        excel_io = BytesIO(contents)
        wb: Workbook = load_workbook(excel_io)
        return wb

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar el archivo: {str(e)}"
        )
