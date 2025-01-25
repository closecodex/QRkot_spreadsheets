from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationResponse
)

router = APIRouter()


@router.post('/', response_model=DonationResponse)
async def create_donation(
    donation_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user),
):
    return await donation_crud.create_donation_with_investment(
        donation_in, session, user
    )


@router.get('/my', response_model=list[DonationResponse])
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user),
):
    return await donation_crud.get_user_donations(session, user.id)


@router.get('/', response_model=list[DonationDB])
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
    superuser=Depends(current_superuser),
):
    return await donation_crud.get_multi(session)
