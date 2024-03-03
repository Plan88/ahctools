from enum import Enum, auto

from pydantic import BaseModel


class TileType(Enum):
    one = auto()
    tate = auto()
    yoko = auto()


class Tile(BaseModel):
    tile_type: TileType
    score: int | tuple[int, int]
    pos: tuple[int, int]

    def get_white_line(self) -> dict | None:
        if self.tile_type == TileType.one:
            return None

        if self.tile_type == TileType.yoko:
            x0 = self.pos[1] + 1
            x1 = self.pos[1] + 1
            y0 = self.pos[0]
            y1 = self.pos[0] + 1
        else:
            x0 = self.pos[1]
            x1 = self.pos[1] + 1
            y0 = self.pos[0] + 1
            y1 = self.pos[0] + 1

        return {
            "x": [x0, x1],
            "y": [y0, y1],
        }

    def get_full_pos(self) -> tuple[int, int] | tuple[tuple[int, int], tuple[int, int]]:
        if self.tile_type == TileType.one:
            return self.pos
        elif self.tile_type == TileType.tate:
            return (self.pos, (self.pos[0] + 1, self.pos[1]))
        else:
            return (self.pos, (self.pos[0], self.pos[1] + 1))
