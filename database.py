"""
Module for handling database operations for the celebrity guessing game.
"""

import sqlite3
import os
from datetime import datetime

class ScoreDatabase:
    """
    Handles database operations for storing and retrieving player scores.
    """
    
    def __init__(self, db_file="scores.db"):
        """
        Initialize the database connection.
        
        Args:
            db_file (str): Path to the SQLite database file
        """
        self.db_file = db_file
        self.init_db()
        
    def init_db(self):
        """Initialize the database by creating tables if they don't exist."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER NOT NULL,
            mode TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL COLLATE NOCASE,
            best_score INTEGER DEFAULT 0,
            first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()

        self.migrate_existing_users(conn)
        
        conn.close()
        
    def migrate_existing_users(self, conn=None):
        """
        Migrate existing users from scores table to players table.
        
        Args:
            conn (sqlite3.Connection, optional): Existing database connection
        """
        if conn is None:
            conn = sqlite3.connect(self.db_file)
            
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT username FROM scores")
        usernames = cursor.fetchall()
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for (username,) in usernames:
            cursor.execute("SELECT MAX(score) FROM scores WHERE username = ?", (username,))
            best_score = cursor.fetchone()[0] or 0

            cursor.execute("SELECT MIN(timestamp) FROM scores WHERE username = ?", (username,))
            first_seen = cursor.fetchone()[0] or current_time
            
            cursor.execute("SELECT COUNT(*) FROM players WHERE username COLLATE NOCASE = ?", (username,))
            exists = cursor.fetchone()[0] > 0
            
            if not exists:
                try:
                    cursor.execute(
                        "INSERT INTO players (username, best_score, first_seen, last_seen) VALUES (?, ?, ?, ?)",
                        (username, best_score, first_seen, current_time)
                    )
                    print(f"Migrated user: {username} with best score {best_score}")
                except sqlite3.Error as e:
                    print(f"Error migrating user {username}: {e}")
        
        conn.commit()
        
        if conn is not None:
            conn.close()
        
    def user_exists(self, username):
        """
        Check if a username exists in the database.
        
        Args:
            username (str): Username to check
            
        Returns:
            bool: True if the username exists, False otherwise
        """
        if not username:
            return False
            
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM players WHERE username COLLATE NOCASE = ?", (username,))
        count = cursor.fetchone()[0]
        
        if count == 0:
            cursor.execute("SELECT COUNT(*) FROM scores WHERE username COLLATE NOCASE = ?", (username,))
            count = cursor.fetchone()[0]
            
            if count > 0:
                print(f"Found user {username} in scores but not players, migrating...")
                self.migrate_existing_users()

                cursor.execute("SELECT COUNT(*) FROM players WHERE username COLLATE NOCASE = ?", (username,))
                count = cursor.fetchone()[0]
        
        conn.close()
        
        return count > 0
        
    def update_player(self, username, score):
        """
        Update player information or create a new player.
        
        Args:
            username (str): Player's username
            score (int): Current score to compare with best score
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute("SELECT best_score FROM players WHERE username COLLATE NOCASE = ?", (username,))
            result = cursor.fetchone()
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if result:
                best_score = result[0]
                if score > best_score:
                    cursor.execute(
                        "UPDATE players SET best_score = ?, last_seen = ? WHERE username COLLATE NOCASE = ?",
                        (score, current_time, username)
                    )
                else:
                    cursor.execute(
                        "UPDATE players SET last_seen = ? WHERE username COLLATE NOCASE = ?",
                        (current_time, username)
                    )
            else:
                cursor.execute(
                    "INSERT INTO players (username, best_score, first_seen, last_seen) VALUES (?, ?, ?, ?)",
                    (username, score, current_time, current_time)
                )
                
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating player: {e}")
            return False
            
    def get_user_best_score(self, username):
        """
        Get the best score for a user.
        
        Args:
            username (str): Player's username
            
        Returns:
            int: Best score for the user, 0 if user doesn't exist
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute("SELECT best_score FROM players WHERE username COLLATE NOCASE = ?", (username,))
        result = cursor.fetchone()
        
        if not result:
            cursor.execute("SELECT MAX(score) FROM scores WHERE username COLLATE NOCASE = ?", (username,))
            result = cursor.fetchone()
        
        conn.close()
        
        if result and result[0] is not None:
            return result[0]
        return 0
            
    def add_score(self, username, score, mode):
        """
        Add a new score entry to the database.
        
        Args:
            username (str): Player's username
            score (int): Player's score
            mode (str): Game mode played
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO scores (username, score, mode, timestamp) VALUES (?, ?, ?, ?)",
                (username, score, mode, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            
            conn.commit()
            conn.close()

            self.update_player(username, score)
            
            return True
        except Exception as e:
            print(f"Error adding score: {e}")
            return False
            
    def get_top_scores(self, mode=None, limit=10):
        """
        Retrieve top scores from the database.
        
        Args:
            mode (str, optional): Game mode to filter by
            limit (int): Number of scores to retrieve
            
        Returns:
            list: List of tuples containing (username, score, mode, timestamp)
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        if mode:
            cursor.execute(
                """
                SELECT s.username, MAX(s.score) as score, s.mode, MAX(s.timestamp) 
                FROM scores s
                WHERE s.mode = ?
                GROUP BY s.username COLLATE NOCASE
                ORDER BY score DESC
                LIMIT ?
                """,
                (mode, limit)
            )
        else:
            cursor.execute(
                """
                SELECT s.username, MAX(s.score) as score, s.mode, MAX(s.timestamp) 
                FROM scores s
                GROUP BY s.username COLLATE NOCASE
                ORDER BY score DESC
                LIMIT ?
                """,
                (limit,)
            )
            
        results = cursor.fetchall()
        conn.close()
        
        return results
        
    def get_player_history(self, username, limit=10):
        """
        Retrieve a player's score history.
        
        Args:
            username (str): Player's username
            limit (int): Number of scores to retrieve
            
        Returns:
            list: List of tuples containing (score, mode, timestamp)
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT score, mode, timestamp FROM scores WHERE username COLLATE NOCASE = ? ORDER BY timestamp DESC LIMIT ?",
            (username, limit)
        )
            
        results = cursor.fetchall()
        conn.close()
        
        return results