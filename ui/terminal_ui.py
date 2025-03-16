import os
import time
import threading
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.style import Style
from rich.prompt import Prompt
from rich.live import Live
from rich.layout import Layout
from rich import box
import questionary
from questionary import Style as QuestionaryStyle
import pyfiglet

from data.celebrities import (
    get_all_bollywood_celebrities, 
    get_all_hollywood_celebrities,
    get_all_scientists, 
    get_all_celebrities
)
from ui.ascii_animations import AnimationController
from database import ScoreDatabase

class TerminalUI:
    """
    Rich terminal-based user interface for the celebrity guessing game.
    Handles all display and user interaction with colors, styling, and interactive elements.
    """
    
    def __init__(self, game_engine):
        """
        Initialize the terminal UI.
        
        Args:
            game_engine: The game engine instance
        """
        self.game_engine = game_engine
        self.console = Console()
        self.animation = AnimationController(self.console)
        self.db = ScoreDatabase()
        
        self.colors = {
            "title": "bold bright_yellow",
            "subtitle": "bold cyan",
            "highlight": "bright_magenta",
            "success": "bold bright_green",
            "failure": "bold red",
            "info": "bright_blue",
            "question": "bright_cyan",
            "answer": "green",
            "prompt": "yellow",
            "celebrity": "bold bright_magenta", 
            "remaining": "bright_red",
            "divider": "cyan",
            "bollywood": "bold bright_red",
            "hollywood": "bold bright_blue",
            "scientists": "bold bright_green",
            "all": "bold bright_yellow",
            "username": "bold bright_yellow",
            "score": "bold bright_green",
            "commands": "bright_white on dark_blue"
        }
        
        self.question_style = QuestionaryStyle([
            ('qmark', 'fg:yellow bold'),         
            ('question', 'fg:cyan bold'),        
            ('answer', 'fg:green bold'),         
            ('pointer', 'fg:magenta bold'),      
            ('highlighted', 'fg:magenta bold'),  
            ('selected', 'fg:green bold'),        
            ('separator', 'fg:cyan'),            
            ('instruction', 'fg:blue'),           
            ('text', 'fg:white'),                
        ])
        
        self.animation_active = False
        self.game_animation_thread = None 
                
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def create_title(self, text, use_figlet=True):
        """Create a title panel."""
        if use_figlet:
            fig_text = pyfiglet.figlet_format(text, font="small")
            content = Text(fig_text, style=self.colors["title"], justify="center")
        else:
            content = Text(text, style=self.colors["title"], justify="center")
            
        return Panel(
            content,
            box=box.DOUBLE,
            border_style=self.colors["title"],
            width=80 if use_figlet else 70
        )
        
    def create_mode_title(self):
        """Create a title panel based on current game mode."""
        mode = self.game_engine.mode
        mode_name = mode.upper()
        
        if mode == "bollywood":
            title_text = "BOLLYWOOD CELEBRITY EDITION"
            title_color = self.colors["bollywood"]
        elif mode == "hollywood":
            title_text = "HOLLYWOOD CELEBRITY EDITION"
            title_color = self.colors["hollywood"]
        elif mode == "scientists":
            title_text = "FAMOUS SCIENTISTS EDITION"
            title_color = self.colors["scientists"]
        else:
            title_text = "CELEBRITY & SCIENTISTS EDITION"
            title_color = self.colors["all"]
            
        fig_text = pyfiglet.figlet_format(mode_name, font="small")
        content = Text(fig_text, style=title_color, justify="center")
            
        return Panel(
            content,
            box=box.DOUBLE,
            border_style=title_color,
            width=80
        )

    def create_commands_panel(self):
        """Create a panel with keyboard commands."""
        command_text = Text.from_markup(
            "[bold]Game Commands[/bold]\n"
            "Type [bold]/q[/bold] to quit the game\n"
            "Type [bold]/r[/bold] to restart with new user"
        )
        command_text.stylize(self.colors["commands"])
        
        return Panel(
            command_text,
            box=box.ROUNDED,
            border_style=self.colors["commands"],
            title="Keyboard Commands",
            width=30
        )
        
    def create_divider(self):
        """Create a divider."""
        return Text("─" * 70, style=self.colors["divider"], justify="center")
        
    def start_game_animation(self):
        """Start the background animation during gameplay."""
        self.animation_active = True
        current_mode = self.game_engine.mode
        
        def run_animation():
            frame_idx = 0
            
            if current_mode == "scientists":
                camera_frames = self.animation.SCIENCE_GAME_ANIMATION_FRAMES
            else:
                camera_frames = self.animation.GAME_ANIMATION_FRAMES
            
            while self.animation_active:
                if not hasattr(self, 'busy') or not self.busy:
                    frame = camera_frames[frame_idx % len(camera_frames)]
                    
                    lines = frame.split('\n')
                    with self.console.capture() as capture:
                        for line in lines:
                            self.console.print(line, end='\n')
                            
                    frame_idx += 1
                    
                time.sleep(0.5)
                
        self.game_animation_thread = threading.Thread(target=run_animation)
        self.game_animation_thread.daemon = True
        self.game_animation_thread.start()
        
    def stop_game_animation(self):
        """Stop the game animation."""
        self.animation_active = False
        if self.game_animation_thread:
            self.game_animation_thread.join(timeout=1.0)
    
    def get_username(self):
        """
        Ask for and return the player's username.
        
        Returns:
            str: Player's username
        """
        self.clear_screen()
        
        self.console.print()
        self.console.print(self.create_title("GUESS WHO I AM", use_figlet=True), justify="center")
        self.console.print()
        
        username_panel = Panel(
            Text("Please enter your username to start the game:", style=self.colors["prompt"]),
            box=box.ROUNDED,
            border_style=self.colors["info"],
            width=60
        )
        
        self.console.print(username_panel, justify="center")
        self.console.print()

        self.show_scoreboard()
        self.console.print()
        
        username = questionary.text(
            "Username:",
            style=self.question_style
        ).ask()
        
        while not username or len(username.strip()) == 0:
            self.console.print("Username cannot be empty. Please try again.", style=self.colors["failure"])
            username = questionary.text(
                "Username:",
                style=self.question_style
            ).ask()
        
        username = username.strip()
        
        if self.db.user_exists(username):
            self.console.print(f"Welcome back, {username}!", style=self.colors["success"])
            time.sleep(1)

            best_score = self.db.get_user_best_score(username)
            if best_score > 0:
                self.console.print(f"Your best score so far is: {best_score}", style=self.colors["info"])
                time.sleep(1)
        else:
            self.console.print(f"Welcome, {username}! A new player has joined.", style=self.colors["info"])
            time.sleep(1)
        
        return username
        
    def select_game_mode(self):
        """Let the player select a game mode."""
        self.clear_screen()
        
        self.animation.play_welcome_animation(color=self.colors["title"])
        
        self.console.print()
        self.console.print(self.create_title("GUESS WHO I AM", use_figlet=True), justify="center")
        self.console.print()
        
        mode_panel = Panel(
            Text.from_markup(
                "[bold]Choose a Category:[/bold]\n\n"
                "[red]Bollywood[/red] - Guess Indian film celebrities\n"
                "[blue]Hollywood[/blue] - Guess American/International film celebrities\n"
                "[green]Scientists[/green] - Guess famous scientists and inventors\n"
                "[yellow]All Categories[/yellow] - Mix of celebrities and scientists"
            ),
            box=box.ROUNDED,
            border_style=self.colors["info"],
            width=60
        )
        
        self.console.print(mode_panel, justify="center")
        self.console.print()
        
        mode = questionary.select(
            "Select game mode:",
            choices=[
                "Bollywood",
                "Hollywood",
                "Scientists",
                "All Categories"
            ],
            style=self.question_style
        ).ask()
        
        if mode == "Scientists":
            self.animation.play_scientist_animation(color=self.colors["scientists"])
        else:
            self.animation.play_loading_animation(
                text=f"Setting up {mode} mode", 
                color=self.colors["info"],
                duration=2
            )
        
        if mode == "Bollywood":
            return "bollywood"
        elif mode == "Hollywood":
            return "hollywood"
        elif mode == "Scientists":
            return "scientists"
        else:
            return "all"
        
    def show_menu(self):
        """Display the game's main menu and get username."""
        # Get username first
        username = self.get_username()
        self.game_engine.set_username(username)
        
        mode = self.select_game_mode()
        self.game_engine.set_mode(mode)
        self.animation.set_mode(mode)
        
        self.clear_screen()
        
        self.console.print()
        self.console.print(self.create_title("GUESS WHO I AM", use_figlet=True), justify="center")
        self.console.print(self.create_mode_title(), justify="center")
        self.console.print()

        player_panel = Panel(
            Text(f"Player: {username}", style=self.colors["username"]),
            box=box.ROUNDED,
            border_style=self.colors["username"],
            width=30
        )
        
        self.console.print(player_panel, justify="center")
        self.console.print()

        if mode == "bollywood":
            count = len(get_all_bollywood_celebrities())
            category = "Bollywood celebrities"
        elif mode == "hollywood":
            count = len(get_all_hollywood_celebrities())
            category = "Hollywood celebrities"
        elif mode == "scientists":
            count = len(get_all_scientists())
            category = "famous scientists"
        else:
            count = len(get_all_celebrities())
            category = "famous people"
        
        instructions = Panel(
            Text.from_markup(
                f"[bold]Can you guess the {category}?[/bold]\n\n"
                f"I'm thinking of one of {count} {category}.\n"
                "I'll give you a description with several clues.\n"
                "You have 2 guesses to figure out who I'm thinking of.\n"
                "Your score increases based on how many guesses you have left.\n"
                "If you guess correctly, you continue with a new person!"
            ),
            box=box.ROUNDED,
            border_style=self.colors["info"],
            width=60
        )
        
        self.console.print(instructions, justify="center")
        self.console.print()
        
        commands_panel = self.create_commands_panel()
        self.console.print(commands_panel, justify="center")
        self.console.print()

        self.show_scoreboard(mode)
        
        self.console.print()
        questionary.confirm(
            "Are you ready to start?",
            default=True,
            style=self.question_style
        ).ask()
    
    def show_scoreboard(self, mode=None):
        """Display the top scores."""
        scores = self.db.get_top_scores(mode=mode, limit=5)
        
        if not scores:
            scoreboard = Panel(
                Text("No scores recorded yet. Be the first!", style=self.colors["info"]),
                title="Top Scores",
                title_align="center",
                box=box.ROUNDED,
                border_style=self.colors["info"],
                width=60
            )
            
            self.console.print(scoreboard, justify="center")
            return
            
        table = Table(
            title="Top Scores",
            title_style=self.colors["subtitle"],
            box=box.ROUNDED,
            border_style=self.colors["info"],
            header_style=self.colors["highlight"],
            width=60
        )
        
        table.add_column("Rank", style="dim", width=6)
        table.add_column("Username", style=self.colors["username"])
        table.add_column("Score", style=self.colors["score"], justify="right")
        table.add_column("Mode", style=self.colors["info"])
        
        for i, (username, score, mode, _) in enumerate(scores, 1):
            table.add_row(f"#{i}", username, str(score), mode.capitalize())
            
        self.console.print(table, justify="center")
    
    def show_game_screen(self):
        """Display the main game screen."""
        self.clear_screen()
        
        self.console.print()
        self.console.print(self.create_title("GUESS WHO I AM", use_figlet=True), justify="center")
        self.console.print(self.create_mode_title(), justify="center")
        self.console.print()
        
        game_state = self.game_engine.get_game_state()
        
        player_panel = Panel(
            Text(f"Player: {game_state['username']} | Score: {game_state['score']}", 
                 style=self.colors["username"]),
            box=box.ROUNDED,
            border_style=self.colors["info"],
            width=60
        )
        
        self.console.print(player_panel, justify="center")
        self.console.print()

        progress_text = Text(
            f"People guessed: {game_state['guessed_count']}/{game_state['total_count']}",
            style=self.colors["info"],
            justify="center"
        )
        
        progress_panel = Panel(
            progress_text,
            box=box.ROUNDED,
            border_style=self.colors["info"],
            width=40
        )
        
        self.console.print(progress_panel, justify="center")
        self.console.print()
        
        remaining = game_state['guesses_remaining']
        remaining_style = (
            self.colors["success"] if remaining == 2 else 
            self.colors["failure"]
        )
        
        remaining_text = Text(
            f"Guesses remaining: {remaining}",
            style=remaining_style,
            justify="center"
        )
        
        remaining_panel = Panel(
            remaining_text,
            box=box.ROUNDED,
            border_style=remaining_style,
            width=30
        )
        
        self.console.print(remaining_panel, justify="center")
        self.console.print()
        
        description_panel = Panel(
            Text(game_state['mystery_celebrity']['description'], style=self.colors["question"]),
            title="Clues",
            title_align="center",
            box=box.ROUNDED,
            border_style=self.colors["info"],
            width=70
        )
        
        self.console.print(description_panel, justify="center")
        self.console.print()
        
        commands_panel = self.create_commands_panel()
        self.console.print(commands_panel, justify="center")
        self.console.print()
        
    def show_correct_guess_screen(self, celebrity):
        """
        Display a screen for a correct guess.
        
        Args:
            celebrity: The correctly guessed celebrity
        """
        self.clear_screen()
        current_mode = self.game_engine.mode
        
        self.console.print()
        self.animation.play_win_animation(
            color=self.colors["success"], 
            loops=1,
            mode=current_mode
        )
        
        win_title = pyfiglet.figlet_format("CORRECT!", font="small")
        self.console.print(Text(win_title, style=self.colors["success"]), justify="center")
        self.console.print()
        
        result_panel = Panel(
            Text(f"You correctly guessed {celebrity['answer']}!", style=self.colors["success"]),
            box=box.ROUNDED,
            border_style=self.colors["success"],
            width=60
        )
        
        self.console.print(result_panel, justify="center")
        self.console.print()
        
        description_panel = Panel(
            Text(celebrity['description'], style=self.colors["info"]),
            title="The Clues",
            title_align="center",
            box=box.ROUNDED,
            border_style=self.colors["info"],
            width=70
        )
        
        self.console.print(description_panel, justify="center")
        self.console.print()
        
        game_state = self.game_engine.get_game_state()
        
        score_panel = Panel(
            Text(f"Your score: {game_state['score']} (+{self.game_engine.guesses_remaining})", 
                 style=self.colors["score"]),
            box=box.ROUNDED,
            border_style=self.colors["success"],
            width=30
        )
        
        self.console.print(score_panel, justify="center")
        self.console.print()
        
        commands_panel = self.create_commands_panel()
        self.console.print(commands_panel, justify="center")
        self.console.print()
        
        self.console.print("Get ready for the next person!", 
                          style=self.colors["info"], justify="center")
        self.console.print()
        
        user_input = input("Press Enter to continue (or type /q to quit, /r to restart): ")
        if user_input.lower() == "/q":
            return "quit"
        elif user_input.lower() == "/r":
            return "restart"
        return "continue"
        
    def show_game_over_screen(self):
        """
        Display the game over screen.
        
        Returns:
            bool: Whether the player wants to play again
            bool: Whether the player wants to change their username
        """
        self.clear_screen()
        
        game_state = self.game_engine.get_game_state()
        celeb = game_state['mystery_celebrity']
        current_mode = game_state['mode']
        
        self.console.print()
        
        self.animation.play_lose_animation(
            color=self.colors["failure"],
            mode=current_mode
        )
        
        game_over = pyfiglet.figlet_format("GAME OVER", font="small")
        self.console.print(Text(game_over, style=self.colors["failure"]), justify="center")
        self.console.print()
        
        result_panel = Panel(
            Text(f"The answer was {celeb['answer']}!", style=self.colors["failure"]),
            box=box.ROUNDED,
            border_style=self.colors["failure"],
            width=60
        )
        
        self.console.print(result_panel, justify="center")
        
        score_panel = Panel(
            Text(f"Your final score: {game_state['score']}", style=self.colors["score"]),
            box=box.ROUNDED,
            border_style=self.colors["failure"],
            width=30
        )
        
        self.console.print(score_panel, justify="center")

        if game_state['score'] > 0:
            self.db.add_score(game_state['username'], game_state['score'], game_state['mode'])
        
        self.console.print()
        
        description_panel = Panel(
            Text(celeb['description'], style=self.colors["info"]),
            title="The Clues",
            title_align="center",
            box=box.ROUNDED,
            border_style=self.colors["info"],
            width=70
        )
        
        self.console.print(description_panel, justify="center")
        self.console.print()
        
        self.show_scoreboard(game_state['mode'])
        self.console.print()
        
        play_again = questionary.confirm(
            "Would you like to play again?",
            default=True,
            style=self.question_style
        ).ask()
        
        if play_again:
            change_user = questionary.confirm(
                "Would you like to restart with a new user?",
                default=False,
                style=self.question_style
            ).ask()
            
            if change_user:
                return play_again, True
            
            if game_state['category_completed']:
                change_mode = questionary.confirm(
                    "You've guessed all people in this category! Would you like to change the game mode?",
                    default=True,
                    style=self.question_style
                ).ask()
                
                if change_mode:
                    mode = self.select_game_mode()
                    self.game_engine.set_mode(mode)
                    self.animation.set_mode(mode)
            
        return play_again, False

    def handle_special_commands(self, input_value):
        """
        Check for and handle special commands.
        
        Args:
            input_value (str): User input to check
            
        Returns:
            str: Command action if special command, None otherwise
        """
        if not input_value:
            return None
            
        if input_value.lower() == "/q":
            if questionary.confirm(
                "Are you sure you want to quit the game?",
                default=False,
                style=self.question_style
            ).ask():
                return "quit"
            return "cancel"
            
        elif input_value.lower() == "/r":
            if questionary.confirm(
                "Are you sure you want to restart with a new user?",
                default=False,
                style=self.question_style
            ).ask():
                return "restart"
            return "cancel"
            
        return None
        
    def get_player_action(self):
        """
        Get the player's next action.
        
        Returns:
            str: The action chosen
            str: Additional input if needed
        """
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "Make a guess",
                "Quit game"
            ],
            style=self.question_style
        ).ask()
            
        if choice == "Make a guess":
            self.console.print()

            if self.game_engine.mode == "bollywood":
                celeb_names = [c["answer"] for c in get_all_bollywood_celebrities()]
            elif self.game_engine.mode == "hollywood":
                celeb_names = [c["answer"] for c in get_all_hollywood_celebrities()]
            elif self.game_engine.mode == "scientists":
                celeb_names = [c["answer"] for c in get_all_scientists()]
            else:
                celeb_names = [c["answer"] for c in self.game_engine.celebrities]

            self.console.print("Type /q to quit or /r to restart with new user", 
                              style=self.colors["commands"])
            
            guess = questionary.autocomplete(
                "Who do you think it is? Enter the full name:",
                choices=celeb_names,
                style=self.question_style
            ).ask()
            
            cmd = self.handle_special_commands(guess)
            if cmd == "quit":
                return "quit", None
            elif cmd == "restart":
                return "restart", None
            elif cmd == "cancel":
                return "invalid", None
            
            return "guess", guess
            
        elif choice == "Quit game":
            if questionary.confirm(
                "Are you sure you want to quit?",
                default=False,
                style=self.question_style
            ).ask():
                return "quit", None
            else:
                return "invalid", None
        
    def run_game_loop(self):
        """
        Run the main game loop.
        
        Returns:
            bool: Whether to play again
        """
        self.show_menu()
        self.game_engine.start_new_game()
        
        self.start_game_animation()
        
        game_running = True
        restart_with_new_user = False
        
        while game_running:
            self.show_game_screen()
            
            action, value = self.get_player_action()
                    
            if action == "guess":
                if value:
                    self.busy = True 
                    is_correct, continue_game, score, new_round = self.game_engine.process_guess(value)
                    
                    self.console.print()
                    
                    if is_correct:
                        current_celeb = self.game_engine.mystery_celebrity

                        result = self.show_correct_guess_screen(current_celeb)
                        if result == "quit":
                            game_running = False
                        elif result == "restart":
                            game_running = False
                            restart_with_new_user = True
                        else:
                            if new_round:
                                self.game_engine.start_new_game()
                    else:
                        result_panel = Panel(
                            Text("That's not correct!", style=self.colors["failure"]),
                            box=box.ROUNDED,
                            border_style=self.colors["failure"],
                            width=60
                        )
                    
                        self.console.print(result_panel, justify="center")
                        
                        if not continue_game:
                            game_running = False
                        else:
                            self.console.print()
                            user_input = input("\nPress Enter to continue (or type /q to quit, /r to restart): ")
                            if user_input.lower() == "/q":
                                game_running = False
                            elif user_input.lower() == "/r":
                                game_running = False
                                restart_with_new_user = True
                    
                    self.busy = False
                    
            elif action == "quit":
                game_running = False
            
            elif action == "restart":
                game_running = False
                restart_with_new_user = True
        
        self.stop_game_animation()

        if restart_with_new_user:
            username = self.get_username()
            self.game_engine.set_username(username)
            self.game_engine.score = 0
            return True

        play_again, new_user = self.show_game_over_screen()
        
        if play_again and new_user:
            username = self.get_username()
            self.game_engine.set_username(username)
            self.game_engine.score = 0
            
        return play_again