import random
from math import ceil
from enum import Enum

from skyjo.policies.policy import Policy
from skyjo.environment import EXPECTED_VALUE


class GlidingType(Enum):
    LINEAR = "linear"


def linear_gliding_function(t: int, acceptance_value) -> float:
    return round(acceptance_value + (max(EXPECTED_VALUE, acceptance_value) - acceptance_value) * t / 11, 2)


class GlidingGreedyPolicy(Policy):
    def __init__(
        self, board, deck, discard_pile, acceptance_value=EXPECTED_VALUE, gliding: GlidingType = GlidingType.LINEAR
    ) -> None:
        self.board = board
        self.deck = deck
        self.discard_pile = discard_pile
        self.acceptance_value = acceptance_value
        self.gliding = gliding

    def __repr__(self) -> str:
        return f"Gliding Greedy Policy({self.acceptance_value=}, {self.gliding=})".replace("self.", "")

    def turn(self, other_player_board) -> tuple[int, int]:
        """Return a tuple of (card, position)."""
        discard = False

        if self.gliding == GlidingType.LINEAR:
            acceptance_value = linear_gliding_function(len(other_player_board.unknown_cards()), self.acceptance_value)
        else:
            acceptance_value = self.acceptance_value

        def _v(v):
            return EXPECTED_VALUE if v is None else v

        # Choosing deck or discard pile
        if self.discard_pile.top_card() < acceptance_value:
            card = self.discard_pile.draw()
        else:
            card = self.deck.draw()
            if acceptance_value < card:
                discard = True
                self.discard_pile.discard(card)

        # Choosing position
        if discard:
            position = random.choice(self.board.unknown_cards())
            card = self.board.turn_uncover_card(position)
        else:
            difference = [round(_v(c) - card, 3) for c in self.board.visible_board]

            max_difference = max(difference)

            max_difference_positions = [i for i, d in enumerate(difference) if d == max_difference]

            position = random.choice(max_difference_positions)

            self.discard_pile.discard(self.board.board[position])
            self.board.turn_replace_card(card, position)

        return card, position
