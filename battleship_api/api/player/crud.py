from sqlalchemy.orm import Session

from battleship_api.api.player.models import Player as PlayerModel
from battleship_api.api.board.models import Board as BoardModel


def create_player(
    db: Session,
    board: BoardModel,
) -> PlayerModel:
    board.players.append(player := PlayerModel())
    db.commit()
    db.refresh(player)
    return player


def get_player(db: Session, player_id: int) -> PlayerModel | None:
    return db.query(PlayerModel).filter(PlayerModel.id == player_id).first()


def get_players(
    db: Session,
    limit: int,
    offset: int
) -> list[PlayerModel]:
    return db.query(PlayerModel).offset(offset).limit(limit).all()


def delete_player(db: Session, player_id: int):
    player = db.query(PlayerModel).filter(PlayerModel.id == player_id)
    deleted = player.delete()
    db.commit()
    return deleted
