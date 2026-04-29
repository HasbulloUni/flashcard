import sqlite3
import os
import logging
from typing import List, Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "flashcards.db")

def init_db() -> None:
    """Initializes the SQLite database with required tables."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Create decks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS decks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        
        # Create cards table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deck_id INTEGER,
                front TEXT NOT NULL,
                back TEXT NOT NULL,
                FOREIGN KEY (deck_id) REFERENCES decks (id) ON DELETE CASCADE
            )
        ''')
        
        # Create study_sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS study_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deck_id INTEGER,
                correct INTEGER,
                total INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (deck_id) REFERENCES decks (id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error initializing database: {e}")

def get_decks() -> List[Tuple[int, str]]:
    """Retrieves all decks from the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM decks")
        decks = cursor.fetchall()
        conn.close()
        return decks
    except sqlite3.Error as e:
        logger.error(f"Error fetching decks: {e}")
        return []

def add_deck(name: str) -> bool:
    """Adds a new deck to the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO decks (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        logger.info(f"Deck added: {name}")
        return True
    except sqlite3.IntegrityError:
        logger.warning(f"Failed to add deck (already exists): {name}")
        return False
    except sqlite3.Error as e:
        logger.error(f"Error adding deck: {e}")
        return False

def rename_deck(deck_id: int, new_name: str) -> bool:
    """Renames an existing deck."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE decks SET name = ? WHERE id = ?", (new_name, deck_id))
        conn.commit()
        conn.close()
        logger.info(f"Deck {deck_id} renamed to {new_name}")
        return True
    except sqlite3.IntegrityError:
        logger.warning(f"Failed to rename deck: Name '{new_name}' already exists.")
        return False
    except sqlite3.Error as e:
        logger.error(f"Error renaming deck: {e}")
        return False

def delete_deck(deck_id: int) -> None:
    """Deletes a deck and all its associated cards."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("DELETE FROM decks WHERE id = ?", (deck_id,))
        conn.commit()
        conn.close()
        logger.info(f"Deck {deck_id} deleted.")
    except sqlite3.Error as e:
        logger.error(f"Error deleting deck: {e}")

def get_cards(deck_id: int) -> List[Tuple[int, str, str]]:
    """Retrieves all cards for a specific deck."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, front, back FROM cards WHERE deck_id = ?", (deck_id,))
        cards = cursor.fetchall()
        conn.close()
        return cards
    except sqlite3.Error as e:
        logger.error(f"Error fetching cards for deck {deck_id}: {e}")
        return []

def add_card(deck_id: int, front: str, back: str) -> None:
    """Adds a new card to a specific deck."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cards (deck_id, front, back) VALUES (?, ?, ?)", (deck_id, front, back))
        conn.commit()
        conn.close()
        logger.debug(f"Card added to deck {deck_id}")
    except sqlite3.Error as e:
        logger.error(f"Error adding card: {e}")

def update_card(card_id: int, front: str, back: str) -> None:
    """Updates the content of an existing card."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE cards SET front = ?, back = ? WHERE id = ?", (front, back, card_id))
        conn.commit()
        conn.close()
        logger.info(f"Card {card_id} updated.")
    except sqlite3.Error as e:
        logger.error(f"Error updating card: {e}")

def delete_card(card_id: int) -> None:
    """Deletes a specific card."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cards WHERE id = ?", (card_id,))
        conn.commit()
        conn.close()
        logger.info(f"Card {card_id} deleted.")
    except sqlite3.Error as e:
        logger.error(f"Error deleting card: {e}")

def save_session(deck_id: int, correct: int, total: int) -> None:
    """Saves the result of a study session."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO study_sessions (deck_id, correct, total) VALUES (?, ?, ?)", (deck_id, correct, total))
        conn.commit()
        conn.close()
        logger.info(f"Session saved for deck {deck_id}: {correct}/{total}")
    except sqlite3.Error as e:
        logger.error(f"Error saving session: {e}")

def get_stats(deck_id: Optional[int] = None) -> List[Tuple[int, int, str]]:
    """Retrieves study statistics globally or for a specific deck."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        if deck_id:
            cursor.execute("SELECT correct, total, timestamp FROM study_sessions WHERE deck_id = ? ORDER BY timestamp", (deck_id,))
        else:
            cursor.execute("SELECT correct, total, timestamp FROM study_sessions ORDER BY timestamp")
        stats = cursor.fetchall()
        conn.close()
        return stats
    except sqlite3.Error as e:
        logger.error(f"Error fetching stats: {e}")
        return []

def get_card_count(deck_id: int) -> int:
    """Returns the number of cards in a specific deck."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cards WHERE deck_id = ?", (deck_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except sqlite3.Error as e:
        logger.error(f"Error getting card count: {e}")
        return 0
