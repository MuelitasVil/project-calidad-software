from typing import Dict, Any, List, Tuple, Set
from fastapi import HTTPException
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell
from sqlmodel import Session

from app.domain.dtos.school_headquarters_associate.school_headquarters_associate_input import (  # noqa: E501 ignora error flake8
    SchoolHeadquartersAssociateInput,
)
from app.domain.dtos.unit_school_associate.unit_school_associate_input import ( 
    UnitSchoolAssociateInput,
)

from app.domain.dtos.user_unit_associate.user_unit_associate_input import (
    UserUnitAssociateInput,
)

from app.service.crud.school_headquarters_associate_service import (
    SchoolHeadquartersAssociateService
)

from app.service.crud.unit_school_associate_service import (
    UnitSchoolAssociateService
)

from app.service.crud.user_unit_associate_service import (
    UserUnitAssociateService,
)

from app.utils.excel_processing import (
    get_value_from_row,
    is_blank,
    )

from app.domain.dtos.user_unal.user_unal_input import UserUnalInput
from app.domain.dtos.unit_unal.unit_unal_input import UnitUnalInput
from app.domain.dtos.school.school_input import SchoolInput
from app.domain.dtos.headquarters.headquarters_input import HeadquartersInput

from app.domain.enums.files.general import General_Values
from app.domain.enums.files.estudiante_activos import (
    EstudianteActivos,
    TypesEstudiante
)

from app.service.crud.user_unal_service import UserUnalService
from app.service.crud.unit_unal_service import UnitUnalService
from app.service.crud.school_service import SchoolService
from app.service.crud.headquarters_service import HeadquartersService

from app.utils.app_logger import AppLogger

logger = AppLogger(__file__)
logger2 = AppLogger(__file__, "user_unit_association.log")


# --------- validación principal y armado de colecciones ---------
def case_estudiantes_activos(
    ws: Worksheet,
    cod_period: str,
    session: Session
) -> Dict[str, Any]:
    """
    - Valida filas vacías y celdas vacías (según Enum).
    - Construye listas de DTOs (sin duplicados por código).
    - Devuelve resumen: status, errores, conteos y previews.
    """
    errors: List[Dict[str, Any]] = []
    users: List[UserUnalInput] = []
    units: List[UnitUnalInput] = []
    schools: List[SchoolInput] = []
    headquarters: List[HeadquartersInput] = []
    userUnitAssocs: List[UserUnitAssociateInput] = []
    unitSchoolAssocs: List[UnitSchoolAssociateInput] = []
    schoolHeadquartersAssocs: List[SchoolHeadquartersAssociateInput] = []

    seen_units: Set[str] = set()
    seen_schools: Set[str] = set()
    seen_heads: Set[str] = set()
    seen_users: Set[str] = set()
    seen_user_unit_assocs: Set[str] = set()
    seen_unit_school_assocs: Set[str] = set()
    seen_school_head_assocs: Set[str] = set()

    logger.info("Iniciando procesamiento de archivo de estudiantes activos")
    # recorre todas las filas (incluye encabezados en row 1)
    for row_idx, row in enumerate(ws.iter_rows(), start=1):
        logger.debug(f"Procesando fila {row_idx}")
        logger.debug(f"Contenido de la fila: {[cell.value for cell in row]}")

        if row_idx == 1:
            continue

        if is_row_blank(row):
            errors.append({
                "row": row_idx,
                "column": None,
                "message": "Fila completamente vacía"
            })
            continue

        errors.extend(get_blank_cell_errors(row, row_idx))

        # construir DTOs de la fila
        row_tuple: Tuple[Cell, ...] = row  # tipado explícito

        user: UserUnalInput = get_user_from_row(row_tuple)
        if user.email_unal and user.email_unal not in seen_users:
            users.append(user)
            seen_users.add(user.email_unal)
            logger.debug(f"Usuario agregado: {user}")
        else:
            logger.warning(f"Usuario duplicado encontrado: {user.email_unal}")

        unit: UnitUnalInput = get_unit_from_row(row_tuple)
        if unit.cod_unit and unit.cod_unit not in seen_units:
            units.append(unit)
            seen_units.add(unit.cod_unit)
            logger.debug(f"Plan agregada: {unit}")
        else:
            logger.warning(f"Plan duplicada encontrada: {unit.cod_unit}")

        school: SchoolInput = get_school_from_row(row_tuple)
        if school.cod_school and school.cod_school not in seen_schools:
            schools.append(school)
            seen_schools.add(school.cod_school)
            logger.debug(f"Facultad agregada: {school}")
        else:
            logger.warning(
                f"Facultad duplicada encontrada: {school.cod_school}"
            )

        head: HeadquartersInput = get_headquarters_from_row(row_tuple)
        if head.cod_headquarters and head.cod_headquarters not in seen_heads:
            headquarters.append(head)
            seen_heads.add(head.cod_headquarters)
            logger.debug(
                f"Sede administrativa agregada: {head}"
            )
        else:
            logger.warning(
                f"Sede administrativa duplicada encontrada: "
                f"{head.cod_headquarters}"
            )

        userUnitAssoc: UserUnitAssociateInput = UserUnitAssociateInput(
            email_unal=user.email_unal,
            cod_unit=unit.cod_unit,
            cod_period=cod_period
        )
        if (
            f"{user.email_unal}{unit.cod_unit}{cod_period}"
            not in seen_user_unit_assocs
        ):
            seen_user_unit_assocs.add(
                f"{user.email_unal}{unit.cod_unit}{cod_period}"
            )
            userUnitAssocs.append(userUnitAssoc)
            logger.debug(
                f"Asociación de usuario a plan agregada: "
                f"{userUnitAssoc}"
            )
        else:
            logger.warning(
                f"Asociación de usuario a plan duplicada encontrada: "
                f"{user.email_unal}, {unit.cod_unit}, {cod_period}"
            )

        logger2.debug(f"Asociación de usuario a plan: {userUnitAssoc}")

        unitSchoolAssoc = UnitSchoolAssociateInput(
            cod_unit=unit.cod_unit,
            cod_school=school.cod_school,
            cod_period=cod_period
        )
        if (
            f"{unit.cod_unit}{school.cod_school}{cod_period}"
            not in seen_unit_school_assocs
        ):
            seen_unit_school_assocs.add(
                f"{unit.cod_unit}{school.cod_school}{cod_period}"
            )
            unitSchoolAssocs.append(unitSchoolAssoc)
            logger.debug(
                f"Asociación de plan a facultad agregada: "
                f"{unitSchoolAssoc}"
            )
        else:
            logger.warning(
                "Asociación de plan a facultad duplicada encontrada: "
                f"{unitSchoolAssoc.cod_period} "
                f"{unitSchoolAssoc.cod_unit} "
                f"{unitSchoolAssoc.cod_school}"
            )

        schoolHeadAssoc = SchoolHeadquartersAssociateInput(
            cod_school=school.cod_school,
            cod_headquarters=head.cod_headquarters,
            cod_period=cod_period
        )
        if (
            f"{school.cod_school}{head.cod_headquarters}{cod_period}"
            not in seen_school_head_assocs
        ):
            seen_school_head_assocs.add(
                f"{school.cod_school}{head.cod_headquarters}{cod_period}"
            )
            schoolHeadquartersAssocs.append(schoolHeadAssoc)
            logger.debug(
                f"Asociación de facultad a sede agregada: "
                f"{schoolHeadAssoc}"
            )
        else:
            logger.warning(
                f"Asociación de facultad a sede duplicada encontrada: "
                f"{schoolHeadAssoc.cod_school}, "
                f"{schoolHeadAssoc.cod_headquarters}, "
                f"{schoolHeadAssoc.cod_period}"
            )

    if errors:
        raise HTTPException(status_code=400, detail={
            "status": False,
            "errors": errors
        })

    resUsers = UserUnalService.bulk_insert_ignore(users, session)
    resUnits = UnitUnalService.bulk_insert_ignore(units, session)
    resSchools = SchoolService.bulk_insert_ignore(schools, session)
    resHeadquarters = HeadquartersService.bulk_insert_ignore(
        headquarters,
        session
    )
    resUserUnitAssocs = UserUnitAssociateService.bulk_insert_ignore(
        userUnitAssocs,
        session
    )
    resUnitSchoolAssocs = UnitSchoolAssociateService.bulk_insert_ignore(
        unitSchoolAssocs,
        session
    )
    resSchoolHeadquartersAssocs = SchoolHeadquartersAssociateService.bulk_insert_ignore(  # noqa: E501 ignora error flake8
        schoolHeadquartersAssocs,
        session
    )   

    logger.info(f"Resultados de inserción users: {resUsers}")
    logger.info(f"Resultados de inserción units: {resUnits}")
    logger.info(f"Resultados de inserción schools: {resSchools}")
    logger.info(f"Resultados de inserción headquarters: {resHeadquarters}")
    logger.info(
        f"Resultados de inserción user_unit_assocs: {resUserUnitAssocs}"
    )
    logger.info(
        f"Resultados de inserción unit_school_assocs: {resUnitSchoolAssocs}"
    )
    logger.info(
        f"Resultados de inserción school_headquarters_assocs: "
        f"{resSchoolHeadquartersAssocs}"
    )

    for userUserAssoc in userUnitAssocs:
        logger.info(f"Asociación de usuario a plan: {userUserAssoc}")

    return {
        "status": True,
        "cant_users": len(users),
        "cant_units": len(units),
        "cant_schools": len(schools),
        "cant_headquarters": len(headquarters),
        "cant_user_unit_assocs": len(userUnitAssocs),
        "cant_unit_school_assocs": len(unitSchoolAssocs),
        "cant_school_head_assocs": len(schoolHeadquartersAssocs),
    }


def get_user_from_row(row: Tuple[Cell, ...]) -> UserUnalInput:
    return UserUnalInput(
        email_unal=(
            get_value_from_row(row, EstudianteActivos.EMAIL.value) or None
        ),
        document=None,
        name=None,
        lastname=None,
        full_name=(
            get_value_from_row(
                row, EstudianteActivos.NOMBRES_APELLIDOS.value
            ) or None
        ),
        gender=None,
        birth_date=None,
    )


def get_unit_from_row(row: Tuple[Cell, ...]) -> UnitUnalInput:
    cod_unit: str = get_value_from_row(row, EstudianteActivos.COD_PLAN.value)
    plan: str = get_value_from_row(row, EstudianteActivos.PLAN.value)
    tipo_nivel: str = get_value_from_row(
        row, EstudianteActivos.TIPO_NIVEL.value
    )
    email: str = f"{cod_unit}@unal.edu.co"
    return UnitUnalInput(
        cod_unit=cod_unit,
        email=email,
        name=plan or None,
        description=None,
        type_unit=tipo_nivel or None,
    )


def get_school_from_row(row: Tuple[Cell, ...]) -> SchoolInput:
    facultad: str = get_value_from_row(row, EstudianteActivos.FACULTAD.value)
    sede: str = get_value_from_row(row, EstudianteActivos.SEDE.value)
    tipoEstudiante: str = get_value_from_row(
        row, EstudianteActivos.TIPO_NIVEL.value
    )
    prefix_sede: str = sede.split(" ")[1][:3].lower()

    logger.debug(f"Facultad: {facultad}, Sede: {sede}, Tipo: {tipoEstudiante}")

    if tipoEstudiante == General_Values.PREGRADO.value:
        logger.debug("Tipo de estudiante es pregrado")
        tipoEstudiante = "pre"
    elif tipoEstudiante == General_Values.POSGRADO.value:
        logger.debug("Tipo de estudiante es posgrado")
        tipoEstudiante = "pos"

    cod_school: str = ""
    if (
        sede == TypesEstudiante.SEDE_AMAZONIA or
        sede == TypesEstudiante.SEDE_CARIBE or
        sede == TypesEstudiante.SEDE_ORINOQUÍA or
        sede == TypesEstudiante.SEDE_TUMACO or
        sede == TypesEstudiante.SEDE_DE_LA_PAZ
    ):
        cod_school = f"estf{tipoEstudiante}{prefix_sede}"
    else:
        acronimo = "".join(
            p[0].lower() for p in facultad.split() if len(p) > 2
        )
        cod_school = f"est{acronimo}{tipoEstudiante}_{prefix_sede}"

    email: str = f"{cod_school}@unal.edu.co"
    return SchoolInput(
        cod_school=cod_school,
        email=email,
        name=facultad or None,
        description=None,
        type_facultad=None,
    )


def get_headquarters_from_row(row: Tuple[Cell, ...]) -> HeadquartersInput:
    sede: str = get_value_from_row(row, EstudianteActivos.SEDE.value)
    tipoEstudiante: str = get_value_from_row(
        row, EstudianteActivos.TIPO_NIVEL.value
    )

    if tipoEstudiante == General_Values.PREGRADO.value:
        tipoEstudiante = "pre"
    elif tipoEstudiante == General_Values.POSGRADO.value:
        tipoEstudiante = "pos"

    prefix_sede: str = sede.split(" ")[1][:3].lower()
    cod_sede: str = f"estudiante{tipoEstudiante}_{prefix_sede}"
    type_facultad: str = f"estudiante_{prefix_sede}"

    email: str = f"{cod_sede}@unal.edu.co"

    return HeadquartersInput(
        cod_headquarters=cod_sede,
        email=email,
        name=sede,
        description=None,
        type_facultad=type_facultad,
    )


def is_row_blank(row: Tuple[Cell, ...]) -> bool:
    """Retorna True si todas las columnas del Enum están vacías."""
    cells = [
        row[EstudianteActivos.NOMBRES_APELLIDOS.value - 1].value,
        row[EstudianteActivos.EMAIL.value - 1].value,
        row[EstudianteActivos.SEDE.value - 1].value,
        row[EstudianteActivos.FACULTAD.value - 1].value,
        row[EstudianteActivos.COD_PLAN.value - 1].value,
        row[EstudianteActivos.PLAN.value - 1].value,
        row[EstudianteActivos.TIPO_NIVEL.value - 1].value,
    ]
    return all(is_blank(v) for v in cells)


def get_blank_cell_errors(
    row: Tuple[Cell, ...], row_idx: int
) -> List[Dict[str, Any]]:
    """Retorna lista de errores por celdas vacías en la fila."""
    col_names = [
        "NOMBRES_APELLIDOS",
        "EMAIL",
        "SEDE",
        "FACULTAD",
        "COD_PLAN",
        "PLAN",
        "TIPO_NIVEL",
    ]
    cells = [
        row[EstudianteActivos.NOMBRES_APELLIDOS.value - 1].value,
        row[EstudianteActivos.EMAIL.value - 1].value,
        row[EstudianteActivos.SEDE.value - 1].value,
        row[EstudianteActivos.FACULTAD.value - 1].value,
        row[EstudianteActivos.COD_PLAN.value - 1].value,
        row[EstudianteActivos.PLAN.value - 1].value,
        row[EstudianteActivos.TIPO_NIVEL.value - 1].value,
    ]

    errors: List[Dict[str, Any]] = []
    for i, v in enumerate(cells):
        if is_blank(v):
            errors.append({
                "row": row_idx,
                "column": col_names[i],
                "message": "Celda vacía"
            })
    return errors
