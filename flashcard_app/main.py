import customtkinter as ctk
import logging
from typing import Optional
from database import init_db
from ui.home import HomeFrame
from ui.editor import EditorFrame
from ui.study import StudyFrame
from ui.stats import StatsFrame
import assets.theme as theme

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FlashcardApp(ctk.CTk):
    """
    Main Application class for Flashcard Generator.
    Handles navigation between different frames.
    """
    def __init__(self):
        super().__init__()

        self.title("Flashcard Generator")
        self.geometry("1000x700")
        
        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize Database
        init_db()

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.current_frame: Optional[ctk.CTkFrame] = None
        self.show_home()
        logger.info("Application started.")

    def clear_frame(self) -> None:
        """Destroys the current frame if it exists."""
        if self.current_frame is not None:
            self.current_frame.destroy()

    def show_home(self) -> None:
        """Displays the Home screen."""
        self.clear_frame()
        self.current_frame = HomeFrame(self)
        self.current_frame.grid(row=0, column=0, sticky="nsew")
        logger.debug("Switched to Home screen.")

    def show_editor(self, deck_id: Optional[int] = None, deck_name: Optional[str] = None) -> None:
        """Displays the Editor screen for a specific deck."""
        self.clear_frame()
        self.current_frame = EditorFrame(self, deck_id, deck_name)
        self.current_frame.grid(row=0, column=0, sticky="nsew")
        logger.debug(f"Switched to Editor screen for deck: {deck_name}")

    def show_study(self, deck_id: int, deck_name: str) -> None:
        """Displays the Study screen for a specific deck."""
        self.clear_frame()
        self.current_frame = StudyFrame(self, deck_id, deck_name)
        self.current_frame.grid(row=0, column=0, sticky="nsew")
        logger.debug(f"Switched to Study screen for deck: {deck_name}")

    def show_stats(self, deck_id: Optional[int] = None) -> None:
        """Displays the Statistics screen."""
        self.clear_frame()
        self.current_frame = StatsFrame(self, deck_id)
        self.current_frame.grid(row=0, column=0, sticky="nsew")
        logger.debug("Switched to Stats screen.")

if __name__ == "__main__":
    try:
        app = FlashcardApp()
        app.mainloop()
    except KeyboardInterrupt:
        logger.info("Application closed by user.")
        print("\nApplicazione chiusa dall'utente.")
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}", exc_info=True)
