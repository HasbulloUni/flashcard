import customtkinter as ctk
import logging
from typing import List, Tuple, Optional
from tkinter import filedialog, messagebox
import database as db
import assets.theme as theme
from export.pdf_exporter import export_to_pdf
from export.image_exporter import export_card_to_image

logger = logging.getLogger(__name__)

class EditorFrame(ctk.CTkFrame):
    """
    Frame for managing cards within a specific deck.
    Supports adding, editing, deleting cards and exporting the deck.
    """
    def __init__(self, master: ctk.CTk, deck_id: Optional[int], deck_name: Optional[str]):
        super().__init__(master, fg_color=theme.COLORS["bg_dark"])
        self.master = master
        self.deck_id = deck_id
        self.deck_name = deck_name
        self.edit_card_id: Optional[int] = None
        
        if self.deck_id is None:
            self.show_not_selected()
            return

        self.setup_ui()
        self.load_cards()

    def show_not_selected(self) -> None:
        """Handles cases where no deck is correctly passed to the editor."""
        label = ctk.CTkLabel(self, text="No deck selected", font=theme.FONTS["header"])
        label.pack(pady=50)
        btn = ctk.CTkButton(self, text="Back Home", command=self.master.show_home)
        btn.pack()

    def setup_ui(self) -> None:
        """Initializes the UI layout for the editor."""
        # Navigation
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.pack(fill="x", pady=10, padx=20)
        
        self.back_btn = ctk.CTkButton(self.nav_frame, text="< Back", width=80, command=self.master.show_home)
        self.back_btn.pack(side="left")
        
        self.title_label = ctk.CTkLabel(self.nav_frame, text=f"Editing Deck: {self.deck_name}", font=theme.FONTS["header"], text_color=theme.COLORS["text"])
        self.title_label.pack(side="left", padx=20)

        self.export_pdf_btn = ctk.CTkButton(self.nav_frame, text="Export PDF", fg_color=theme.COLORS["accent"], 
                                           command=self.export_deck_pdf)
        self.export_pdf_btn.pack(side="right", padx=10)
        
        # Add/Edit Card Form
        self.form_frame = ctk.CTkFrame(self, fg_color=theme.COLORS["bg_medium"])
        self.form_frame.pack(pady=10, padx=50, fill="x")
        
        self.form_title = ctk.CTkLabel(self.form_frame, text="Add New Card", font=theme.FONTS["body"], text_color=theme.COLORS["accent"])
        self.form_title.grid(row=0, column=0, columnspan=2, pady=(10, 0))

        self.front_label = ctk.CTkLabel(self.form_frame, text="Front (Question):", font=theme.FONTS["body"])
        self.front_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.front_entry = ctk.CTkEntry(self.form_frame, width=500)
        self.front_entry.grid(row=1, column=1, padx=20, pady=10)
        
        self.back_label = ctk.CTkLabel(self.form_frame, text="Back (Answer):", font=theme.FONTS["body"])
        self.back_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.back_entry = ctk.CTkEntry(self.form_frame, width=500)
        self.back_entry.grid(row=2, column=1, padx=20, pady=10)
        
        self.submit_btn = ctk.CTkButton(self.form_frame, text="Add Card", fg_color=theme.COLORS["success"], 
                                    hover_color="#218838", command=self.save_card)
        self.submit_btn.grid(row=3, column=1, padx=20, pady=20, sticky="e")
        
        self.cancel_edit_btn = ctk.CTkButton(self.form_frame, text="Cancel Edit", fg_color=theme.COLORS["bg_light"], 
                                            command=self.reset_form)
        
        # Bind Return key to save_card
        self.front_entry.bind("<Return>", lambda e: self.save_card())
        self.back_entry.bind("<Return>", lambda e: self.save_card())
        
        # Cards List Section
        self.list_section = ctk.CTkFrame(self, fg_color="transparent")
        self.list_section.pack(fill="both", expand=True, padx=50, pady=(10, 20))

        self.cards_list_label = ctk.CTkLabel(self.list_section, text="Cards List", font=theme.FONTS["subheader"], text_color=theme.COLORS["text_secondary"])
        self.cards_list_label.pack(pady=(0, 5), anchor="w")
        
        self.cards_frame = ctk.CTkScrollableFrame(self.list_section, fg_color=theme.COLORS["bg_medium"])
        self.cards_frame.pack(fill="both", expand=True)

    def load_cards(self) -> None:
        """Loads and displays all cards for the current deck."""
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
            
        cards = db.get_cards(self.deck_id)
        if not cards:
            empty_label = ctk.CTkLabel(self.cards_frame, text="No cards in this deck.", font=theme.FONTS["body"], text_color=theme.COLORS["text_secondary"])
            empty_label.pack(pady=20)
            return

        for card_id, front, back in cards:
            self.create_card_item(card_id, front, back)

    def create_card_item(self, card_id: int, front: str, back: str) -> None:
        """Creates a UI component for a single card."""
        item_frame = ctk.CTkFrame(self.cards_frame, fg_color=theme.COLORS["bg_light"])
        item_frame.pack(pady=2, padx=10, fill="x")
        
        text_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True, padx=10, pady=5)
        
        f_label = ctk.CTkLabel(text_frame, text=f"Q: {front}", font=theme.FONTS["body"], anchor="w", wraplength=450)
        f_label.pack(fill="x")
        b_label = ctk.CTkLabel(text_frame, text=f"A: {back}", font=theme.FONTS["body"], text_color=theme.COLORS["text_secondary"], anchor="w", wraplength=450)
        b_label.pack(fill="x")
        
        btns_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        btns_frame.pack(side="right", padx=10)

        edit_btn = ctk.CTkButton(btns_frame, text="Edit", width=40, fg_color=theme.COLORS["warning"], text_color="#000000",
                                command=lambda c=card_id, f=front, b=back: self.prepare_edit(c, f, b))
        edit_btn.pack(side="left", padx=5)

        img_btn = ctk.CTkButton(btns_frame, text="PNG", width=40, fg_color=theme.COLORS["accent"], 
                               command=lambda f=front, b=back: self.export_card_png(f, b))
        img_btn.pack(side="left", padx=5)

        delete_btn = ctk.CTkButton(btns_frame, text="X", width=30, fg_color=theme.COLORS["error"], 
                                  hover_color="#c82333", command=lambda c=card_id: self.delete_card(c))
        delete_btn.pack(side="left", padx=5)

    def save_card(self) -> None:
        """Saves a new card or updates an existing one with validation."""
        front = self.front_entry.get().strip()
        back = self.back_entry.get().strip()
        
        if not front or not back:
            messagebox.showwarning("Validation Error", "Both Front and Back fields are required.")
            logger.warning("Attempted to save card with empty fields.")
            return

        if self.edit_card_id:
            db.update_card(self.edit_card_id, front, back)
            logger.info(f"Card {self.edit_card_id} updated.")
        else:
            db.add_card(self.deck_id, front, back)
            logger.info(f"New card added to deck {self.deck_id}.")
            
        self.reset_form()
        self.load_cards()

    def prepare_edit(self, card_id: int, front: str, back: str) -> None:
        """Populates the form with card data for editing."""
        self.edit_card_id = card_id
        self.front_entry.delete(0, 'end')
        self.front_entry.insert(0, front)
        self.back_entry.delete(0, 'end')
        self.back_entry.insert(0, back)
        
        self.form_title.configure(text="Edit Card", text_color=theme.COLORS["warning"])
        self.submit_btn.configure(text="Update Card", fg_color=theme.COLORS["warning"], text_color="#000000")
        self.cancel_edit_btn.grid(row=3, column=0, padx=20, pady=20, sticky="w")
        logger.debug(f"Form prepared for editing card {card_id}.")

    def reset_form(self) -> None:
        """Resets the input form to 'Add' mode."""
        self.edit_card_id = None
        self.front_entry.delete(0, 'end')
        self.back_entry.delete(0, 'end')
        self.form_title.configure(text="Add New Card", text_color=theme.COLORS["accent"])
        self.submit_btn.configure(text="Add Card", fg_color=theme.COLORS["success"], text_color="#ffffff")
        self.cancel_edit_btn.grid_forget()
        self.master.focus() # Reset focus from entries
        logger.debug("Form reset.")

    def delete_card(self, card_id: int) -> None:
        """Deletes a card from the deck."""
        db.delete_card(card_id)
        self.load_cards()
        logger.info(f"Card {card_id} deleted.")

    def export_deck_pdf(self) -> None:
        """Triggers the PDF export for the current deck."""
        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=f"{self.deck_name}.pdf")
        if filename:
            if export_to_pdf(self.deck_id, self.deck_name, filename):
                messagebox.showinfo("Success", f"Deck exported to {filename}")
                logger.info(f"Deck {self.deck_id} exported to PDF: {filename}")
            else:
                messagebox.showerror("Error", "Failed to export PDF")
                logger.error(f"Failed to export PDF for deck {self.deck_id}.")

    def export_card_png(self, front: str, back: str) -> None:
        """Triggers the PNG export for a single card."""
        safe_front = "".join([c for c in front[:20] if c.isalnum() or c==' ']).rstrip()
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")], initialfile=f"{safe_front}.png")
        if filename:
            if export_card_to_image(front, back, filename):
                messagebox.showinfo("Success", f"Card exported to {filename}")
                logger.info(f"Card exported to PNG: {filename}")
            else:
                messagebox.showerror("Error", "Failed to export image")
                logger.error("Failed to export image.")
