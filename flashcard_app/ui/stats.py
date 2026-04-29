import customtkinter as ctk
import logging
from typing import Optional, List, Tuple
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import database as db
import assets.theme as theme

logger = logging.getLogger(__name__)

class StatsFrame(ctk.CTkFrame):
    """
    Frame for visualizing study statistics using Matplotlib.
    Displays a bar chart of session performance.
    """
    def __init__(self, master: ctk.CTk, deck_id: Optional[int] = None):
        super().__init__(master, fg_color=theme.COLORS["bg_dark"])
        self.master = master
        self.deck_id = deck_id
        
        # Navigation
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.pack(fill="x", pady=10, padx=20)
        
        self.back_btn = ctk.CTkButton(self.nav_frame, text="< Back", width=80, command=self.master.show_home)
        self.back_btn.pack(side="left")
        
        title = "Global Statistics"
        if deck_id:
            decks = db.get_decks()
            deck_name = next((d[1] for d in decks if d[0] == deck_id), "Deck")
            title = f"Statistics: {deck_name}"

        self.title_label = ctk.CTkLabel(self.nav_frame, text=title, font=theme.FONTS["header"])
        self.title_label.pack(side="left", padx=20)
        
        self.stats: List[Tuple[int, int, str]] = db.get_stats(deck_id)
        
        if not self.stats:
            self.show_empty()
        else:
            self.show_charts()

    def show_empty(self) -> None:
        """Displays a message when no stats are available."""
        label = ctk.CTkLabel(self, text="No study sessions recorded yet.", font=theme.FONTS["subheader"])
        label.pack(pady=100)

    def show_charts(self) -> None:
        """Generates and embeds the Matplotlib chart."""
        # Prepare data
        percentages = [(s[0] / s[1] * 100) if s[1] > 0 else 0 for s in self.stats]
        x_data = list(range(1, len(self.stats) + 1))
        
        # Create Figure
        fig = Figure(figsize=(8, 4), dpi=100, facecolor=theme.COLORS["bg_dark"])
        ax = fig.add_subplot(111)
        ax.set_facecolor(theme.COLORS["bg_medium"])
        
        # Use Bar chart
        ax.bar(x_data, percentages, color=theme.COLORS["accent"], alpha=0.8)
        
        ax.set_ylim(0, 105)
        ax.set_title("Performance per Session (%)", color=theme.COLORS["text"], pad=20)
        ax.set_xlabel("Session Number", color=theme.COLORS["text"])
        ax.set_ylabel("Percentage", color=theme.COLORS["text"])
        
        # Styling axes
        ax.spines['bottom'].set_color(theme.COLORS["text_secondary"])
        ax.spines['top'].set_color(theme.COLORS["text_secondary"])
        ax.spines['right'].set_color(theme.COLORS["text_secondary"])
        ax.spines['left'].set_color(theme.COLORS["text_secondary"])
        ax.tick_params(colors=theme.COLORS["text_secondary"])
        ax.grid(True, linestyle='--', alpha=0.3, color=theme.COLORS["text_secondary"])
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(pady=20, padx=50, fill="both", expand=True)
        canvas.draw()
        
        # Summary Labels
        avg_score = sum(percentages) / len(percentages)
        summary_frame = ctk.CTkFrame(self, fg_color="transparent")
        summary_frame.pack(pady=20)
        
        ctk.CTkLabel(summary_frame, text=f"Total Sessions: {len(self.stats)}", font=theme.FONTS["body"]).pack(side="left", padx=20)
        ctk.CTkLabel(summary_frame, text=f"Average Score: {avg_score:.1f}%", font=theme.FONTS["body"], text_color=theme.COLORS["accent"]).pack(side="left", padx=20)
        logger.debug("Statistics chart rendered.")
