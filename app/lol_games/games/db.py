from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
import app.lol_games.games.schemas as _schemas
import app.lol_games.games.models as _models


def create_game(db: Session, request: _schemas.PlayerCreate):
    game_in_db = db.query(_models.Player).filter(_models.Player.nick == request.nick).first()
    if game_in_db is not None:
        request.unique_nick = f"{request.nick} ({request.full_name})"

    new_game = _models.Player(
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

    db.add(new_game)
    db.commit()
    db.refresh(new_game)

    return new_game


def get_games(db: Session):
    return db.query(_models.Player).all()


def get_game_by_id(game_id: int, db: Session):
    return db.query(_models.Player).filter(_models.Player.id == game_id).first()


def get_game_by_unique_nick(game_nick: str, db: Session):
    return db.query(_models.Player).filter(_models.Player.unique_nick == game_nick).first()


def get_games_by_nick(game_nick: str, db: Session):
    return db.query(_models.Player).filter(_models.Player.nick == game_nick).all()


def update_game(id: int, db: Session, request: _schemas.PlayerCreate):
    game = db.query(_models.Player).filter(_models.Player.id == id)
    game.update(_models.Player(
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
    return game.all()


def delete_game(game_id: int, db: Session):
    game = db.query(_models.Player).filter(_models.Player.id == game_id).first()

    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")

    db.delete(game)
    db.commit()

    return game
