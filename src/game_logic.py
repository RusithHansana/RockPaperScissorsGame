import random
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class GameLogic:
    # Game state constants
    GAME_STATES = {
        "STOPPED": "stopped",
        "RUNNING": "running",
        "PAUSED": "paused",
        "ROUND_ENDED": "round_ended",
        "MATCH_ENDED": "match_ended"
    }

    def __init__(self):
        self.game_state = self.GAME_STATES["STOPPED"]
        self.clock = 0
        self.player_move = None
        self.computer_move = None
        self.round_number = 1
        self.player_score = 0
        self.computer_score = 0
        self.match_ended = False
        self.round_result_shown = False
        self.game_text = "Press Start to begin"  # Default status text

    def start_game(self):
        """Start the game."""
        self.game_state = self.GAME_STATES["RUNNING"]
        self.game_text = "Game started!"
        logging.debug(f"Game started, game_text: {self.game_text}")

    def stop_game(self):
        """Pause the game."""
        self.game_state = self.GAME_STATES["PAUSED"]
        self.game_text = "Game paused"
        logging.debug(f"Game paused, game_text: {self.game_text}")

    def restart_game(self):
        """Reset the game to initial state."""
        self.clock = 0
        self.round_number = 1
        self.player_score = 0
        self.computer_score = 0
        self.match_ended = False
        self.round_result_shown = False
        self.game_text = "Press Start to begin"
        self.game_state = self.GAME_STATES["STOPPED"]
        logging.debug(f"Game reset, game_text: {self.game_text}")

    def get_computer_move(self):
        """Generate a random computer move."""
        return random.choice(["rock", "paper", "scissors"])

    def update_game_state(self, clock, player_move, success):
        """Update the game state based on the current clock and player move."""
        self.clock = clock
        if self.game_state == self.GAME_STATES["RUNNING"] and not self.match_ended:
            if 0 <= self.clock < 20:
                self.game_text = f"Round {self.round_number} - Get Ready!"
                self.round_result_shown = False
            elif self.clock < 30:
                self.game_text = "Rock"
            elif self.clock < 40:
                self.game_text = "Paper"
            elif self.clock < 50:
                self.game_text = "Scissors"
            elif self.clock < 60:
                self.game_text = "Shoot!"
            elif self.clock == 60:
                if success:
                    self.player_move = player_move
                    self.computer_move = self.get_computer_move()
                else:
                    self.game_text = "Show exactly one hand!"
            elif self.clock < 100 and not self.round_result_shown:
                if success and self.player_move and self.computer_move:
                    self.game_text = f"You: {self.player_move} | Computer: {self.computer_move}"
                    if self.player_move == self.computer_move:
                        self.game_text += " | Draw!"
                    elif (self.player_move == "rock" and self.computer_move == "scissors") or \
                         (self.player_move == "scissors" and self.computer_move == "paper") or \
                         (self.player_move == "paper" and self.computer_move == "rock"):
                        self.game_text += " | You win this round!"
                        self.player_score += 1
                    else:
                        self.game_text += " | Computer wins this round!"
                        self.computer_score += 1

                    if self.player_score >= 2 or self.computer_score >= 2:
                        self.match_ended = True
                        self.game_state = self.GAME_STATES["PAUSED"]
                        self.game_text = "You Win the Match!" if self.player_score > self.computer_score else "Computer Wins the Match!"

                    self.round_result_shown = True

                    if self.clock >= 90:
                        self.clock = 0
                        if not self.match_ended:
                            self.round_number += 1
                else:
                    self.game_text = "Show exactly one hand!"
            logging.debug(f"Updated game_text: {self.game_text}")
        else:
            if not self.game_text:
                self.game_text = "Game paused or stopped"
            logging.debug(f"Game not running, game_text: {self.game_text}")

    def get_state(self):
        """Return the current game state."""
        return {
            "game_state": self.game_state,
            "clock": self.clock,
            "player_move": self.player_move,
            "computer_move": self.computer_move,
            "round_number": self.round_number,
            "player_score": self.player_score,
            "computer_score": self.computer_score,
            "match_ended": self.match_ended,
            "game_text": self.game_text
        }