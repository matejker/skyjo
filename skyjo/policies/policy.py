from skyjo.environment import PlayersBoard, Deck, DiscardPile


class Policy:
    def __int__(self, board: PlayersBoard, deck: Deck, discard_pile: DiscardPile, expected_value: int = 0) -> None:
        self.board = board
        self.deck = deck
        self.discard_pile = discard_pile
        self.expected_value = expected_value

    def turn(self) -> tuple[int, int]:
        """Return a tuple of (card, position)."""
        raise NotImplementedError()
