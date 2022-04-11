from . import schemas
from .models import Shot as ShotModel

from sqlalchemy.orm import Session


def get_shot(db: Session, shot_id: int) -> ShotModel | None:
    """
    Returns shot object from database searched by shot id.

    Params:
        - db (Session): Database session
        - shot_id: Shot id

    Returns:
        Shot database object instance
    """
    return db.query(ShotModel).filter(ShotModel.id == shot_id).first()


def get_shots(db: Session, limit: int, offset: int) -> list[ShotModel]:
    """
    Returns list of `limit` shots in database starting from `offset` shot.

    Params:
        - db: Database session
        - limit: Number of shots to return
        - offset: Number of shots to skip

    Returns:
        Shot list of `limit` elements starting from `offset` shot.
    """
    return db.query(ShotModel).offset(offset).limit(limit).all()


def create_shot(db: Session, shot: schemas.ShotCreate) -> ShotModel:
    db.add(new_shot := ShotModel(**shot.dict()))
    return new_shot
