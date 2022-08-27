""" test_datastructures.py

Test compound data structures.
Reference: https://docs.python.org/3/library/dataclasses.html

Created by Chaitanya Rajguru 24-Aug-2022
"""

import sys
import os
from dataclasses import asdict, dataclass

@dataclass
class InventoryItem:
    """Class for keeping track of an item in inventory."""
    name: str
    unit_price: float
    quantity_on_hand: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand

@dataclass
class InventoryList:
    item_list: list[InventoryItem]

    def full_cost(self) -> float:
        return sum(x.total_cost() for x in self.item_list)


@dataclass
class TubeState:
    """Class for recording a state of the tube."""
    contents: str

@dataclass
class PuzzleState:
    """Class for recording a state of the puzzle."""
    game_state: list[TubeState]

@dataclass
class PuzzleSequence:
    """Class for recording the puzzle solution sequence."""
    puzzle_seq: list[PuzzleState]

@dataclass
class StatesVisited:
    """Class for recording every state reached."""
    states_visited: list[PuzzleState]


def main():
    """Create an inventory structure."""
    my_item = InventoryItem('Pen', 2.5)
    my_item2 = InventoryItem('Pad', 4, 6)

    print(my_item, my_item.total_cost())
    print(my_item2, my_item2.total_cost())

    my_list = InventoryList([])
    my_item.quantity_on_hand = 3
    my_list.item_list += [my_item, my_item2]
    print(my_list, my_list.full_cost())

    my_list_dict = asdict(my_list)
    print(my_list_dict['item_list'])
    for item in my_list_dict['item_list']:
        print(item['unit_price'] if item['name'] == 'Pen' else '')

    """Create a game data structure."""
    no_t = 3
    t_cap = 3
    no_c = 2
    no_b = 2

    t_empty = t_cap * "x"
    p_state = PuzzleState([t_empty for _ in range(no_t)])

    p_seq = PuzzleSequence([p_state])
    s_visited = StatesVisited([p_state])
    pass

if __name__ == '__main__':
    main()