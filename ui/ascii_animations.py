import time
import random
import threading
import sys
from rich.console import Console
from rich.text import Text

WELCOME_ANIMATION = [
    """
    ★彡 ⭐ ★彡 ⭐ ★彡 ⭐ ★彡 ⭐ ★彡 ⭐ ★彡 ⭐ ★彡 ⭐ ★彡 ⭐
    
     ██╗    ██╗██╗  ██╗ ██████╗      █████╗ ███╗   ███╗    ██╗██████╗
     ██║    ██║██║  ██║██╔═══██╗    ██╔══██╗████╗ ████║    ██║╚════██╗
     ██║ █╗ ██║███████║██║   ██║    ███████║██╔████╔██║    ██║ █████╔╝
     ██║███╗██║██╔══██║██║   ██║    ██╔══██║██║╚██╔╝██║    ██║██╔═══╝ 
     ╚███╔███╔╝██║  ██║╚██████╔╝    ██║  ██║██║ ╚═╝ ██║    ██║███████╗
      ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝     ╚═╝  ╚═╝╚═╝     ╚═╝    ╚═╝╚══════╝
                                                                       
    🎬 GUESS WHO I AM 🎬
    
    ★彡 ⭐ ★彡 ⭐ ★彡 ⭐ ★彡 ⭐ ★彡 ⭐ ★彡 ⭐ ★彡 ⭐ ★彡 ⭐
    """,
    """
    ⭐ ★彡 ⭐ ★彡 ⭐ ★彡 ⭐ ★彡 ⭐ ★彡 ⭐ ★彡 ⭐ ★彡 ⭐ ★彡
    
     ██╗    ██╗██╗  ██╗ ██████╗      █████╗ ███╗   ███╗    ██╗██████╗
     ██║    ██║██║  ██║██╔═══██╗    ██╔══██╗████╗ ████║    ██║╚════██╗
     ██║ █╗ ██║███████║██║   ██║    ███████║██╔████╔██║    ██║ █████╔╝
     ██║███╗██║██╔══██║██║   ██║    ██╔══██║██║╚██╔╝██║    ██║██╔═══╝ 
     ╚███╔███╔╝██║  ██║╚██████╔╝    ██║  ██║██║ ╚═╝ ██║    ██║███████╗
      ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝     ╚═╝  ╚═╝╚═╝     ╚═╝    ╚═╝╚══════╝
                                                                       
    ✨ CELEBRITIES, STARS, & BRILLIANT MINDS! ✨
    
    ⭐ ★彡 ⭐ ★彡 ⭐ ★彡 ⭐ ★彡 ⭐ ★彡 ⭐ ★彡 ⭐ ★彡 ⭐ ★彡
    """,
    """
    🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨
    
     ██╗    ██╗██╗  ██╗ ██████╗      █████╗ ███╗   ███╗    ██╗██████╗
     ██║    ██║██║  ██║██╔═══██╗    ██╔══██╗████╗ ████║    ██║╚════██╗
     ██║ █╗ ██║███████║██║   ██║    ███████║██╔████╔██║    ██║ █████╔╝
     ██║███╗██║██╔══██║██║   ██║    ██╔══██║██║╚██╔╝██║    ██║██╔═══╝ 
     ╚███╔███╔╝██║  ██║╚██████╔╝    ██║  ██║██║ ╚═╝ ██║    ██║███████╗
      ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝     ╚═╝  ╚═╝╚═╝     ╚═╝    ╚═╝╚══════╝
                                                                       
    📽️ BOLLYWOOD, HOLLYWOOD & SCIENTISTS 📽️
    
    🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨
    """,
    """
    ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟
    
    █▀█ █▀█ █▀▀ █▀▀ █▀▀ █▄░█ ▀█▀ █ █▄░█ █▀▀   ▀█▀ █░█ █▀▀
    █▀▀ █▀▄ ██▄ ▀▀█ ██▄ █░▀█ ░█░ █ █░▀█ █▄█   ░█░ █▀█ ██▄
    
    ░█▀▀░█▀▀░█░░░█▀▀░█▀▄░█▀▄░▀█▀░▀█▀░▀▄░▄▀
    ░█░░░█▀▀░█░░░█▀▀░█▀▄░█▀▄░░█░░░█░░░█░░
    ░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀▀░░▀░▀░▀▀▀░░▀░░░▀░░
    
    ░█▀▀░█░█░█▀▀░█▀▀░█▀▀░▀█▀░█▀█░█▀▀░░░█▀▀░█▀█░█▄█░█▀▀
    ░█░█░█░█░█▀▀░▀▀█░▀▀█░░█░░█░█░█░█░░░█░█░█▀█░█░█░█▀▀
    ░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░▀░░▀░▀░▀▀▀░░░▀▀▀░▀░▀░▀░▀░▀▀▀
    
    ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟 ✨ 🌟
    """,
    """
    🎬 📽️ 🎞️ 🎭 🎬 📽️ 🎞️ 🎭 🎬 📽️ 🎞️ 🎭 🎬 📽️ 🎞️ 🎭 🎬 
    
                        .-=+*+=-:.                           
                    .=*#@@@@#:                             
                   =#@@@@@@@@+                             
                  +@@@@@@@@@@+                             
                  *@@@@@@@@@@+                             
                  :+=*@@@@@@@+                             
                     .%@@@@@%+                             
                     .%@@@@@%+                             
                    .#@@@@@@%=                             
                -. :%@@@@@@@%+::=++++=-:.                  
               +%#%@@@@@@@@@@@@@@@@@@@@@%%%*=:             
              =@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%+.           
              %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#            
              %@@@@@@@@@@@@@@@@@@@%@@@@@@@@@@%:            
              =@@@@@@@@@@@@@@%%@@%@@@@@@@@@@%=             
              .+@@@@@@@@@%@@@@@@@@@@@@@@@@%+.              
                :%%@@@@@@@@@@@@@@@@@@@@@@%.                
                 :*@@@@@@@@@@@@@@@@@@@@@#:                 
                   =@@@@@@@@@@@@@@@@@%%=                   
                    .=#@@@@@@@@@@@#+:                      
                       .:=++++=:.                          
    
    🎬 📽️ 🎞️ 🎭 🎬 📽️ 🎞️ 🎭 🎬 📽️ 🎞️ 🎭 🎬 📽️ 🎞️ 🎭 🎬
    """,
    """
    🎭 🎬 📽️ 🎞️ 🎭 🎬 📽️ 🎞️ 🎭 🎬 📽️ 🎞️ 🎭 🎬 📽️ 🎞️ 🎭 🎬
    
     █░█░█ █░█ █▀█   █▀█ █▀▄▀█   █   ▀█
     ▀▄▀▄▀ █▀█ █▄█   █▀█ █░▀░█   █   █▄
    
     ▄▀█   █▀▀ █░█ █▀▀ █▀ █▀ █ █▄░█ █▀▀   █▀▀ ▄▀█ █▀▄▀█ █▀▀
     █▀█   █▄█ █▄█ ██▄ ▄█ ▄█ █ █░▀█ █▄█   █▄█ █▀█ █░▀░█ ██▄
    
     █▀█ █░░ ▄▀█ █▄█   █▄░█ █▀█ █░█ █
     █▀▀ █▄▄ █▀█ ░█░   █░▀█ █▄█ █▄█ ▄
    
    🎭 🎬 📽️ 🎞️ 🎭 🎬 📽️ 🎞️ 🎭 🎬 📽️ 🎞️ 🎭 🎬 📽️ 🎞️ 🎭 🎬
    """
]

SCIENTIST_ANIMATION_FRAMES = [
    """
     ⚛️  🧪  🔬  🧬  ⚛️  🧪  🔬  🧬  ⚛️  🧪  🔬  🧬  ⚛️ 
          _____       _                      
         / ____|     (_)                     
        | (___   ___ _  ___ _ __   ___ ___  
         \\___ \\ / __| |/ _ \\ '_ \\ / __/ _ \\ 
         ____) | (__| |  __/ | | | (_|  __/ 
        |_____/ \\___|_|\\___|_| |_|\\___\\___| 
                                           
        GREAT MINDS & DISCOVERIES
     ⚛️  🧪  🔬  🧬  ⚛️  🧪  🔬  🧬  ⚛️  🧪  🔬  🧬  ⚛️ 
    """,
    """
     🧬  ⚛️  🧪  🔬  🧬  ⚛️  🧪  🔬  🧬  ⚛️  🧪  🔬  🧬 
                _         
       ___  ___(_)___ ___ 
      / _ \\/ __| / __/ _ \\
     |  __/\\__ \\ \\__ \\  __/
      \\___||___/_|___/\\___|
                       
        INNOVATIONS & BREAKTHROUGHS
     🧬  ⚛️  🧪  🔬  🧬  ⚛️  🧪  🔬  🧬  ⚛️  🧪  🔬  🧬 
    """,
    """
     🔬  🧬  ⚛️  🧪  🔬  🧬  ⚛️  🧪  🔬  🧬  ⚛️  🧪  🔬
            
       .d8888b.  888    888 8888888888 .d8888b.  .d8888b.  
      d88P  Y88b 888    888 888       d88P  Y88b d88P  Y88b 
      888    888 888    888 888       Y88b.      Y88b.      
      888        888888 888 8888888    "Y888b.    "Y888b.   
      888  88888 888    888 888           "Y88b.     "Y88b. 
      888    888 888    888 888             "888       "888 
      Y88b  d88P Y88b  d88P 888       Y88b  d88P Y88b  d88P 
       "Y8888P88  "Y8888P88 8888888888 "Y8888P"   "Y8888P"  
                                              
     🔬  🧬  ⚛️  🧪  🔬  🧬  ⚛️  🧪  🔬  🧬  ⚛️  🧪  🔬
    """
]

GAME_ANIMATION_FRAMES = [
    """
    ┌─────────────┐
    │  ▄▄▄▄▄▄▄▄▄  │
    │ █ ◢█████◣ █ │
    │ █ ▌ o o ▐ █ │  GUESS
    │ █ ▌  ▿  ▐ █ │  WHO
    │ █  ▀▀▀▀▀  █ │  I AM!
    └─────────────┘
    """,
    """
    ┌─────────────┐
    │ ←▄▄▄▄▄▄▄▄▄→ │
    │ █ ◢█████◣ █ │
    │ █ ▌ - - ▐ █ │  GUESS
    │ █ ▌  ▿  ▐ █ │  WHO
    │ █  ▀▀▀▀▀  █ │  I AM!
    └─────────────┘
    """,
    """
    ┌─────────────┐
    │  ▄▄▄▄▄▄▄▄▄  │
    │ █ ◢█████◣ █ │
    │ █ ▌ o o ▐ █ │  GUESS
    │ █ ▌  ▿  ▐ █ │  WHO
    │ █  ▀▀▀▀▀  █ │  I AM!
    └─────────────┘
    """,
]

SCIENCE_GAME_ANIMATION_FRAMES = [
    """
    ┌─────────────┐
    │  ⚗️   🧪  ⚛️  │
    │ 🔬      🧬  │
    │    🧠       │  SCIENCE
    │  🧮      📊  │  MINDS
    │  📡   🔭  💻  │  QUIZ!
    └─────────────┘
    """,
    """
    ┌─────────────┐
    │  ⚛️   🧪  ⚗️  │
    │ 🧬      🔬  │
    │    🧠       │  SCIENCE
    │  📊      🧮  │  MINDS
    │  💻   🔭  📡  │  QUIZ!
    └─────────────┘
    """,
    """
    ┌─────────────┐
    │  🧪   ⚛️  ⚗️  │
    │ 🔬      🧬  │
    │    🧠       │  SCIENCE
    │  🧮      📊  │  MINDS
    │  📡   💻  🔭  │  QUIZ!
    └─────────────┘
    """,
]

WIN_ANIMATION_FRAMES = [
    """
      ___________
     '._==_==_=_.'
     .-\\:      /-.
    | (|:.     |) |
     '-|:.     |-'
       \\::.    /
        '::. .'
          ) (
        _.' '._
       `"""""""`
    """,
    """
      ___________
     '._==_==_=_.'
     .-\\:      /-.
    | (|:.     |) |    WINNER!
     '-|:.     |-'     
       \\::.    /      
        '::. .'        
          ) (        
        _.' '._       
       `"""""""`       
    """,
    """
      ___________
     '._==_==_=_.'     ★
     .-\\:      /-.    ★
    | (|:.     |) |   WINNER!
     '-|:.     |-'    ★
       \\::.    /      ★
        '::. .'        
          ) (        
        _.' '._       
       `"""""""`       
    """,
    """
      ___________      ★
     '._==_==_=_.'    ★ ★
     .-\\:      /-.   ★   ★
    | (|:.     |) |  WINNER!
     '-|:.     |-'   ★   ★
       \\::.    /     ★ ★
        '::. .'       ★
          ) (        
        _.' '._       
       `"""""""`       
    """,
]

SCIENCE_WIN_ANIMATION_FRAMES = [
    """
       _____
      |  __ \\
      | |__) |___  ___  ___  __ _ _ __ ___| |__  
      |  _  // _ \\/ __|/ _ \\/ _` | '__/ __| '_ \\ 
      | | \\ \\  __/\\__ \\  __/ (_| | | | (__| | | |
      |_|  \\_\\___||___/\\___|\\__,_|_|  \\___|_| |_|
      
       _____                          _ 
      / ____|                        | |
     | |  __  ___ _ __  _   _ ___   | |
     | | |_ |/ _ \\ '_ \\| | | / __|  | |
     | |__| |  __/ | | | |_| \\__ \\  |_|
      \\_____|\\___||_| |_|\\__,_|___/  (_)
                                         
    """,
    """
      🧪 🔬 ⚗️ ⚛️ 🧬 🧪 🔬 ⚗️ ⚛️ 🧬 🧪 🔬 ⚗️ ⚛️ 🧬 
      
       _____                          _ 
      / ____|                        | |
     | |  __  ___ _ __  _   _ ___   | |
     | | |_ |/ _ \\ '_ \\| | | / __|  | |
     | |__| |  __/ | | | |_| \\__ \\  |_|
      \\_____|\\___||_| |_|\\__,_|___/  (_)
     
      BRILLIANT DEDUCTION!
      
      🧪 🔬 ⚗️ ⚛️ 🧬 🧪 🔬 ⚗️ ⚛️ 🧬 🧪 🔬 ⚗️ ⚛️ 🧬
    """,
    """
      ⚛️ 🧪 🔬 🧬 ⚛️ 🧪 🔬 🧬 ⚛️ 🧪 🔬 🧬 ⚛️ 🧪 
      
       _____                          _ 
      / ____|                        | |
     | |  __  ___ _ __  _   _ ___   | |  ★
     | | |_ |/ _ \\ '_ \\| | | / __|  | |  ★
     | |__| |  __/ | | | |_| \\__ \\  |_|
      \\_____|\\___||_| |_|\\__,_|___/  (_)
      
      EUREKA! YOU'VE GOT IT!  ★
      
      ⚛️ 🧪 🔬 🧬 ⚛️ 🧪 🔬 🧬 ⚛️ 🧪 🔬 🧬 ⚛️ 🧪
    """,
    """
      🔬 ⚗️ ⚛️ 🧬 🔬 ⚗️ ⚛️ 🧬 🔬 ⚗️ ⚛️ 🧬 🔬 ⚗️ 
      
       _____                          _   ★
      / ____|                        | | ★ ★
     | |  __  ___ _ __  _   _ ___   | |★   ★
     | | |_ |/ _ \\ '_ \\| | | / __|  | | ★ ★
     | |__| |  __/ | | | |_| \\__ \\  |_|  ★
      \\_____|\\___||_| |_|\\__,_|___/  (_)
     
      SCIENTIFIC BREAKTHROUGH!
      
      🔬 ⚗️ ⚛️ 🧬 🔬 ⚗️ ⚛️ 🧬 🔬 ⚗️ ⚛️ 🧬 🔬 ⚗️
    """,
]

LOSE_ANIMATION_FRAMES = [
    """
     +-------+
     |       |
     | x   x |
     |       |
     |  ===  |
     +-------+
    """,
    """
     +-------+
     |       |
     | -   - |
     |       |
     |  ===  |
     +-------+
    """,
    """
     +-------+
     |       |
     | x   x |
     |       |
     |  ===  |
     +-------+
    """,
    """
     +-------+
     |       |
     | -   - |
     |       |
     |   v   |
     +-------+
    """
]

SCIENCE_LOSE_ANIMATION_FRAMES = [
    """
     +-------+
     |       |
     |Hmm... |
     | x   x |
     |       |
     |  ===  |
     +-------+
    """,
    """
     +-------+
     |       |
     |Back to|
     | -   - |
     |the lab|
     |  ===  |
     +-------+
    """,
    """
     +-------+
     |       |
     |Experi-|
     | x   x |
     | -ment |
     |  ===  |
     |Failed!|
     +-------+
    """,
    """
     +-------+
     |       |
     |Hypoth-|
     | -   - |
     | -esis |
     |   v   |
     |Denied!|
     +-------+
    """
]

LOADING_ANIMATION_FRAMES = [
    """
     ╔═══════╗
     ║   5   ║
     ╚═══════╝
    """,
    """
     ╔═══════╗
     ║   4   ║
     ╚═══════╝
    """,
    """
     ╔═══════╗
     ║   3   ║
     ╚═══════╝
    """,
    """
     ╔═══════╗
     ║   2   ║
     ╚═══════╝
    """,
    """
     ╔═══════╗
     ║   1   ║
     ╚═══════╝
    """,
    """
     ╔═══════╗
     ║  GO!  ║
     ╚═══════╝
    """
]

class AnimationController:
    """Controls and displays ASCII animations."""
    
    def __init__(self, console):
        """
        Initialize the animation controller.
        
        Args:
            console: Rich console instance for display
        """
        self.console = console
        self.stop_animation = False
        self.animation_thread = None
        self.current_mode = "all"
        
        self.GAME_ANIMATION_FRAMES = GAME_ANIMATION_FRAMES
        self.SCIENCE_GAME_ANIMATION_FRAMES = SCIENCE_GAME_ANIMATION_FRAMES
        self.WIN_ANIMATION_FRAMES = WIN_ANIMATION_FRAMES
        self.SCIENCE_WIN_ANIMATION_FRAMES = SCIENCE_WIN_ANIMATION_FRAMES
        self.LOSE_ANIMATION_FRAMES = LOSE_ANIMATION_FRAMES
        self.SCIENCE_LOSE_ANIMATION_FRAMES = SCIENCE_LOSE_ANIMATION_FRAMES
        
    def set_mode(self, mode):
        """Set the current game mode to use appropriate animations."""
        self.current_mode = mode
        
    def play_welcome_animation(self, color="bright_yellow", loops=2):
        """
        Play the welcome animation.
        
        Args:
            color: Color of the animation
            loops: Number of loops to play
        """
        self.stop_animation = False
        
        for _ in range(loops):
            if self.stop_animation:
                break
                
            for frame in WELCOME_ANIMATION:
                if self.stop_animation:
                    break
                    
                self.console.clear()
                self.console.print()
                self.console.print(Text(frame, style=color), justify="center")
                time.sleep(0.5)
                
    def start_game_animation(self, color="bright_cyan", mode=None):
        """
        Start the game animation in a background thread.
        
        Args:
            color: Color of the animation
            mode: Game mode to determine animation style
        """
        self.stop_animation = False
        mode = mode or self.current_mode
        
        def animation_loop():
            """Animation loop to run in a separate thread."""
            frame_index = 0
            
            if mode == "scientists":
                frames = SCIENCE_GAME_ANIMATION_FRAMES
            else:
                frames = GAME_ANIMATION_FRAMES
            
            while not self.stop_animation:
                frame = frames[frame_index % len(frames)]
                frame_index += 1
                
                lines = frame.split('\n')
                sys.stdout.write("\033[s")
                
                for i, line in enumerate(lines):
                    if line.strip():
                        sys.stdout.write(f"\033[{i+1};60H{line}")
                
                sys.stdout.write("\033[u")
                sys.stdout.flush()
                
                time.sleep(0.5)
                
        self.animation_thread = threading.Thread(target=animation_loop)
        self.animation_thread.daemon = True
        self.animation_thread.start()
        
    def stop_game_animation(self):
        """Stop the currently running game animation."""
        self.stop_animation = True
        if self.animation_thread:
            self.animation_thread.join(1.0)
            
    def play_win_animation(self, color="bright_green", loops=3, mode=None):
        """
        Play the win animation.
        
        Args:
            color: Color of the animation
            loops: Number of loops to play
            mode: Game mode to determine animation style
        """
        self.stop_animation = False
        mode = mode or self.current_mode

        if mode == "scientists":
            frames = SCIENCE_WIN_ANIMATION_FRAMES
        else:
            frames = WIN_ANIMATION_FRAMES
            
        for _ in range(loops):
            if self.stop_animation:
                break
                
            for frame in frames:
                if self.stop_animation:
                    break
                    
                self.console.print()
                self.console.print(Text(frame, style=color), justify="center")
                time.sleep(0.3)
                
    def play_lose_animation(self, color="bright_red", loops=3, mode=None):
        """
        Play the lose animation.
        
        Args:
            color: Color of the animation
            loops: Number of loops to play
            mode: Game mode to determine animation style
        """
        self.stop_animation = False
        mode = mode or self.current_mode
        
        if mode == "scientists":
            frames = SCIENCE_LOSE_ANIMATION_FRAMES
        else:
            frames = LOSE_ANIMATION_FRAMES
            
        for _ in range(loops):
            if self.stop_animation:
                break
                
            for frame in frames:
                if self.stop_animation:
                    break
                    
                self.console.print()
                self.console.print(Text(frame, style=color), justify="center")
                time.sleep(0.3)
                
    def play_loading_animation(self, text="Loading", color="yellow", duration=3):
        """
        Play a loading animation with text.
        
        Args:
            text: Text to display alongside animation
            color: Color of the animation
            duration: Duration in seconds to play animation
        """
        self.console.clear()
        self.console.print()
        
        for frame in LOADING_ANIMATION_FRAMES:
            self.console.clear()
            self.console.print()
            self.console.print(Text(f"{text}", style=color), justify="center")
            self.console.print(Text(frame, style=color), justify="center")
            time.sleep(0.5)
            
        self.console.print()
        
    def play_scientist_animation(self, color="bright_cyan", loops=2):
        """
        Play a scientist-themed animation.
        
        Args:
            color: Color of the animation
            loops: Number of loops to play
        """
        self.stop_animation = False
        
        for _ in range(loops):
            if self.stop_animation:
                break
                
            for frame in SCIENTIST_ANIMATION_FRAMES:
                if self.stop_animation:
                    break
                    
                self.console.clear()
                self.console.print()
                self.console.print(Text(frame, style=color), justify="center")
                time.sleep(0.5)