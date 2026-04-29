"""
Centralized theme configuration for the Flashcard Generator.
Includes color palettes and font settings.
"""
from typing import Dict, Tuple, Union

COLORS: Dict[str, str] = {
    "bg_dark": "#1a1a1a",
    "bg_medium": "#2d2d2d",
    "bg_light": "#3d3d3d",
    "accent": "#1f6aa5",
    "accent_hover": "#144e75",
    "text": "#ffffff",
    "text_secondary": "#aaaaaa",
    "success": "#28a745",
    "error": "#dc3545",
    "warning": "#ffc107"
}

# Tuple for font settings: (Font Family, Size, Style)
FONTS: Dict[str, Tuple[str, int, str]] = {
    "header": ("Helvetica", 24, "bold"),
    "subheader": ("Helvetica", 18, "bold"),
    "body": ("Helvetica", 14, "normal"),
    "card_text": ("Helvetica", 20, "normal")
}
