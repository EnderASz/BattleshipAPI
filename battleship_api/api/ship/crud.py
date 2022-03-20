from .schemas import ShipCreate as ShipCreateSchema
from .models import Ship as ShipModel
from battleship_api.api.player.models import Player as PlayerModel

from sqlalchemy.orm import Session


def create_ship(
    db: Session,
    ship: ShipCreateSchema,
) -> ShipModel:
    """
    Creates ship instance assigned to player given via `owner` and adds it to
    the database.

    Params:
        - db: Database session
        - ship: Ship creation data represented by
            `battleship_api.api.ship.schemas.ShipCreate` schema
        - owner: Player database model instance to which ship will be assigned

    Returns:
        New ship database object instance.
    """
    db.add(new_ship := ShipModel(**ship.dict()))
    db.commit()
    db.refresh(new_ship)
    return new_ship


def get_ship(db: Session, ship_id: int) -> ShipModel | None:
    """
    Returns ship object from database searched by ship id.

    Params:
        - db (Session): Database session
        - ship_id: Ship id

    Returns:
        Ship database object instance
    """
    return db.query(ShipModel).filter(ShipModel.id == ship_id).first()


def get_ships(db: Session, limit: int, offset: int) -> list[ShipModel]:
    """
    Returns list of `limit` ships in database starting from `offset` ship.

    Params:
        - db: Database session
        - limit: Number of ships to return
        - offset: Number of ships to skip

    Returns:
        Ship list of `limit` elements starting from `offset` ship.
    """
    return db.query(ShipModel).offset(offset).limit(limit).all()
