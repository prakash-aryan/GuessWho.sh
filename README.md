# GuessWho.sh 🎮

A beautiful terminal-based guessing game that challenges your knowledge of Bollywood celebrities, Hollywood stars, and famous scientists from around the world!

[GuessWhoSh.webm](https://github.com/user-attachments/assets/4f6e35d1-75d0-4358-8db7-aa1b60bd2412)

## ✨ Overview

GuessWho.sh is an engaging CLI game where players are presented with descriptive clues about famous personalities. Put your knowledge to the test as you guess who's being described with only two chances per round. The game features colorful animations, persistent score tracking, and three distinct categories to explore.

## 🚀 How to Install

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone git@github.com:prakash-aryan/GuessWho.sh.git
   cd GuessWho.sh
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the game**
   ```bash
   python main.py
   ```

## 🎮 How to Play

1. **Enter your username** when prompted
2. **Select a category**:
   - Bollywood (15 Indian film celebrities)
   - Hollywood (15 international movie stars)
   - Scientists (25 brilliant minds, including 6 renowned Indian scientists)
   - All Categories (for the ultimate challenge!)

3. **Read the clues** carefully about the mystery person
4. **Make your guess** - you have two attempts per round
5. **Score points** based on your remaining guesses:
   - First attempt correct = 2 points
   - Second attempt correct = 1 point

6. **Continue playing** with new personalities after each correct guess
7. **Game ends** only when you fail to identify someone within two attempts

### Keyboard Commands
- During gameplay, you can type:
  - `/q` to quit the current game
  - `/r` to restart with a new user

## 🌟 Features

- **Rich, Colorful Interface** with category-specific animations
- **Persistent Score Tracking** across game sessions
- **Interactive Leaderboards** to compete with friends
- **Autocomplete** help when guessing names
- **Three Knowledge Categories** with 55 total personalities
- **SQLite Database** for reliable score storage

## 📝 Game Categories

### 1. Bollywood Celebrities
Test your knowledge of 15 iconic Indian film stars from legendary actors like Amitabh Bachchan to contemporary favorites like Deepika Padukone and Ranveer Singh.

### 2. Hollywood Stars
Challenge yourself with 15 international movie stars spanning different eras, from Meryl Streep to Dwayne "The Rock" Johnson.

### 3. Scientists & Inventors
Explore the minds that changed our world! This category features 25 scientists including:
- Historical giants like Albert Einstein and Marie Curie
- Computing pioneers like Alan Turing
- Indian luminaries like C.V. Raman and A.P.J. Abdul Kalam

## 📂 Project Structure

```
GuessWho.sh/
├── data/                    # Data files
│   ├── celebrities.py       # Contains all personalities and descriptions
│   └── __init__.py
├── logic/                   # Game logic
│   ├── game_engine.py       # Core game mechanics
│   └── __init__.py
├── ui/                      # User interface components
│   ├── ascii_animations.py  # Terminal animations
│   ├── terminal_ui.py       # UI components and screens
│   └── __init__.py
├── database.py              # Score database operations
├── main.py                  # Game entry point
├── README.md                # Documentation
└── requirements.txt         # Project dependencies
```

## 🛠️ Dependencies

- **rich** (≥10.0.0): Beautiful terminal formatting
- **questionary** (≥1.10.0): Interactive prompts and autocomplete
- **pyfiglet** (≥0.8.post1): ASCII art text

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---


Enjoy the game and test your knowledge of celebrities and scientists from around the world!

*"In the future, everyone will be famous for 15 minutes. Let's see if you can recognize who's who!" - Andy Warhol*
