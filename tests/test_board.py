import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from geodashga.board import (
    Geo,
    fall_geo,
    jump_geo,
    death_geo,
    scroll_geo,
    create_blank_board,
    populate_bound_box,
    play_game,
    FLOOR,
    JUMP,
)


class BoardTestCases(unittest.TestCase):
    def test_create_blank_board(self):
        # ACTION
        # ------
        my_board = create_blank_board(width=2, height=3)

        # ASSERT
        # ------
        expected = [[0, 0], [0, 0], [0, 0]]
        self.assertTrue(my_board == expected)

    def test_fall_geo(self):
        # INITALIZATION
        # -------------
        geo = Geo(moves=[0, 0, 0, 0, 0])
        my_baord = create_blank_board(width=5, height=3)

        # ACTION
        # ------
        fall_geo(geo=geo, board=my_baord)

        # ASSERT
        # ------
        self.assertTrue(geo.y == 1)

    def test_jump_geo_top(self):
        # INITALIZATION
        # -------------
        geo = Geo(moves=[JUMP, JUMP, JUMP, JUMP, JUMP])
        geo.y = 1
        my_baord = create_blank_board(width=5, height=3)
        my_baord[geo.y + 1][geo.x] = FLOOR

        # ACTION
        # ------
        jump_geo(geo=geo, board=my_baord)
        fall_geo(geo=geo, board=my_baord)

        # ASSERT
        # ------
        self.assertTrue(geo.y == 0)

    def test_jump_geo(self):
        # INITALIZATION
        # -------------
        geo = Geo(moves=[JUMP, JUMP, JUMP, JUMP, JUMP])
        geo.y = 3
        my_baord = create_blank_board(width=5, height=5)
        my_baord[geo.y + 1][geo.x] = FLOOR

        # ACTION
        # ------
        jump_geo(geo=geo, board=my_baord)

        # ASSERT
        # ------
        self.assertTrue(geo.y == 0)

    def test_jump_geo(self):
        # INITALIZATION
        # -------------
        geo = Geo(moves=[0, 0, 0, 0, 0])

        # ACTION
        # ------
        scroll_geo(geo=geo)

        # ASSERT
        # ------
        self.assertTrue(geo.x == 1)

    def test_death_go(self):
        # INITALIZATION
        # -------------
        geo = Geo(moves=[0, 0, 0, 0, 0])
        board = [[1]]

        # ACTION
        # ------
        is_dead = death_geo(geo=geo, board=board)

        # ASSERT
        # ------
        self.assertTrue(is_dead)
    
    def test_populate_bound_box(self):
        # INITALIZATION
        # -------------
        my_baord = create_blank_board(width=5, height=5)

        # ACTION
        # ------
        populated_board = populate_bound_box(board=my_baord)

        # ASSERT
        # ------
        expected = [
            [0, 0, 0, 0, 2], 
            [0, 0, 0, 0, 2], 
            [0, 0, 0, 0, 2], 
            [0, 0, 0, 0, 2], 
            [2, 2, 2, 2, 2]
        ]
        self.assertTrue(populated_board == expected)
    
    def test_play_game_1(self):
        # INITALIZATION
        # -------------
        my_baord = create_blank_board(width=10, height=5)
        my_baord = populate_bound_box(board=my_baord)
        geos = [Geo([0,0,0,0,0,0,0,0,0,0])]

        # ACTION
        # ------
        updated_geos = play_game(geos=geos, board=my_baord)

        # ASSERT
        # ------
        self.assertTrue(updated_geos[0].score == 4)
    
    def test_play_game_2(self):
        # INITALIZATION
        # -------------
        my_baord = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 2], 
            [1, 1, 1, 1, 1, 1, 1, 2, 2, 2]
        ]

        geos = [Geo([0,0,0,0,0,0,0,0,0,0])]

        # ACTION
        # ------
        updated_geos = play_game(geos=geos, board=my_baord)

        # ASSERT
        # ------
        self.assertTrue(updated_geos[0].score == 6)
    
    def test_play_game_3(self):
        # INITALIZATION
        # -------------
        my_baord = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 2], 
            [1, 1, 1, 1, 1, 1, 1, 2, 2, 2]
        ]

        geos = [Geo([0,0,0,0,0,1,0,0,0,0])]

        # ACTION
        # ------
        updated_geos = play_game(geos=geos, board=my_baord)

        # ASSERT
        # ------
        self.assertTrue(updated_geos[0].score == 9)
    
    def test_play_game_sort(self):
        # INITALIZATION
        # -------------
        my_baord = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 2], 
            [1, 1, 1, 1, 1, 1, 1, 2, 2, 2]
        ]

        geos = [Geo([0,0,0,0,0,0,0,0,0,0]), Geo([0,0,0,0,0,1,0,0,0,0])]

        # ACTION
        # ------
        updated_geos = play_game(geos=geos, board=my_baord)

        # ASSERT
        # ------
        self.assertTrue(updated_geos[0].score == 9)


if __name__ == "__main__":
    unittest.main()
