from typing import List
import random
import asyncio
from copy import deepcopy

from js import document
from pyodide.ffi import create_proxy
import pyscript
from pyscript import Element

from geodashga.board import (
    Geo,
    AIR_ID,
    BOUND_BOX_ID,
    SPIKES_ID,
    FLOOR_ID,
    create_blank_board,
    play_game,
    populate_bound_box,
    move_geo,
)
from geodashga.geo import create_offspring


LINE_WIDTH = 2
SPACING = 12
GEO_PERSON_ID = -1

DRAW_MODE_KEY = 1
ERASE_MODE_KEY = 2
SPIKES_MODE_KEY = 3

MODE = DRAW_MODE_KEY

COLOUR_MAPPING = {
    AIR_ID: "white",
    BOUND_BOX_ID: "white",
    FLOOR_ID: "black",
    SPIKES_ID: "red",
    GEO_PERSON_ID: "blue",
}

BOARD_WIDTH = 12 * 3
BOARD_HEIGHT = 6
GEO_COUNT = 10

start_game = False
start_index = 0
geos = [
    Geo(moves=[random.randint(0, 1) for _ in range(BOARD_WIDTH)])
    for _ in range(GEO_COUNT)
]
# board = create_blank_board(width=BOARD_WIDTH, height=BOARD_HEIGHT)
board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 3, 3, 0, 0, 0, 0, 3, 3], 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 3, 3, 1, 1, 3, 3, 3, 3]
]


def clear_board(reset_board: bool = True):
    """
    Clear the game board by filling it with black, then drawing a white rectangle
    inside filled with black lines to represent the game board grid. If reset_board
    is True, create a new blank board with the specified width and height.

    Args:
        reset_board (bool, optional): If True, reset the game board to a new blank
            board. Default is True.
    """
    global LINE_WIDTH, SPACING, BOARD_WIDTH, BOARD_HEIGHT, board
    canvas = document.getElementById("geo-game")
    ctx = canvas.getContext("2d")

    # Black background
    ctx.fillStyle = "black"
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    # White mini-background
    ctx.fillStyle = "white"
    ctx.fillRect(
        LINE_WIDTH,
        LINE_WIDTH,
        canvas.width - LINE_WIDTH * 2,
        canvas.height - LINE_WIDTH * 2,
    )

    # Black lines vertical
    ctx.fillStyle = "black"
    for index in range(1, SPACING):
        ctx.fillRect(
            index * (canvas.width / SPACING) - LINE_WIDTH,
            0,
            LINE_WIDTH * 2,
            canvas.height,
        )

    # Black lines horizontal
    for index in range(1, SPACING * 2):
        ctx.fillRect(
            0,
            index * ((canvas.height * 2) / SPACING) - LINE_WIDTH,
            canvas.width,
            LINE_WIDTH * 2,
        )

    # Clears the board
    if reset_board:
        board = create_blank_board(width=BOARD_WIDTH, height=BOARD_HEIGHT)


def draw_board(board: List[List[int]], start_index: int):
    """
    Draw the given board on the canvas starting from the specified index.

    Args:
        board (List[List[int]]): The board to be drawn.
        start_index (int): The index from which to start drawing.
    """
    global LINE_WIDTH, SPACING, COLOUR_MAPPING

    canvas = document.getElementById("geo-game")
    ctx = canvas.getContext("2d")

    for y, row in enumerate(board):
        for x, value in enumerate(row[start_index : start_index + 12]):
            ctx.fillStyle = COLOUR_MAPPING[value]

            ctx.fillRect(
                x * (canvas.width / SPACING) + LINE_WIDTH,
                2 * y * (canvas.height / SPACING) + LINE_WIDTH,
                canvas.width / SPACING - LINE_WIDTH * 2,
                2 * canvas.height / SPACING - LINE_WIDTH * 2,
            )


def update_start_index(amount: int):
    """
    Updates the start index by the given amount and ensures it stays within
    the valid range. Then clears the board without resetting it and draws the
    updated board with the new start index. Updates the page element to
    display the current page index.
    
    Args:
        amount (int): The amount to update the start index by.
    """
    global start_index, board

    # Increasing the start index
    start_index += amount

    # Correcting any over or under-shooting
    if start_index < 0:
        start_index = 0
    if start_index > len(board[0]):
        start_index = len(board[0]) - (SPACING + 1)

    # Cleaning up the boards
    clear_board(reset_board=False)
    draw_board(board=board, start_index=start_index)

    # Cleaning up the page index
    page_element = Element("page-index")
    page_element.element.innerHTML = f"Page : {start_index // SPACING + 1}/3"


def toggle_mode(mode: int):
    global MODE
    MODE = mode


def start():
    global start_game
    start_game = True


async def main():
    """
    Asynchronous main function that runs indefinitely. It checks if the game has started,
    and if so, iterates through the game for 5 iterations. It updates the board and
    scrolls through the moves while displaying the game updates. It also creates and
    updates offspring geos. It sleeps for 0.5 seconds between iterations.
    """
    global board, geos, start_game, COLOUR_MAPPING, GEO_PERSON_ID
    while True:
        if start_game:
            for itteration in range(5):
                gen_element = Element("gen-index")
                gen_element.element.innerHTML = f"Gen : {itteration}"

                board_scroll = 0
                my_board = populate_bound_box(board=board)
                ranked_geos = play_game(geos=geos, board=my_board)
                model_geo = deepcopy(ranked_geos[0])

                model_geo.x = 0
                model_geo.y = 0

                for index, move in enumerate(model_geo.moves):
                    previous_board_id = board[model_geo.y][model_geo.x]

                    board[model_geo.y][model_geo.x] = GEO_PERSON_ID
                    draw_board(board=board, start_index=board_scroll)

                    board[model_geo.y][model_geo.x] = previous_board_id

                    board_scroll += 1
                    if board_scroll + SPACING > len(board[0]):
                        board_scroll = len(board[0]) - (SPACING)

                    if index >= model_geo.score:
                        break

                    move_geo(geo=model_geo, board=my_board)
                    await asyncio.sleep(0.2)

                geos = create_offspring(
                    geo=model_geo,
                    offspring_count=GEO_COUNT - 1,
                    pre_epoch_noise=0.5,
                    post_epoch_noise=1,
                )
                geos.append(model_geo)

            start_game = False

        await asyncio.sleep(0.5)


def _on_click(element):
    global board, SPACING, MODE, DRAW_MODE_KEY, ERASE_MODE_KEY, FLOOR_ID, AIR_ID, start_index

    canvas = document.getElementById("geo-game")

    # DRAW
    # ----
    if MODE == DRAW_MODE_KEY:
        board[int(element.offsetY // (canvas.width / SPACING))][
            int(element.offsetX // (canvas.width / SPACING)) + start_index
        ] = FLOOR_ID

    # DRAW
    # ----
    if MODE == SPIKES_MODE_KEY:
        board[int(element.offsetY // (canvas.width / SPACING))][
            int(element.offsetX // (canvas.width / SPACING)) + start_index
        ] = SPIKES_ID

    # ERASE
    # -----
    elif MODE == ERASE_MODE_KEY:
        board[int(element.offsetY // (canvas.width / SPACING))][
            int(element.offsetX // (canvas.width / SPACING)) + start_index
        ] = AIR_ID

    draw_board(board, start_index=start_index)


clear_board(reset_board=False)
draw_board(board=board, start_index=start_index)

on_click = create_proxy(_on_click)
document.getElementById("geo-game").addEventListener("mousedown", on_click)
pyscript.run_until_complete(main())
