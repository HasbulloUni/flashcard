from PIL import Image, ImageDraw, ImageFont
import os

def export_card_to_image(front, back, filename):
    # Create a 800x500 image with dark background
    width, height = 800, 500
    bg_color = (45, 45, 45) # theme.COLORS["bg_medium"] approx
    accent_color = (31, 106, 165) # theme.COLORS["accent"]
    text_color = (255, 255, 255)
    secondary_text_color = (170, 170, 170)
    
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw border
    draw.rectangle([20, 20, width-20, height-20], outline=accent_color, width=10)
    
    # Try to load a nice font
    try:
        # Common linux font paths
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
            "arial.ttf"
        ]
        font_main = None
        for path in font_paths:
            if os.path.exists(path):
                font_main = ImageFont.truetype(path, 40)
                font_sub = ImageFont.truetype(path, 25)
                break
        if not font_main:
            font_main = ImageFont.load_default()
            font_sub = ImageFont.load_default()
    except:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        
    # Draw "Question" label
    draw.text((width/2, 100), "QUESTION", fill=secondary_text_color, font=font_sub, anchor="mm")
    
    # Draw Front Text (handling wrapping manually or just centering)
    # Simple wrap: split by length
    def wrap_text(text, max_chars=40):
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            if len(" ".join(current_line + [word])) <= max_chars:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
        lines.append(" ".join(current_line))
        return lines

    front_lines = wrap_text(front)
    y_start = 160
    for line in front_lines:
        draw.text((width/2, y_start), line, fill=text_color, font=font_main, anchor="mm")
        y_start += 50

    # Draw separator line
    draw.line([100, 300, 700, 300], fill=accent_color, width=2)

    # Draw "Answer" label
    draw.text((width/2, 340), "ANSWER", fill=secondary_text_color, font=font_sub, anchor="mm")

    # Draw Back Text
    back_lines = wrap_text(back)
    y_start = 400
    for line in back_lines:
        draw.text((width/2, y_start), line, fill=text_color, font=font_main, anchor="mm")
        y_start += 50
    
    try:
        img.save(filename)
        return True
    except Exception as e:
        print(f"Image Export Error: {e}")
        return False
