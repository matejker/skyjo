"""From ChatGPT:
Creating a full-fledged AI to play a game like Skyjo would be a significant undertaking and may require machine
learning techniques for optimal decision-making. However, I can provide a simple example of a Python script that
simulates a basic two-player Skyjo game. This script will include the game setup, card drawing, and simple scoring.
"""
import random


class SkyjoGame:
    def __init__(self, players):
        self.players = players
        self.deck = self.generate_deck()
        self.discard_pile = []
        self.hands = {player: [] for player in players}
        self.scores = {player: 0 for player in players}

    def generate_deck(self):
        # Each card appears twice in the deck
        deck = list(range(1, 16)) * 2
        random.shuffle(deck)
        return deck

    def deal_initial_cards(self):
        for _ in range(12):
            for player in self.players:
                card = self.deck.pop()
                self.hands[player].append(card)

    def draw_card(self):
        if not self.deck:
            # Shuffle discard pile into the deck if it's empty
            random.shuffle(self.discard_pile)
            self.deck = self.discard_pile
            self.discard_pile = []

        return self.deck.pop()

    def play_round(self):
        for player in self.players:
            print(f"\nPlayer {player}'s turn:")
            self.display_game_state(player)
            input("Press Enter to draw a card...")
            drawn_card = self.draw_card()
            print(f"Player {player} drew: {drawn_card}")
            self.display_game_state(player)

            replace_index = int(input("Choose a card to replace (0-11): "))
            replaced_card = self.hands[player][replace_index]
            self.discard_pile.append(replaced_card)
            self.hands[player][replace_index] = drawn_card

            self.display_game_state(player)

    def display_game_state(self, current_player):
        print("\nCurrent Game State:")
        for player in self.players:
            print(f"Player {player}: {self.hands[player]} (Score: {self.scores[player]})")
        print(f"Discard Pile: {self.discard_pile}")
        print(f"Deck Size: {len(self.deck)} cards remaining")

    def calculate_scores(self):
        for player in self.players:
            # Calculate the score for each player's hand
            self.scores[player] = sum(self.hands[player])

    def play_game(self):
        self.deal_initial_cards()
        rounds = 1

        while rounds <= 12:  # Assuming 12 rounds in a full game
            print(f"\n------ Round {rounds} ------")
            self.play_round()
            self.calculate_scores()
            rounds += 1

        print("\nGame Over!")
        self.display_game_state(None)
        winner = min(self.scores, key=self.scores.get)
        print(f"Player {winner} wins with a score of {self.scores[winner]}!")


if __name__ == "__main__":
    players = [1, 2]  # You can adjust the number of players as needed
    skyjo_game = SkyjoGame(players)
    skyjo_game.play_game()
