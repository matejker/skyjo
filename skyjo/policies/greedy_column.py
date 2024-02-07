import random

from skyjo.policies.policy import Policy
from skyjo.environment import EXPECTED_VALUE


class GreedyColumnPolicy(Policy):
    def __init__(self, board, deck, discard_pile, acceptance_value=EXPECTED_VALUE) -> None:
        self.board = board
        self.deck = deck
        self.discard_pile = discard_pile
        self.acceptance_value = acceptance_value

    def __repr__(self) -> str:
        return "Greedy Column Policy"

    def check_column_match(self, position: int) -> bool:
        """Return True if the card in the position matches the column."""
        if self.board.visible_board[position] is None:
            return False

        mod = position % 4
        return all(self.board.visible_board[i] == self.board.visible_board[position] for i in range(mod, 12, 4))

    def check_column_available(self, position: int) -> int:
        """Return -1 if no position in a column is available. Otherwise, return the available position."""
        mod = position % 4
        positions = [i for i in range(mod, 12, 4) if i != position]
        v = self.board.board[position]

        are_available = all(self.board.visible_board[i] in (v, None) for i in positions)

        return next((i for i in positions if self.board.visible_board[i] is None), -1) if are_available else -1

    def get_all_positions(self, card: int) -> list[int]:
        return [i for i in range(12) if self.board.visible_board[i] == card]

    def turn(self, *argv) -> tuple[int, int]:
        """Return a tuple of (card, position)."""
        discard = False
        column_match = False
        position = -1

        def _v(v):
            # TODO: if there are two values in the same column, keep them
            return EXPECTED_VALUE if v is None else v

        # Choosing deck or discard pile
        if position := self.check_column_available(self.discard_pile.top_card()) != -1:
            card = self.discard_pile.draw()
            column_match = True
        elif self.discard_pile.top_card() < self.acceptance_value:
            card = self.discard_pile.draw()
        else:
            card = self.deck.draw()
            if position := self.check_column_available(card) != -1:
                column_match = True
            elif self.acceptance_value < card:
                discard = True
                self.discard_pile.discard(card)

        # Choosing position
        if discard:
            position = random.choice(self.board.unknown_cards())
            card = self.board.turn_uncover_card(position)
        elif column_match:
            self.discard_pile.discard(self.board.board[position])
            self.board.turn_replace_card(card, position)
        else:
            difference = [
                round(_v(c) - card, 3)
                for i, c in enumerate(self.board.visible_board)
                if check_column_available(i) != -1
            ]

            max_difference = max(difference)

            max_difference_positions = [i for i, d in enumerate(difference) if d == max_difference]

            position = random.choice(max_difference_positions)

            self.discard_pile.discard(self.board.board[position])
            self.board.turn_replace_card(card, position)

        return card, position
