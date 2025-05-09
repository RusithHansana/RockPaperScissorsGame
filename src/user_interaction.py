import cv2 as cv

class UserInteraction:
    def __init__(self, window_name, buttons, on_start, on_stop, on_restart, on_close):
        self.window_name = window_name
        self.buttons = buttons
        self.on_start = on_start
        self.on_stop = on_stop
        self.on_restart = on_restart
        self.on_close = on_close

    def set_mouse_callback(self):
        """Set the mouse callback for the window."""
        cv.setMouseCallback(self.window_name, self.mouse_callback)

    def mouse_callback(self, event, x, y, flags, param):
        """Handle mouse click events."""
        if event == cv.EVENT_LBUTTONDOWN:
            for btn in self.buttons:
                bx, by, bw, bh = btn["rect"]
                if bx < x < bx + bw and by < y < by + bh:
                    btn["callback"]()

    def setup_buttons(self):
        """Configure buttons with callbacks."""
        self.buttons = [
            {
                "name": "Start",
                "rect": (0, 0, 120, 40),
                "color": (76, 175, 80),
                "callback": self.on_start
            },
            {
                "name": "Stop",
                "rect": (0, 0, 120, 40),
                "color": (63, 81, 181),
                "callback": self.on_stop
            },
            {
                "name": "Reset",
                "rect": (0, 0, 120, 40),
                "color": (255, 152, 0),
                "callback": self.on_restart
            },
            {
                "name": "Close",
                "rect": (0, 0, 120, 40),
                "color": (244, 67, 54),
                "callback": self.on_close
            }
        ]
        return self.buttons