#!/usr/bin/env python3
from logic.game_engine import GameEngine
from ui.terminal_ui import TerminalUI

def main():
    """Main function to run the game."""
    game_engine = GameEngine()
    
    ui = TerminalUI(game_engine)
    
    play_again = True
    while play_again:
        play_again = ui.run_game_loop()
        
    print("\nThank you for playing! Goodbye!")

if __name__ == "__main__":
    main()