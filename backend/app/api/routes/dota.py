import logging
import random
import uuid
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
    PredictOut,
    Teams,
    TeamsOut,
)
from app.open_dota import OpenDotaAPI
from app.utils import make_prediction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


@router.get("/teams", response_model=TeamsOut)
def read_teams(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve teams.
    """

    count_statement = select(func.count()).select_from(Teams)
    count = session.exec(count_statement).one()
    if not count:
        raise HTTPException(status_code=404, detail="Teams not found")
    else:
        statement = select(Teams).offset(skip).limit(limit)
        teams = session.exec(statement).all()

    return TeamsOut(data=teams, count=count)


@router.get("/team/{id}")
def read_team(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    """
    Retrieve team info.
    """
    # check if user is superuser
    if current_user.is_superuser:
        response = _make_request(f"/teams/{id}")
        if not response:
            raise HTTPException(status_code=404, detail="teams not found")
        return response
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")


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


@router.delete("/polls")
def delete_polls(session: SessionDep, current_user: CurrentUser) -> Message:
    """
    Delete a poll.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    polls = session.query(Poll).delete()
    if not polls:
        raise HTTPException(status_code=404, detail="Polls not found")
    session.commit()
    return Message(message="Polls deleted successfully")


@router.post("/randompoll")
def random_poll(session: SessionDep, current_user: CurrentUser) -> Message:
    """
    Create a random poll.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    # Get ramdom 2 random teams from Table teams
    statement = select(Teams).order_by(func.random()).limit(2)
    teams = session.exec(statement).all()
    if not teams:
        raise HTTPException(status_code=404, detail="Teams not found")

    team_1 = teams[0]
    team_2 = teams[1]
    response = _make_request("/heroes")
    if not response:
        raise HTTPException(status_code=404, detail="Heroes not found")

    session.query(Poll).delete()

    # Get 10 random heroes from response List
    if response:
        random_heroes = random.sample(response, 10)

    ui_description = uuid.uuid4()
    for hero in range(5):
        hero_radiant_id = random_heroes[hero]["id"]
        hero_direct_id = random_heroes[hero + 5]["id"]
        hero_radiant_name = random_heroes[hero]["localized_name"]
        hero_direct_name = random_heroes[hero + 5]["localized_name"]
        poll1 = Poll(
            hero_id=hero_radiant_id,
            hero_name=hero_radiant_name,
            team=team_1.name_team,
            team_id=team_1.id_team,
            owner_id=current_user.id,
            player_name=f"Player {hero + 1}",
            description=ui_description,
        )
        session.add(poll1)
        session.commit()
        session.refresh(poll1)
        poll2 = Poll(
            hero_id=hero_direct_id,
            hero_name=hero_direct_name,
            team=team_2.name_team,
            team_id=team_2.id_team,
            owner_id=current_user.id,
            player_name=f"Player {hero + 1}",
            description=ui_description,
        )
        session.add(poll2)
        session.commit()
        session.refresh(poll2)

    session.commit()
    return Message(message="Random Polls Generated Successfully")


@router.get("/predict", response_model=PredictOut)
def predict_poll(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve predict.
    """

    open_dota = OpenDotaAPI()

    statement = (
        select(Poll).where(Poll.owner_id == current_user.id).offset(skip).limit(limit)
    )
    polls = session.exec(statement).all()

    if not polls:
        raise HTTPException(status_code=404, detail="Polls not found")

    team_ids = list(set([poll.team_id for poll in polls]))

    # Filter polls by team_id
    team_radiant_id = team_ids[0]
    team_direct_id = team_ids[1]

    heroes_radiant = [obj for obj in polls if obj.team_id == team_radiant_id]
    heroes_direct = [obj for obj in polls if obj.team_id == team_direct_id]

    predict_list = []

    for i in range(5):
        predict_list.append(heroes_radiant[i].hero_id)

    for i in range(5):
        predict_list.append(heroes_direct[i].hero_id)

    predict_list.append(team_radiant_id)
    predict_list.append(team_direct_id)

    feactures = open_dota.get_model_features_from_input(predict_list)

    output = make_prediction(feactures, "models/3_GradientBoostingClassifier.pkl")

    if output[0] == 1:
        return PredictOut(prediction=output[0], message="Radiant Wins")
    else:
        return PredictOut(prediction=output[0], message="Dire Wins")
