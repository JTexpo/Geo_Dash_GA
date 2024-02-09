from typing import List
from copy import deepcopy

from geodashga.geo import Geo, JUMP

SPIKES_ID = 3
BOUND_BOX_ID = 2
FLOOR_ID = 1
AIR_ID = 0


def create_blank_board(width: int, height: int) -> List[List[int]]:
    return [[0 for _ in range(width)] for _ in range(height)]


# NOTE - falls are +y , jumps are -y
# this is because that the top left of the map is 0,0
def jump_geo(geo: Geo, board: List[List[int]]):
    if (geo.moves[geo.x] == JUMP) and (board[geo.y + 1][geo.x] == FLOOR_ID):
        for index in range(3):
            if board[geo.y - index][geo.x] != AIR_ID:
                geo.y -= index
                break
        else:
            geo.y -= 3


def scroll_geo(geo: Geo):
    geo.x += 1


def fall_geo(geo: Geo, board: List[List[int]]):
    if board[geo.y + 1][geo.x] != FLOOR_ID:
        geo.y += 1

    if geo.y < 0:
        geo.y = 0


def death_geo(geo: Geo, board: List[List[int]]):
    return board[geo.y][geo.x] != AIR_ID


def populate_bound_box(board: List[List[int]]) -> List[List[int]]:
    board_copy = deepcopy(board)

    # Adding the bounds to the bottom
    for index in range(len(board_copy[0])):
        if board_copy[-1][index] == AIR_ID:
            board_copy[-1][index] = BOUND_BOX_ID

    # Adding the bounds to the far right side
    for index in range(len(board_copy)):
        if board_copy[index][-1] == AIR_ID:
            board_copy[index][-1] = BOUND_BOX_ID

    return board_copy


def move_geo(geo: Geo, board: List[List[int]]):
    jump_geo(geo=geo, board=board)
    scroll_geo(geo=geo)
    fall_geo(geo=geo, board=board)
    if death_geo(geo=geo, board=board):
        geo.score = geo.x


def play_game(geos: List[Geo], board: List[List[int]]):
    geo_played = False
    for i in range(len(board[0])):
        geo_played = False
        for geo in geos:
            if geo.score:
                continue
            move_geo(geo=geo, board=board)
            geo_played = True
        if not geo_played:
            break

    geos = sorted(geos, key=lambda geo: -geo.score)  # sorting best to worst
    return geos
