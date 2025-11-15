from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.configuration.database import get_session
from app.domain.models.user_workspace_associate import UserWorkspaceAssociate
from app.domain.dtos.user_workspace_associate.user_workspace_associate_input import (  # noqa: E501 ignora error flake8
    UserWorkspaceAssociateInput
) 
from app.service.crud.user_workspace_associate_service import (
    UserWorkspaceAssociateService
)
from app.utils.auth import get_current_user

router = APIRouter(prefix="/associates", tags=["UserWorkspaceAssociate"])


@router.post(
    "/",
    response_model=UserWorkspaceAssociate,
    status_code=status.HTTP_201_CREATED
)
def create_associate(
    data: UserWorkspaceAssociateInput,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    return UserWorkspaceAssociateService.create(data, session)


@router.get("/", response_model=List[UserWorkspaceAssociate])
def list_associates(
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    return UserWorkspaceAssociateService.get_all(session)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_associate(
    data: UserWorkspaceAssociateInput,
    session: Session = Depends(get_session),
    #user_email: str = Depends(get_current_user)
):
    deleted = UserWorkspaceAssociateService.delete(
        data.email_unal,
        data.user_workspace_id,
        data.cod_period,
        session
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Association not found")
