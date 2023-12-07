from skyjo.environment import PlayersBoard, Deck, DiscardPile


class Policy:
    def __int__(self, board: PlayersBoard, deck: Deck, discard_pile: DiscardPile) -> None:
        self.board = board
        self.deck = deck
        self.discard_pile = discard_pile

    def turn(self, *argv) -> tuple[int, int]:
        """Return a tuple of (card, position)."""
        raise NotImplementedError()
