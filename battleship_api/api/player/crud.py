from sqlalchemy.orm import Session

from battleship_api.api.player.models import Player as PlayerModel
from battleship_api.api.board.models import Board as BoardModel


def create_player(
    db: Session,
    board: BoardModel,
) -> PlayerModel:
    """Creates player instance, assignes and adds it to the database.

    Params:
        - db: Database session
        - board: Board data represented by
            `battleship_api.api.board.schemas.Board` schema

    Returns:
        New player database object instance.
    """
    board.players.append(player := PlayerModel())
    db.commit()
    db.refresh(player)
    return player


def get_player(db: Session, player_id: int) -> PlayerModel | None:
    """
    Returns player object from database searched by player id.

    Params:
        - db: Database session
        - player_id: Player id

    Returns:
        Player database object instance.
    """
    return db.query(PlayerModel).filter(PlayerModel.id == player_id).first()


def get_players(
    db: Session,
    limit: int,
    offset: int
) -> list[PlayerModel]:
    """
    Returns list of 'limit' players in database starting from `offset` player.

    Params:
        db: Database session
        - limit: Number of players to return
        - offset: Number of players to skip

    Returns:
        Player list of 'limit' elements starting from 'offset' database.s
    """
    return db.query(PlayerModel).offset(offset).limit(limit).all()


def delete_player(db: Session, player_id: int):
    """
    Removes player from the database and returns number of deleted players.
    In this case it always be 0 (if player remove was not successful) or 1 (if player remove was successful).

    Params:
        - db: Database session
        - player_id: Player id

    Returns:
        If remove was successful - `1`
        If remove was not successful - `0`
    """
    player = db.query(PlayerModel).filter(PlayerModel.id == player_id)
    deleted = player.delete()
    db.commit()
    return deleted
