from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
import app.lol_games.players.schemas as _schemas
import app.lol_games.players.models as _models


def create_player(db: Session, request: _schemas.PlayerCreate):
    player_in_db = db.query(_models.Player).filter(_models.Player.nick == request.nick).first()
    if player_in_db is not None:
        request.unique_nick = f"{request.nick} ({request.full_name})"

    new_player = _models.Player(
        nick=request.nick,
        unique_nick=request.unique_nick,
        full_name=request.full_name,
        country=request.country,
        residency=request.residency,
        age=request.age,
        birthdate=request.birthdate,
        actual_team_id=request.actual_team_id,
        retired=request.retired,
        main_position=request.main_position,
    )

    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    return new_player


def get_players(db: Session):
    return db.query(_models.Player).all()


def get_player_by_id(player_id: int, db: Session):
    return db.query(_models.Player).filter(_models.Player.id == player_id).first()


def get_player_by_unique_nick(player_nick: str, db: Session):
    return db.query(_models.Player).filter(_models.Player.unique_nick == player_nick).first()


def get_players_by_nick(player_nick: str, db: Session):
    return db.query(_models.Player).filter(_models.Player.nick == player_nick).all()


def update_player(id: int, db: Session, request: _schemas.PlayerCreate):
    player = db.query(_models.Player).filter(_models.Player.id == id)
    player.update(_models.Player(
        nick=request.nick,
        unique_nick=request.unique_nick,
        full_name=request.full_name,
        country=request.country,
        residency=request.residency,
        age=request.age,
        birthdate=request.birthdate,
        actual_team_id=request.actual_team_id,
        retired=request.retired,
        main_position=request.main_position,
    ))
    db.commit()
    return player.all()


def delete_player(player_id: int, db: Session):
    player = db.query(_models.Player).filter(_models.Player.id == player_id).first()

    if player is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")

    db.delete(player)
    db.commit()

    return player
