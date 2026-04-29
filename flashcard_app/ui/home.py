import customtkinter as ctk
import logging
from typing import List, Tuple, Optional
import database as db
import assets.theme as theme

logger = logging.getLogger(__name__)

class HomeFrame(ctk.CTkFrame):
    """
    Frame responsible for displaying the list of decks and global actions.
    """
    def __init__(self, master: ctk.CTk):
        super().__init__(master, fg_color=theme.COLORS["bg_dark"])
        self.master = master
        
        # Title
        self.title_label = ctk.CTkLabel(self, text="Flashcard Generator", font=theme.FONTS["header"], text_color=theme.COLORS["text"])
        self.title_label.pack(pady=30)
        
        # Action Buttons
        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_frame.pack(pady=10)

        self.new_deck_btn = ctk.CTkButton(self.actions_frame, text="+ Create New Deck", font=theme.FONTS["body"], 
                                         fg_color=theme.COLORS["success"], hover_color="#218838",
                                         command=self.create_deck_dialog)
        self.new_deck_btn.pack(side="left", padx=10)
        
        self.global_stats_btn = ctk.CTkButton(self.actions_frame, text="Global Statistics", font=theme.FONTS["body"],
                                             command=self.master.show_stats)
        self.global_stats_btn.pack(side="left", padx=10)

        # Decks List Title
        self.list_label = ctk.CTkLabel(self, text="Your Decks", font=theme.FONTS["subheader"], text_color=theme.COLORS["text_secondary"])
        self.list_label.pack(pady=(20, 5))

        # Decks List
        self.decks_frame = ctk.CTkScrollableFrame(self, fg_color=theme.COLORS["bg_medium"], width=850, height=400)
        self.decks_frame.pack(pady=10, padx=50, fill="both", expand=True)
        
        self.load_decks()

    def load_decks(self) -> None:
        """Loads and displays all decks from the database."""
        # Clear current decks
        for widget in self.decks_frame.winfo_children():
            widget.destroy()
            
        decks: List[Tuple[int, str]] = db.get_decks()
        if not decks:
            empty_label = ctk.CTkLabel(self.decks_frame, text="No decks yet. Create one to get started!", font=theme.FONTS["body"], text_color=theme.COLORS["text_secondary"])
            empty_label.pack(pady=50)
            return

        for deck_id, name in decks:
            card_count = db.get_card_count(deck_id)
            self.create_deck_item(deck_id, name, card_count)

    def create_deck_item(self, deck_id: int, name: str, card_count: int) -> None:
        """Creates a UI component for a single deck."""
        item_frame = ctk.CTkFrame(self.decks_frame, fg_color=theme.COLORS["bg_light"])
        item_frame.pack(pady=5, padx=10, fill="x")
        
        label = ctk.CTkLabel(item_frame, text=f"{name} ({card_count} cards)", font=theme.FONTS["body"], text_color=theme.COLORS["text"])
        label.pack(side="left", padx=20, pady=15)
        
        # Buttons container
        btns_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        btns_frame.pack(side="right", padx=10)
        
        study_btn = ctk.CTkButton(btns_frame, text="Study", width=70, height=30, command=lambda d=deck_id, n=name: self.master.show_study(d, n))
        study_btn.pack(side="left", padx=2)
        
        edit_btn = ctk.CTkButton(btns_frame, text="Edit", width=70, height=30, fg_color=theme.COLORS["accent"], command=lambda d=deck_id, n=name: self.master.show_editor(d, n))
        edit_btn.pack(side="left", padx=2)
        
        stats_btn = ctk.CTkButton(btns_frame, text="Stats", width=70, height=30, fg_color=theme.COLORS["bg_medium"], command=lambda d=deck_id: self.master.show_stats(d))
        stats_btn.pack(side="left", padx=2)
        
        rename_btn = ctk.CTkButton(btns_frame, text="Rename", width=70, height=30, fg_color=theme.COLORS["warning"], text_color="#000000", command=lambda d=deck_id, n=name: self.rename_deck_dialog(d, n))
        rename_btn.pack(side="left", padx=2)
        
        delete_btn = ctk.CTkButton(btns_frame, text="Delete", width=70, height=30, fg_color=theme.COLORS["error"], hover_color="#c82333", command=lambda d=deck_id: self.delete_deck(d))
        delete_btn.pack(side="left", padx=2)

    def create_deck_dialog(self) -> None:
        """Shows a dialog to create a new deck with input validation."""
        dialog = ctk.CTkInputDialog(text="Enter Deck Name:", title="New Deck")
        name = dialog.get_input()
        if name:
            name = name.strip()
            if not name:
                self.show_error("Deck name cannot be empty.")
                return
            if db.add_deck(name):
                self.load_decks()
            else:
                self.show_error("Deck name already exists.")

    def rename_deck_dialog(self, deck_id: int, current_name: str) -> None:
        """Shows a dialog to rename an existing deck with validation."""
        dialog = ctk.CTkInputDialog(text=f"Rename '{current_name}' to:", title="Rename Deck")
        new_name = dialog.get_input()
        if new_name:
            new_name = new_name.strip()
            if not new_name:
                self.show_error("Deck name cannot be empty.")
                return
            if new_name != current_name:
                if db.rename_deck(deck_id, new_name):
                    self.load_decks()
                else:
                    self.show_error("Deck name already exists.")

    def delete_deck(self, deck_id: int) -> None:
        """Shows a confirmation dialog before deleting a deck."""
        confirm = ctk.CTkInputDialog(text="Type 'DELETE' to confirm:", title="Confirm Delete")
        user_input = confirm.get_input()
        if user_input and user_input.upper() == "DELETE":
            db.delete_deck(deck_id)
            self.load_decks()
            logger.info(f"Deck {deck_id} deleted by user.")

    def show_error(self, message: str) -> None:
        """Displays an error message in a new top-level window."""
        error_dialog = ctk.CTkToplevel(self)
        error_dialog.title("Error")
        error_dialog.geometry("400x150")
        label = ctk.CTkLabel(error_dialog, text=message, text_color=theme.COLORS["error"], font=theme.FONTS["body"], wraplength=350)
        label.pack(pady=30)
        btn = ctk.CTkButton(error_dialog, text="OK", command=error_dialog.destroy)
        btn.pack()
        error_dialog.attributes("-topmost", True)
        logger.warning(f"Error dialog shown: {message}")
