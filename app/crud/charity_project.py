from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate
)
from app.services.investment import process_investment
from .base import CRUDBase


class CharityProjectCRUD(
    CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate]
):
    """CRUD-операции для CharityProject."""

    async def create_with_investments(
        self,
        obj_in: CharityProjectCreate,
        open_donations: list,
        session: AsyncSession
    ) -> CharityProject:
        new_project = self.model(**obj_in.dict())
        session.add(new_project)
        session.add_all(process_investment(new_project, open_donations))
        await session.commit()
        await session.refresh(new_project)
        return new_project

    async def delete_charity_project(
        self,
        db_obj,
        session: AsyncSession
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_charity_project_by_name(
        self, name: str, session: AsyncSession
    ) -> Optional[CharityProject]:
        return (
            await session.execute(
                select(self.model).where(self.model.name == name)
            )
        ).scalars().first()

    async def get_projects_by_completion_rate(
        self, session: AsyncSession
    ) -> list[CharityProject]:
        """Закрытые проекты, отсортированные по времени сбора средств."""
        charity_projects = await session.execute(
            select(self.model).where(
                self.model.fully_invested.is_(True)
            ).order_by(
                (self.model.close_date - self.model.create_date)
            )
        )
        return charity_projects.scalars().all()


charity_project_crud = CharityProjectCRUD(CharityProject)
