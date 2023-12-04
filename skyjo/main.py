from skyjo.environment import PlayersBoard, Deck, DiscardPile, EXPECTED_VALUE
from skyjo.policies.greedy_policy import GreedyPolicy
from skyjo.policies.random_policy import RandomPolicy

if __name__ == "__main__":
    # Create environment
    deck = Deck()
    discard_pile = DiscardPile()

    discard_pile.discard(deck.draw())

    board = PlayersBoard([deck.draw() for _ in range(12)])

    # Create policy
    policy = RandomPolicy(board, deck, discard_pile)
    # policy = GreedyPolicy(board, deck, discard_pile)

    # Play
    round = 0
    while not board.is_finished():
        print("--------------------------------------")
        print()
        print(f"Discard: {discard_pile.top_card()}")
        card, position = policy.turn()
        round += 1

        print(f"Card: {card}, Position: {position}, Round {round}, Value: {board.value()}")
        print(board)
        print()

        discard_pile.discard(deck.draw())

    print(f"Final score: {board.value()}")
