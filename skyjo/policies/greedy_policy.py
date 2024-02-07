import random

from skyjo.policies.policy import Policy
from skyjo.environment import EXPECTED_VALUE


class GreedyPolicy(Policy):
    def __init__(self, board, deck, discard_pile, acceptance_value=EXPECTED_VALUE) -> None:
        self.board = board
        self.deck = deck
        self.discard_pile = discard_pile
        self.acceptance_value = acceptance_value

    def __repr__(self) -> str:
        return "Greedy Policy"

    def turn(self, *argv) -> tuple[int, int]:
        """Return a tuple of (card, position)."""
        discard = False

        def _v(v):
            return EXPECTED_VALUE if v is None else v

        # Choosing deck or discard pile
        if self.discard_pile.top_card() < self.acceptance_value:
            card = self.discard_pile.draw()
        else:
            card = self.deck.draw()
            if self.acceptance_value < card:
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
