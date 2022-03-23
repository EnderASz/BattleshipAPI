from pydantic import BaseModel as BaseSchema

from enum import Enum

from . import schemas
from .models import Ship as ShipModel


class Orientation(Enum):
    vertical = 0
    horizontal = 1


class Point(BaseSchema):
    x: int
    y: int


def get_ship_cords(
    ship: schemas.ShipLocation | ShipModel
) -> tuple[Point, Point]:
    """
    Returns points of start and end of a given ship in a tuple.

    Args:
        - ship: Object containing ship location

    Returns:
        Tuple of start and end points of a ship.
    """
    ship_start = Point(ship.column, ship.row)
    if ship.orientation == Orientation.horizontal:
        return (
            ship_start,
            Point(ship.column+ship.length-1, ship.row))
    return (
        ship_start,
        Point(ship.column, ship.row+ship.length-1))


def is_ship(
    column: int,
    row: int,
    ships: list[schemas.ShipLocation | ShipModel]
):
    """
    Checks if at given location (column and row) exists any ship from given
    list. If exists, returns True, otherwise False.

    Params:
        - column: Board column number
        - row: Board row number
        - ships: List of ships

    Returns:
        True if any given ship exists at given location, otherwise False.
    """

    ship_start, ship_end = get_ship_cords(ship)

    for ship in ships:
        if (
            ship_start.x <= column <= ship_end.x
            and ship_start.y <= row <= ship_end.y
        ):
            return True
    return False


def ships_collides(
    first: schemas.ShipLocation | ShipModel,
    second: schemas.ShipLocation | ShipModel
):
    """
    Checks if given ships positions collides with each other. If they do,
    returns True, otherwise False.

    Params:
        - first: First ship
        - second: Second ship

    Returns:
        True if ships collides with each other, otherwise False.
    """
    first_loc = get_ship_cords(first)
    second_loc = get_ship_cords(second)

    start_columns = (first_loc[0].x, second_loc[0].x)
    end_columns = (first_loc[1].x, second_loc[1].x)
    start_rows = (first_loc[0].y, second_loc[0].y)
    end_rows = (first_loc[1].y, second_loc[1].y)

    return (
        max(start_columns) <= min(end_columns)
        and
        max(start_rows) <= min(end_rows))


def ships_conflicts(
    first: schemas.ShipCreate | ShipModel,
    second: schemas.ShipCreate | ShipModel
):
    """
    Checks if given ship has same length as second one or their positions
    collides with each other. Returns True if any of that conditions is met,
    otherwise False.

    Params:
        - first: First ship
        - second: Second ship

    Returns:
        Returns True if ships have the same length or their positions collides
        with each other. Otherwise False.
    """
    return first.length == second.length or ships_collides(first, second)
