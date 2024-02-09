from typing import List
import random

RUN = 0
JUMP = 1

class Geo:
    def __init__(self, moves):
        self.moves = moves
        self.score = 0
        self.x = 0
        self.y = 0


def get_noise_list(my_moves: List[int], noise: float) -> List[int]:
    """
    Generate a list of noisy moves based on the input list of moves and a noise threshold.

    Parameters:
    - my_moves: a list of integers representing the moves
    - noise: a float representing the noise threshold

    Returns:
    - A list of integers representing the noisy moves
    """
    return [
        move if (noise < random.random()) else random.randint(0, 1) for move in my_moves
    ]


def create_offspring(
    geo: Geo, offspring_count: int, pre_epoch_noise: float, post_epoch_noise: float
) -> List[Geo]:
    """
    Creates a specified number of offspring Geo objects based on the given Geo object.
    
    Args:
        geo (Geo): The Geo object to base the offspring on.
        offspring_count (int): The number of offspring to create.
        pre_epoch_noise (float): The amount of noise to apply before the epoch distance.
        post_epoch_noise (float): The amount of noise to apply after the epoch distance.
    
    Returns:
        list: A list of Geo objects representing the offspring.
    """
    max_distance = geo.score

    offsprings = [
        Geo(
            moves=get_noise_list(geo.moves[0:max_distance], pre_epoch_noise)
            + get_noise_list(geo.moves[max_distance::], post_epoch_noise)
        )
        for _ in range(offspring_count)
    ]

    return offsprings
