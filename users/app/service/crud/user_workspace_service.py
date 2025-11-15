from typing import List, Optional
from sqlalchemy.orm import Session
from app.repository.user_workspace_repository import UserWorkspaceRepository
from app.domain.models.user_workspace import UserWorkspace
from app.domain.dtos.user_workspace.user_workspace_input import (
    UserWorkspaceInput,
)
from app.utils.uuid_generator import generate_uuid


class UserWorkspaceService:
    @staticmethod
    def get_all(session: Session) -> List[UserWorkspace]:
        return UserWorkspaceRepository(session).get_all()

    @staticmethod
    def get_by_id(
        workspace_id: str,
        session: Session
    ) -> Optional[UserWorkspace]:
        return UserWorkspaceRepository(session).get_by_id(workspace_id)

    @staticmethod
    def create(data: UserWorkspaceInput, session: Session) -> UserWorkspace:
        workspace = UserWorkspace(
            user_workspace_id=generate_uuid(),
            **data.model_dump(exclude_unset=True)
        )
        return UserWorkspaceRepository(session).create(workspace)

    @staticmethod
    def update(
        workspace_id: str,
        data: UserWorkspaceInput,
        session: Session
    ) -> Optional[UserWorkspace]:
        return UserWorkspaceRepository(session).update(workspace_id, data)

    @staticmethod
    def delete(workspace_id: str, session: Session) -> bool:
        return UserWorkspaceRepository(session).delete(workspace_id)

    @staticmethod
    def bulk_insert_ignore(
        users: List[UserWorkspaceInput],
        session: Session
    ):
        """
        Inserta en bulk usuarios.
        Si hay duplicados en email_unal, MySQL los ignora.
        """
        user_models = [
            UserWorkspace(
                user_workspace_id=generate_uuid(),
                **u.model_dump(exclude_unset=True)
            )
            for u in users
        ]
        UserWorkspaceRepository(session).bulk_insert_ignore(user_models)
        return {"inserted": len(users), "duplicates_ignored": True}
