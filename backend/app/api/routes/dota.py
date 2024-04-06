from typing import Any

import requests
from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.core.config import settings
from app.models import (
    DotaHeroes,
    Message,
    Poll,
    PollCreate,
    PollOut,
    PollsOut,
    PollUpdate,
)

router = APIRouter()


def _make_request(endpoint):
    """
    Make a request to the OpenDota API.

    Args:
        endpoint (str): The API endpoint.

    Returns:
        list: Response from the API.
    """
    url = f"{settings.OPEN_DOTA_API_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    params = {"api_key": settings.OPEN_DOTA_KEY}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {}


@router.get("/heroes", response_model=DotaHeroes)
def read_heroes(
    session: SessionDep, current_user: CurrentUser, limit: int = 100
) -> Any:
    """
    Retrieve Heroes.
    """
    # check if user is superuser
    if current_user.is_superuser:
        response = _make_request("/heroes")
        if not response:
            raise HTTPException(status_code=404, detail="Heroes not found")
        return DotaHeroes(data=response, count=len(response))
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")


@router.get("/polls", response_model=PollsOut)
def read_polls(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve polls.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Poll)
        count = session.exec(count_statement).one()
        statement = select(Poll).offset(skip).limit(limit)
        polls = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Poll)
            .where(Poll.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Poll)
            .where(Poll.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        polls = session.exec(statement).all()

    return PollsOut(data=polls, count=count)


@router.get("/poll/{id}", response_model=PollOut)
def read_poll(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    """
    Get poll by ID.
    """
    poll = session.get(Poll, id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    if not current_user.is_superuser and (poll.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return poll


@router.post("/poll", response_model=PollOut)
def create_poll(
    *, session: SessionDep, current_user: CurrentUser, poll_in: PollCreate
) -> Any:
    """
    Create new poll.
    """
    poll = Poll.model_validate(poll_in, update={"owner_id": current_user.id})
    session.add(poll)
    session.commit()
    session.refresh(poll)
    return poll


@router.put("/poll/{id}", response_model=PollOut)
def update_poll(
    *, session: SessionDep, current_user: CurrentUser, id: int, poll_in: PollUpdate
) -> Any:
    """
    Update an poll.
    """
    poll = session.get(Poll, id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    if not current_user.is_superuser and (poll.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = poll_in.model_dump(exclude_unset=True)
    poll.sqlmodel_update(update_dict)
    session.add(poll)
    session.commit()
    session.refresh(poll)
    return poll


@router.delete("/poll/{id}")
def delete_poll(session: SessionDep, current_user: CurrentUser, id: int) -> Message:
    """
    Delete an poll.
    """
    poll = session.get(Poll, id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    if not current_user.is_superuser and (poll.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(poll)
    session.commit()
    return Message(message="Poll deleted successfully")
