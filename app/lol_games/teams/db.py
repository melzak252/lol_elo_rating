from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
import app.lol_games.teams.schemas as _schemas
import app.lol_games.teams.models as _models


def create_team(db: Session, request: _schemas.TeamCreate):
    team_in_db = db.query(_models.Team).filter(_models.Team.name == request.name).first()

    new_team = _models.Team(
        name=request.name,
        short_name=request.short_name,
        region=request.region,
        location=request.location,
        is_disbanded=request.is_disbanded
    )

    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    return new_team, team_in_db


def get_teams(db: Session):
    return db.query(_models.Team).all()


def get_team_by_id(team_id: int, db: Session):
    return db.query(_models.Team).filter(_models.Team.id == team_id).first()


def get_team_by_name(team_name: str, db: Session):
    return db.query(_models.Team).filter(_models.Team.name == team_name).first()


def get_teams_by_name(team_name: str, db: Session):
    return db.query(_models.Team).filter(_models.Team.name == team_name).all()


def update_team(id: int, db: Session, request: _schemas.TeamCreate):
    team = db.query(_models.Team).filter(_models.Team.id == id)
    team.update(_models.Team(
        name=request.name,
        short_name=request.short_name,
        region=request.region,
        location=request.location,
        is_disbanded=request.is_disbanded
    ))
    db.commit()
    return team.all()


def delete_team(id: int, db: Session):
    team = db.query(_models.Team).filter(_models.Team.id == id).first()

    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    db.delete(team)
    db.commit()

    return team
