import random
from typing import Optional

CARDS_QUANTITY = {
    -2: 5,
    -1: 10,
    0: 15,
    1: 10,
    2: 10,
    3: 10,
    4: 10,
    5: 10,
    6: 10,
    7: 10,
    8: 10,
    9: 10,
    10: 10,
    11: 10,
    12: 10,
}

EXPECTED_VALUE = sum(v * q for v, q in CARDS_QUANTITY.items()) / 150  # 76 / 15 = 5.0666


class PlayersBoard:
    def __init__(self, unknown_cards: list) -> None:
        self.board: list[int] = unknown_cards
        self.visible_board: list[Optional[int]] = [None] * 12

    def turn_replace_card(self, card: int, position: int) -> None:
        self.visible_board[position] = card
        self.board[position] = card

    def turn_uncover_card(self, position: int) -> int:
        self.visible_board[position] = self.board[position]
        return self.visible_board[position]

    def value(self) -> int:
        return round(sum(v for v in self.board), 3)

    def unknown_cards(self) -> list[int]:
        return [i for i, v in enumerate(self.visible_board) if v is None]

    def is_finished(self) -> bool:
        return len(self.unknown_cards()) == 0

    def __str__(self):
        def _r(j: Optional[int], v: int) -> str:
            def _rr(i):
                if 0 <= i <= 9:
                    return f" {i}"
                return str(i)

            if j is None:
                return f"[{_rr(v)}]"
            return f" {_rr(v)} "

        return "\n".join(
            " ".join(_r(i, self.board[4 * r + j]) for j, i in enumerate(self.visible_board[4 * r : 4 * r + 4]))
            for r in range(3)
        )


class Deck:
    """Heap of cards to draw from."""

    def __init__(self) -> None:
        self.cards: list[int] = random.sample([v for v, q in CARDS_QUANTITY.items() for _ in range(q)], 150)

    def draw(self) -> int:
        return self.cards.pop()

    def __len__(self) -> int:
        return len(self.cards)

    def __repr__(self) -> str:
        return f"Deck({len(self)})"

    def expected_value(self) -> float:
        return round(sum(self.cards) / (len(self.cards) or 1), 3)


class DiscardPile:
    """Heap of discarded cards."""

    def __init__(self) -> None:
        self.cards = []

    def discard(self, card) -> None:
        self.cards.append(card)

    def top_card(self) -> int:
        return self.cards[-1]

    def draw(self) -> int:
        return self.cards.pop()

    def __len__(self) -> int:
        return len(self.cards)

    def __repr__(self) -> str:
        return f"DiscardPile({len(self)})"
