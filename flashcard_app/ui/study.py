import customtkinter as ctk
import logging
from typing import List, Tuple
import database as db
import assets.theme as theme
import random

logger = logging.getLogger(__name__)

class StudyFrame(ctk.CTkFrame):
    """
    Frame for the interactive study mode.
    Handles card flipping, scoring, and session tracking.
    """
    def __init__(self, master: ctk.CTk, deck_id: int, deck_name: str):
        super().__init__(master, fg_color=theme.COLORS["bg_dark"])
        self.master = master
        self.deck_id = deck_id
        self.deck_name = deck_name
        
        self.cards: List[Tuple[int, str, str]] = db.get_cards(deck_id)
        
        # Initial Selection View
        self.show_order_selection()

    def show_order_selection(self) -> None:
        """Displays options to start the session in random or sequential order."""
        self.selection_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.selection_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(self.selection_frame, text=f"Deck: {self.deck_name}", font=theme.FONTS["header"]).pack(pady=20)
        ctk.CTkLabel(self.selection_frame, text="Choose study order:", font=theme.FONTS["body"]).pack(pady=10)
        
        ctk.CTkButton(self.selection_frame, text="Sequential Order", command=lambda: self.start_study(False)).pack(pady=10)
        ctk.CTkButton(self.selection_frame, text="Random Order", command=lambda: self.start_study(True)).pack(pady=10)
        ctk.CTkButton(self.selection_frame, text="Cancel", fg_color=theme.COLORS["bg_medium"], command=self.master.show_home).pack(pady=10)

    def start_study(self, shuffle: bool) -> None:
        """Initializes the study session variables and UI."""
        if shuffle:
            random.shuffle(self.cards)
            logger.info(f"Study session started (Random) for deck {self.deck_id}.")
        else:
            logger.info(f"Study session started (Sequential) for deck {self.deck_id}.")
            
        self.selection_frame.destroy()
        
        self.current_index = 0
        self.correct_count = 0
        self.is_flipped = False
        
        self.setup_study_ui()

    def setup_study_ui(self) -> None:
        """Initializes the quiz UI elements."""
        # Navigation
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.pack(fill="x", pady=10, padx=20)
        
        self.back_btn = ctk.CTkButton(self.nav_frame, text="< Exit", width=80, command=self.master.show_home)
        self.back_btn.pack(side="left")
        
        self.title_label = ctk.CTkLabel(self.nav_frame, text=f"Studying: {self.deck_name}", font=theme.FONTS["header"])
        self.title_label.pack(side="left", padx=20)
        
        if not self.cards:
            self.show_empty()
            return
            
        # Progress
        self.progress_label = ctk.CTkLabel(self, text=f"Card 1 of {len(self.cards)}", font=theme.FONTS["body"])
        self.progress_label.pack(pady=10)
        
        # Card Container
        self.card_container = ctk.CTkFrame(self, fg_color="transparent")
        self.card_container.pack(pady=20, padx=50, fill="both", expand=True)

        # Card Frame
        self.card_frame = ctk.CTkFrame(self.card_container, fg_color=theme.COLORS["bg_medium"], corner_radius=15)
        self.card_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)
        
        self.card_text = ctk.CTkLabel(self.card_frame, text="", font=theme.FONTS["card_text"], wraplength=600)
        self.card_text.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Flip Hint
        self.hint_label = ctk.CTkLabel(self, text="Click card to flip", font=theme.FONTS["body"], text_color=theme.COLORS["text_secondary"])
        self.hint_label.pack()
        
        # Bindings for flipping
        self.card_frame.bind("<Button-1>", lambda e: self.flip_card())
        self.card_text.bind("<Button-1>", lambda e: self.flip_card())
        
        # Controls
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.pack(pady=30)
        
        self.wrong_btn = ctk.CTkButton(self.controls_frame, text="❌ Don't Know", fg_color=theme.COLORS["error"], 
                                      hover_color="#c82333", height=40, font=theme.FONTS["body"], command=self.mark_wrong)
        self.wrong_btn.pack(side="left", padx=20)
        
        self.correct_btn = ctk.CTkButton(self.controls_frame, text="✅ Know", fg_color=theme.COLORS["success"], 
                                        hover_color="#218838", height=40, font=theme.FONTS["body"], command=self.mark_correct)
        self.correct_btn.pack(side="left", padx=20)
        
        self.update_card()

    def show_empty(self) -> None:
        """Handles cases where a deck has no cards to study."""
        label = ctk.CTkLabel(self, text="No cards in this deck to study!", font=theme.FONTS["subheader"])
        label.pack(pady=100)
        btn = ctk.CTkButton(self, text="Go to Editor", command=lambda: self.master.show_editor(self.deck_id, self.deck_name))
        btn.pack()

    def update_card(self) -> None:
        """Updates the card display with the current question."""
        self.is_flipped = False
        card = self.cards[self.current_index]
        self.card_text.configure(text=card[1]) # Front
        self.progress_label.configure(text=f"Card {self.current_index + 1} of {len(self.cards)}")
        self.hint_label.configure(text="Click card to flip")
        self.card_frame.configure(fg_color=theme.COLORS["bg_medium"])

    def flip_card(self) -> None:
        """Flips the card to show the answer or question."""
        self.is_flipped = not self.is_flipped
        card = self.cards[self.current_index]
        if self.is_flipped:
            self.card_text.configure(text=card[2]) # Back
            self.hint_label.configure(text="Showing Answer")
            self.card_frame.configure(fg_color=theme.COLORS["bg_light"])
        else:
            self.card_text.configure(text=card[1]) # Front
            self.hint_label.configure(text="Showing Question")
            self.card_frame.configure(fg_color=theme.COLORS["bg_medium"])

    def mark_correct(self) -> None:
        """Records a correct answer and moves to the next card."""
        self.correct_count += 1
        self.next_card()

    def mark_wrong(self) -> None:
        """Records an incorrect answer and moves to the next card."""
        self.next_card()

    def next_card(self) -> None:
        """Moves to the next card in the deck or shows results if finished."""
        self.current_index += 1
        if self.current_index < len(self.cards):
            self.update_card()
        else:
            self.show_results()

    def show_results(self) -> None:
        """Saves session results and displays a summary screen."""
        db.save_session(self.deck_id, self.correct_count, len(self.cards))
        
        # Clear frame
        for widget in self.winfo_children():
            widget.destroy()
            
        # Results View
        ctk.CTkLabel(self, text="Session Complete!", font=theme.FONTS["header"]).pack(pady=50)
        ctk.CTkLabel(self, text=f"Score: {self.correct_count} / {len(self.cards)}", font=theme.FONTS["subheader"]).pack(pady=10)
        
        percentage = (self.correct_count / len(self.cards)) * 100 if len(self.cards) > 0 else 0
        ctk.CTkLabel(self, text=f"{percentage:.1f}%", font=("Helvetica", 64, "bold"), text_color=theme.COLORS["accent"]).pack(pady=20)
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=50)
        
        ctk.CTkButton(btn_frame, text="Study Again", command=lambda: self.master.show_study(self.deck_id, self.deck_name)).pack(side="left", padx=20)
        ctk.CTkButton(btn_frame, text="Finish", command=self.master.show_home).pack(side="left", padx=20)
        logger.info(f"Study session finished. Score: {self.correct_count}/{len(self.cards)}")
