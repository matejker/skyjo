import random

from skyjo.policies.policy import Policy
from skyjo.environment import EXPECTED_VALUE


class GreedyPolicy(Policy):
    def __init__(self, board, deck, discard_pile, expected_value=EXPECTED_VALUE) -> None:
        self.board = board
        self.deck = deck
        self.discard_pile = discard_pile
        self.expected_value = expected_value

    def __repr__(self) -> str:
        return "Greedy Policy"

    def turn(self) -> tuple[int, int]:
        """Return a tuple of (card, position)."""
        discard = False

        def _v(v):
            return EXPECTED_VALUE if v is None else v

        # Choosing deck or discard pile
        if self.discard_pile.top_card() < self.expected_value:
            card = self.discard_pile.draw()
            # print(f"Taking card {card} from discard pile")
        else:
            card = self.deck.draw()
            # print(f"Taking card {card} from drawn pile")
            if self.expected_value < card:
                discard = True
                self.discard_pile.discard(card)
                # print(f"Card is more than expected value, discarding")

        # Choosing position
        if discard:
            position = random.choice(self.board.unknown_cards())
            # print(f"Turning {self.board.board[position]} at position {position}")
            card = self.board.turn_uncover_card(position)
        else:
            difference = [round(_v(c) - card, 3) for c in self.board.visible_board]

            max_difference = max(difference)

            max_difference_positions = [i for i, d in enumerate(difference) if d == max_difference]

            position = random.choice(max_difference_positions)
            # print(f"Replacing card {self.board.board[position]} at position {position} with card {card}")
            self.discard_pile.discard(self.board.board[position])
            self.board.turn_replace_card(card, position)

        return card, position
