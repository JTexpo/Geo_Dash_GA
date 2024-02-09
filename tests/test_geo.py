import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from geodashga.geo import get_noise_list, create_offspring, Geo
import random


class GeoTestCases(unittest.TestCase):
    def test_get_noise_list(self):
        # INITALIZATION
        # -------------
        random_seed = 1
        blank_list = [0, 0, 0, 0, 0, 0]

        # ACTION
        # ------
        random.seed(random_seed)
        my_list = get_noise_list(blank_list, 1)

        # ASSERT
        # ------
        expected = [0, 1, 1, 0, 0, 1]
        self.assertTrue(my_list == expected)

    def test_create_offspring(self):
        # INITALIZATION
        # -------------
        random_seed = 1
        base_geo = Geo(moves=[0, 0, 0, 0, 0, 0])
        base_geo.score = 3

        # ACTION
        # ------
        random.seed(random_seed)
        my_geos = create_offspring(
            geo=base_geo, offspring_count=2, pre_epoch_noise=0, post_epoch_noise=1
        )

        # ASSERT
        # ------
        self.assertTrue(len(my_geos) == 2)
        self.assertTrue(my_geos[0].moves == [0, 0, 0, 1, 1, 0])


if __name__ == "__main__":
    unittest.main()
