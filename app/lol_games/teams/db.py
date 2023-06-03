from typing import List

from unidecode import unidecode
from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
import app.lol_games.teams.schemas as _schemas
import app.lol_games.teams.models as _models


def create_team(db: Session, request: _schemas.TeamCreate):
    team_in_db = db.query(_models.Team).filter(_models.Team.unique_name == request.unique_name).first()

    new_team = _models.Team(
        unique_name=request.unique_name,
        name=request.name,
        short_name=request.short_name,
        region=request.region,
        location=request.location,
        team_location=request.team_location,
        is_disbanded=request.is_disbanded,
        img_name=request.img_name
    )

    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    return new_team, team_in_db


def get_teams(db: Session):
    return db.query(_models.Team).all()


def get_team_by_id(team_id: int, db: Session):
    return db.query(_models.Team).filter(_models.Team.id == team_id).first()


def get_team_by_unique_name(team_name: str, db: Session):
    team_name = unidecode(team_name).lower()
    return db.query(_models.Team).filter(_models.Team.unique_name == team_name).first()


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


def create_team_rename(db: Session, request: _schemas.TeamRenameCreate):
    next_team_renames: List[_models.TeamRename] = db.query(_models.TeamRename).filter(
        _models.TeamRename.prev_name == request.new_name).all()

    if len(next_team_renames) > 1:
        print(f"Reauest: {request}")

    prev_team = get_team_by_unique_name(request.prev_name, db)
    new_team = get_team_by_unique_name(request.new_name, db)

    if not next_team_renames:
        next_team_rename = new_team.id if new_team is not None else None
    else:
        next_team_rename = next_team_renames.pop().actual_team_id

    new_team_rename = _models.TeamRename(
        prev_team_id=prev_team.id if prev_team is not None else None,
        new_team_id=new_team.id if new_team is not None else None,
        actual_team_id=next_team_rename if next_team_rename is not None else None,
        prev_name=request.prev_name,
        new_name=request.new_name,
        team_changed=request.team_changed,
        date=request.date,
        change_type=request.change_type
    )

    db.add(new_team_rename)
    db.commit()
    db.refresh(new_team_rename)

    return next_team_rename
