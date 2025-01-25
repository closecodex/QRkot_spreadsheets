from app.crud.charity_project import charity_project_crud
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationUpdate
from app.services.investment import process_investment
from .base import CRUDBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class DonationCRUD(CRUDBase[Donation, DonationCreate, DonationUpdate]):
    """CRUD для модели Donation."""

    async def create_donation_with_investment(
        self,
        donation_in: DonationCreate,
        session: AsyncSession,
        user: User,
    ) -> Donation:
        new_donation = await self.create(donation_in, session, user=user)
        open_projects = await charity_project_crud.get_open(session)
        session.add_all(process_investment(new_donation, open_projects))
        await session.commit()
        await session.refresh(new_donation)
        return new_donation

    async def get_user_donations(
        self, session: AsyncSession, user_id: int
    ) -> list[Donation]:
        return (
            await session.execute(
                select(Donation)
                .where(Donation.user_id == user_id)
                .order_by(Donation.create_date)
            )
        ).scalars().all()


donation_crud = DonationCRUD(Donation)
