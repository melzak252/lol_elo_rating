from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm.session import Session

import app.lol_games.teams.models as team_model
from db import engine, get_db
import app.lol_games.teams.schemas as _schemas
import app.lol_games.teams.db as team_db

router = APIRouter(
    prefix="/teams",
    tags=["teams"]
)

team_model.Base.metadata.create_all(engine)


# Create team
@router.post("/team", response_model=_schemas.TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(request: _schemas.TeamCreate, db: Session = Depends(get_db)) -> _schemas.TeamResponse:
    created_team, team_in_db = team_db.create_team(db, request)
    return created_team


# Read teams
@router.get("/teams", response_model=List[_schemas.TeamResponse], status_code=status.HTTP_200_OK)
async def get_all_teams(db: Session = Depends(get_db)):
    return team_db.get_teams(db)


@router.get("/team/{id}", response_model=_schemas.TeamResponse, status_code=status.HTTP_200_OK)
async def get_teams_by_id(id: int, db: Session = Depends(get_db)):
    return team_db.get_team_by_id(id, db)


# Update team
@router.post("/team/{id}/update", response_model=_schemas.TeamResponse, status_code=status.HTTP_201_CREATED)
def update_team(id: int, request: _schemas.TeamCreate, db: Session = Depends(get_db)):
    return team_db.update_team(id, db, request)


# Delete team
@router.delete("/team/{id}/delete", response_model=_schemas.TeamResponse, status_code=status.HTTP_200_OK)
def delete_team(id: int, db: Session = Depends(get_db)):
    return team_db.delete_team(id, db)
