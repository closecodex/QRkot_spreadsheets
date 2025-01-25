from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
    CharityProjectDB,
)
from app.api.validators import (
    check_charity_project_name_is_available,
    validate_not_fully_invested,
    validate_full_amount,
    validate_project_for_deletion,
)
from app.crud.donation import donation_crud

router = APIRouter()


@router.post('/', response_model=CharityProjectDB)
async def create_charity_project(
    project_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
    superuser=Depends(current_superuser),
):
    await check_charity_project_name_is_available(project_in.name, session)
    open_donations = await donation_crud.get_open(session)
    return await charity_project_crud.create_with_investments(
        project_in, open_donations, session
    )


@router.get('/', response_model=list[CharityProjectDB])
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.patch('/{project_id}', response_model=CharityProjectDB)
async def update_charity_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_superuser),
):
    db_project = await session.get(CharityProject, project_id)
    if not db_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Project not found'
        )

    forbidden_updates = {
        'invested_amount', 'create_date', 'close_date', 'fully_invested'
    }
    update_data = project_in.dict(exclude_unset=True)
    if any(field in forbidden_updates for field in update_data):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Attempt to update restricted fields'
        )
    validate_not_fully_invested(db_project)
    if 'full_amount' in update_data:
        validate_full_amount(
            project_in.full_amount, db_project.invested_amount
        )
    if 'name' in update_data:
        await check_charity_project_name_is_available(
            name=project_in.name, session=session, project_id=project_id
        )
    return await charity_project_crud.update(
        db_obj=db_project,
        obj_in=project_in,
        session=session
    )


@router.delete('/{project_id}', response_model=CharityProjectDB)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_superuser),
):
    project = await charity_project_crud.get(project_id, session)
    validate_project_for_deletion(project)
    deleted_project = await charity_project_crud.delete_charity_project(
        project, session
    )
    return deleted_project
