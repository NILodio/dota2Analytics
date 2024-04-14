import json
import logging

from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models import Teams, User, UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # from app.core.engine import engine
    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)

    teams = session.exec(select(Teams)).first()
    logger.info("......Teams")
    if not teams:
        logger.info("No teams")
        with open("app/assets/teams.json") as f:
            data = json.load(f)
            for team in data:
                try:
                    team_in = Teams(
                        id_team=int(team["team_id"]),
                        name_team=str(team["team_name"]),
                    )
                except Exception as e:
                    logger.error(e)
                else:
                    team = crud.create_team(session=session, team_create=team_in)
                    logger.info(f"Team {team.name_team} created")
        logger.info("Teams created")
    else:
        logger.info("Teams already created")
    session.commit()
