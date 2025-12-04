from typing import List, Optional
from sqlmodel import Session

from app.repository.user_contact_data_repository import UserContactDataRepository
from app.domain.models.user_contact_data import UserContactData
from app.domain.dtos.user_contact_data.user_contact_data_input import UserContactDataInput
from app.domain.dtos.user_contact_data.user_contact_data_update import UserContactDataUpdate
from app.domain.dtos.user_contact_data.user_contact_data_sync import UserContactDataSync


class UserContactDataService:
    @staticmethod
    def get_all(session: Session) -> List[UserContactData]:
        return UserContactDataRepository(session).get_all()

    @staticmethod
    def get_by_id(contact_id: int, session: Session) -> Optional[UserContactData]:
        return UserContactDataRepository(session).get_by_id(contact_id)

    @staticmethod
    def get_by_user_email(email_unal: str, session: Session) -> List[UserContactData]:
        return UserContactDataRepository(session).get_by_user_email(email_unal)

    @staticmethod
    def create(input_data: UserContactDataInput, session: Session) -> UserContactData:
        contact = UserContactData(**input_data.model_dump(exclude_unset=True))
        return UserContactDataRepository(session).create(contact)

    @staticmethod
    def update(
        contact_id: int,
        input_data: UserContactDataUpdate,
        session: Session
    ) -> Optional[UserContactData]:
        return UserContactDataRepository(session).update(contact_id, input_data)

    @staticmethod
    def delete(contact_id: int, session: Session) -> bool:
        return UserContactDataRepository(session).delete(contact_id)

    @staticmethod
    def create_bulk(contacts: List[UserContactDataInput], session: Session) -> List[UserContactData]:
        """Crear múltiples contactos en una sola operación"""
        repository = UserContactDataRepository(session)
        created_contacts = []
        for i, contact_data in enumerate(contacts):
            print(f"Creating contact {i+1}: {contact_data.model_dump()}")
            contact = UserContactData(**contact_data.model_dump())
            created = repository.create(contact)
            print(f"Created contact with ID: {created.id}")
            created_contacts.append(created)
        print(f"Total contacts created: {len(created_contacts)}")
        return created_contacts

    @staticmethod
    def sync_user_contacts(
        email_unal: str,
        contacts: List[UserContactDataSync],
        session: Session
    ) -> List[UserContactData]:
        """
        Sincroniza los contactos de un usuario:
        - Elimina todos los contactos existentes
        - Crea los nuevos contactos recibidos
        """
        repository = UserContactDataRepository(session)
        
        # Eliminar todos los contactos existentes del usuario
        existing_contacts = repository.get_by_user_email(email_unal)
        for contact in existing_contacts:
            repository.delete(contact.id)
        
        # Crear los nuevos contactos
        created_contacts = []
        for contact_data in contacts:
            # Asegurar que el email_unal sea el correcto
            contact_dict = contact_data.model_dump()
            contact_dict['email_unal'] = email_unal
            contact = UserContactData(**contact_dict)
            created = repository.create(contact)
            created_contacts.append(created)
        
        return created_contacts
