import cv2 as cv
import time
from image_processing import ImageProcessor
from game_logic import GameLogic
from user_interaction import UserInteraction
from user_interface import UserInterface

def main():
    # Initialize components
    image_processor = ImageProcessor()
    game_logic = GameLogic()
    ui = UserInterface()
    interaction = UserInteraction(
        window_name="Rock Paper Scissors Game",
        buttons=[],
        on_start=game_logic.start_game,
        on_stop=game_logic.stop_game,
        on_restart=game_logic.restart_game,
        on_close=lambda: setattr(main, "running", False)
    )

    # Setup window
    cv.namedWindow("Rock Paper Scissors Game", cv.WINDOW_NORMAL)
    cv.resizeWindow("Rock Paper Scissors Game", ui.screen_width, ui.screen_height)

    # Set mouse callback after window creation
    interaction.set_mouse_callback()

    # Setup buttons
    buttons = interaction.setup_buttons()

    # FPS control
    FPS = 30
    last_time = time.time()
    main.running = True

    while main.running:
        # Capture and process frame
        frame = image_processor.capture_frame()
        if frame is None:
            break

        results = image_processor.process_hands(frame)
        frame = image_processor.draw_landmarks(frame, results)

        # Update game state
        now = time.time()
        if now - last_time >= 1 / FPS:
            if game_logic.game_state == game_logic.GAME_STATES["RUNNING"] and not game_logic.match_ended:
                game_logic.clock = (game_logic.clock + 1) % 100
            last_time = now

        # Process player move
        success = False
        player_move = None
        if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 1:
            player_move = image_processor.get_hand_move(results.multi_hand_landmarks[0])
            success = True

        game_logic.update_game_state(game_logic.clock, player_move, success)

        # Render UI
        full_screen = ui.render(frame, game_logic.get_state(), buttons)
        cv.imshow("Rock Paper Scissors Game", full_screen)

        # Handle exit
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    image_processor.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()