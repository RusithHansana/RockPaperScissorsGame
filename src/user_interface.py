import cv2 as cv
import numpy as np
from math import cos, sin, pi

class UserInterface:
    def __init__(self, screen_width=1280, screen_height=720, video_width=640, video_height=480):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.video_width = video_width
        self.video_height = video_height
        self.padding = 40
        self.title_bg = (30, 30, 30)
        self.bg_color = (240, 240, 240)
        self.panel_color = (255, 255, 255)
        self.text_color = (50, 50, 50)
        self.accent_color = (102, 204, 153)
        self.font_scale = 0.7

    def draw_rounded_rect(self, img, top_left, bottom_right, color, thickness=2, r=15):
        """Draw a rounded rectangle."""
        x1, y1 = top_left
        x2, y2 = bottom_right
        if thickness < 0:
            overlay = img.copy()
            cv.rectangle(overlay, (x1 + r, y1), (x2 - r, y2), color, thickness)
            cv.rectangle(overlay, (x1, y1 + r), (x2, y2 - r), color, thickness)
            for pt in [(x1 + r, y1 + r), (x2 - r, y1 + r), (x1 + r, y2 - r), (x2 - r, y2 - r)]:
                cv.circle(overlay, pt, r, color, thickness)
            cv.addWeighted(overlay, 0.6, img, 0.4, 0, img)
        else:
            cv.rectangle(img, (x1 + r, y1), (x2 - r, y2), color, thickness)
            cv.rectangle(img, (x1, y1 + r), (x2, y2 - r), color, thickness)
            for pt in [(x1 + r, y1 + r), (x2 - r, y1 + r), (x1 + r, y2 - r), (x2 - r, y2 - r)]:
                cv.ellipse(img, pt, (r, r), 90, 0, 90, color, thickness)

    def apply_glass_effect(self, img, top_left, bottom_right, blur_kernel=(21, 21), alpha=0.5):
        """Apply a frosted glass effect to a region."""
        x1, y1 = top_left
        x2, y2 = bottom_right
        roi = img[y1:y2, x1:x2]
        blurred = cv.GaussianBlur(roi, blur_kernel, 0)
        glassy_roi = cv.addWeighted(blurred, alpha, roi, 1 - alpha, 0)
        img[y1:y2, x1:x2] = glassy_roi

    def draw_circular_progress(self, img, center, radius, progress, color):
        """Draw a circular progress bar."""
        thickness = 10
        for i in range(360):
            angle = i * pi / 180
            x = int(center[0] + radius * cos(angle))
            y = int(center[1] + radius * sin(angle))
            if i <= progress * 360:
                cv.circle(img, (x, y), thickness // 2, color, -1)

    def render(self, frame, game_state, buttons):
        """Render the entire UI."""
        full_screen = np.ones((self.screen_height, self.screen_width, 3), dtype=np.uint8) * 255

        # Title bar
        title_bar_height = 60
        cv.rectangle(full_screen, (0, 0), (self.screen_width, title_bar_height), self.title_bg, -1)
        cv.putText(full_screen, "Rock Paper Scissors - Best of 3", (20, 40),
                   cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv.putText(full_screen, f"You: {game_state['player_score']} - Computer: {game_state['computer_score']}",
                   (self.screen_width - 300, 40), cv.FONT_HERSHEY_SIMPLEX, 0.8, self.accent_color, 2)

        # Video feed
        full_screen[title_bar_height + self.padding: title_bar_height + self.padding + self.video_height,
                    self.padding: self.padding + self.video_width] = frame
        self.apply_glass_effect(full_screen,
                               (self.padding, title_bar_height + self.padding),
                               (self.padding + self.video_width, title_bar_height + self.padding + self.video_height))

        # Game info panel
        info_x = self.padding + self.video_width + self.padding
        info_y = title_bar_height + self.padding
        info_w = self.screen_width - info_x - self.padding
        info_h = self.video_height
        self.apply_glass_effect(full_screen, (info_x, info_y), (self.screen_width - self.padding, info_y + info_h))

        # Section title
        section_y = info_y + 30
        cv.putText(full_screen, "GAME INFORMATION", (info_x + 20, section_y),
                   cv.FONT_HERSHEY_SIMPLEX, 0.7, (80, 80, 80), 1)
        cv.line(full_screen, (info_x + 20, section_y + 15), (self.screen_width - self.padding - 20, section_y + 15),
                (200, 200, 200), 1)

        # Computer move
        comp_box_y = section_y + 40
        cv.putText(full_screen, "Computer Move:", (info_x + 20, comp_box_y),
                   cv.FONT_HERSHEY_SIMPLEX, 0.7, (60, 60, 60), 2)
        if game_state['computer_move']:
            move_text = game_state['computer_move'].upper()
            move_box_x = info_x + 200
            move_box_y = comp_box_y - 25
            self.draw_rounded_rect(full_screen,
                                   (move_box_x, move_box_y),
                                   (move_box_x + 120, move_box_y + 35),
                                   (30, 30, 30), thickness=cv.FILLED, r=10)
            cv.putText(full_screen, move_text, (move_box_x + 15, comp_box_y),
                       cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        else:
            cv.putText(full_screen, "Waiting...", (info_x + 200, comp_box_y),
                       cv.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 2)

        # Timer
        timer_y = comp_box_y + 60
        cv.putText(full_screen, "Timer:", (info_x + 20, timer_y),
                   cv.FONT_HERSHEY_SIMPLEX, 0.7, (60, 60, 60), 2)
        timer_progress = game_state['clock'] / 100
        self.draw_circular_progress(full_screen, (info_x + 200, timer_y - 10), 30, timer_progress, self.accent_color)
        cv.putText(full_screen, f"{game_state['clock']}", (info_x + 190, timer_y + 5),
                   cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

        # Game status
        status_y = timer_y + 80
        cv.putText(full_screen, "Status:", (info_x + 20, status_y),
                   cv.FONT_HERSHEY_SIMPLEX, 0.7, (60, 60, 60), 2)
        status_box_x = info_x + 120
        status_box_y = status_y - 25
        status_box_width = info_w - 120
        status_box_height = 100

        # Get status text, with fallback
        game_text = game_state['game_text'] if game_state['game_text'] else "Waiting for game to start..."

        # Determine status box color based on content
        if "You win" in game_text.lower():
            status_color = (25, 100, 25)  # Green for win
        elif "Computer wins" in game_text.lower():
            status_color = (100, 25, 25)  # Red for loss
        elif "Draw" in game_text.lower():
            status_color = (80, 80, 80)  # Gray for draw
        else:
            status_color = (200, 200, 200)  # Slightly darker neutral for better contrast

        # Draw status box
        self.draw_rounded_rect(full_screen,
                               (status_box_x, status_box_y),
                               (status_box_x + status_box_width, status_box_y + status_box_height),
                               status_color, thickness=cv.FILLED, r=10)

        # Format status text with icons and line breaks
        lines = []
        if "Round" in game_text and "Get Ready" in game_text:
            countdown = max(0, 20 - game_state['clock'])
            lines.append(f"Round {game_state['round_number']} of 3")
            lines.append(f"Get Ready! ({countdown}s)")
        elif "You win" in game_text.lower():
            lines.append("✅ You Win!")
            lines.append(game_text.split("|")[-1].strip())
        elif "Computer wins" in game_text.lower():
            lines.append("❌ Computer Wins!")
            lines.append(game_text.split("|")[-1].strip())
        elif "Draw" in game_text.lower():
            lines.append("↔ Draw!")
            lines.append(game_text.split("|")[-1].strip())
        else:
            # Split long text into chunks of ~30 characters
            words = game_text.split()
            current_line = ""
            for word in words:
                if len(current_line) + len(word) + 1 <= 30:
                    current_line += word + " "
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                lines.append(current_line.strip())

        # Draw status text
        text_y_pos = status_box_y + 25
        for line in lines:
            cv.putText(full_screen, line, (status_box_x + 10, text_y_pos),
                       cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)  # Black text
            text_y_pos += 25

        # Match result overlay
        if game_state['match_ended']:
            overlay_x = self.screen_width // 4
            overlay_y = self.screen_height // 3
            overlay_w = self.screen_width // 2
            overlay_h = self.screen_height // 3
            self.apply_glass_effect(full_screen, (overlay_x, overlay_y), (overlay_x + overlay_w, overlay_y + overlay_h))
            self.draw_rounded_rect(full_screen,
                                   (overlay_x, overlay_y),
                                   (overlay_x + overlay_w, overlay_y + overlay_h),
                                   (50, 50, 50) if "Computer" in game_text else (25, 100, 25),
                                   thickness=cv.FILLED, r=15)
            cv.putText(full_screen, game_text, (overlay_x + 20, overlay_y + 50),
                       cv.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
            cv.putText(full_screen, "Click Reset to Play Again!", (overlay_x + 20, overlay_y + 100),
                       cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Buttons
        button_width = 120
        button_height = 40
        button_spacing = 20
        total_buttons_width = (button_width * 4) + (button_spacing * 3)
        start_x = (self.screen_width - total_buttons_width) // 2
        for i, btn in enumerate(buttons):
            btn["rect"] = (start_x + i * (button_width + button_spacing), 640, button_width, button_height)
            bx, by, bw, bh = btn["rect"]
            self.draw_rounded_rect(full_screen, (bx, by), (bx + bw, by + bh), btn["color"], thickness=cv.FILLED, r=10)
            cv.putText(full_screen, btn["name"], (bx + 10, by + 25),
                       cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        return full_screen