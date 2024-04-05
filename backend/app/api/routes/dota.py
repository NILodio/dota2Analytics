from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import CurrentUser, SessionDep
import requests
from app.api.deps import get_current_active_superuser
from typing import Any
from app.models import DotaHeroes
from app.core.config import settings
router = APIRouter()


def _make_request(base_url, endpoint):
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
        print(response.json())
        return response.json()
    else:
        return {}


@router.get("/heroes", response_model=list[DotaHeroes])
def read_heroes(
    session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Retrieve Heroes.
    """

    # check if user is superuser
    if current_user.is_superuser:
        response = _make_request(settings.OPEN_DOTA_API_URL, "/heroes")
        if not response:
            raise HTTPException(status_code=404, detail="Heroes not found")
        return response
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")