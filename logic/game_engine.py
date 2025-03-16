import random
from data.celebrities import (
    get_all_bollywood_celebrities, 
    get_all_hollywood_celebrities,
    get_all_scientists, 
    get_all_celebrities
)

class GameEngine:
    """
    Core game logic for the celebrity guessing game.
    Handles selection of mystery celebrity, descriptions, and checking guesses.
    """
    
    def __init__(self, mode="all"):
        """
        Initialize the game engine.
        
        Args:
            mode (str): Game mode - "bollywood", "hollywood", "scientists", or "all"
        """
        self.mode = mode
        self.username = None
        self.score = 0
        self.guessed_celebrities = []
        
        if mode == "bollywood":
            self.celebrities = get_all_bollywood_celebrities()
        elif mode == "hollywood":
            self.celebrities = get_all_hollywood_celebrities()
        elif mode == "scientists":
            self.celebrities = get_all_scientists()
        else:
            self.celebrities = get_all_celebrities()
            
        self.mystery_celebrity = None
        self.guesses_remaining = 2
        self.game_result = None
        
    def set_username(self, username):
        """Set the player's username."""
        self.username = username
        
    def set_mode(self, mode):
        """
        Change the game mode.
        
        Args:
            mode (str): Game mode - "bollywood", "hollywood", "scientists", or "all"
        """
        self.mode = mode

        if mode == "bollywood":
            self.celebrities = get_all_bollywood_celebrities()
        elif mode == "hollywood":
            self.celebrities = get_all_hollywood_celebrities()
        elif mode == "scientists":
            self.celebrities = get_all_scientists()
        else:  # "all" mode
            self.celebrities = get_all_celebrities()
        
        self.guessed_celebrities = []
            
    def start_new_game(self):
        """Start a new game by selecting a random celebrity."""
        available_celebrities = [celeb for celeb in self.celebrities 
                               if celeb not in self.guessed_celebrities]
        
        if not available_celebrities:
            self.guessed_celebrities = []
            available_celebrities = self.celebrities
        
        self.mystery_celebrity = random.choice(available_celebrities)
        self.guesses_remaining = 2
        self.game_result = None
        return True
    
    def is_category_completed(self):
        """
        Check if all celebrities in the current category have been guessed.
        
        Returns:
            bool: True if all celebrities in the category have been guessed
        """
        total_celebrities = len(self.celebrities)
        
        guessed_count = len([celeb for celeb in self.guessed_celebrities 
                           if celeb in self.celebrities])
        
        return guessed_count >= total_celebrities
        
    def process_guess(self, guess):
        """
        Process a player's guess.
        
        Args:
            guess (str): The player's guess
            
        Returns:
            bool: Whether the guess is correct
            bool: Whether the game should continue
            int: Current score
            bool: Whether to start a new round
        """
        if not guess:
            return False, True, self.score, False
            
        is_correct = guess.lower() == self.mystery_celebrity['answer'].lower()
        
        if is_correct:
            self.score += self.guesses_remaining
            self.guessed_celebrities.append(self.mystery_celebrity)
            self.game_result = "win"
            
            return True, True, self.score, True
        else:
            self.guesses_remaining -= 1
            
            if self.guesses_remaining == 0:
                self.game_result = "out_of_guesses"
                return False, False, self.score, False
                
            return False, True, self.score, False
    
    def get_game_state(self):
        """
        Get the current state of the game.
        
        Returns:
            dict: The current game state
        """
        return {
            "mode": self.mode,
            "username": self.username,
            "score": self.score,
            "mystery_celebrity": self.mystery_celebrity,
            "guesses_remaining": self.guesses_remaining,
            "game_result": self.game_result,
            "category_completed": self.is_category_completed(),
            "guessed_count": len(self.guessed_celebrities),
            "total_count": len(self.celebrities)
        }