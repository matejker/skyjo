import random

from skyjo.policies.policy import Policy


class RandomPolicy(Policy):
    def __init__(self, board, deck, discard_pile):
        self.board = board
        self.deck = deck
        self.discard_pile = discard_pile

    def __repr__(self):
        return "Random Policy"

    def turn(self, *argv) -> tuple[int, int]:
        """Return a tuple of (card, position)."""
        discard = False

        # Choosing deck or discard pile
        if random.random() < 0.5:
            card = self.deck.draw()

            # Are we discarding?
            if random.random() < 0.5:
                discard = True
                self.discard_pile.discard(card)
        else:
            card = self.discard_pile.draw()

        # Choosing position
        if discard:
            position = random.choice(self.board.unknown_cards())
            card = self.board.turn_uncover_card(position)
        else:
            position = random.choice(range(12))
            self.discard_pile.discard(self.board.board[position])
            self.board.turn_replace_card(card, position)

        return card, position
