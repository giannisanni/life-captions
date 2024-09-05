from config import STORY_MODES
import logging

logger = logging.getLogger(__name__)

def select_template():
    while True:
        print("\nAvailable story modes:")
        for i, mode in enumerate(STORY_MODES, 1):
            print(f"{i}. {mode.replace('_', ' ').title()}")
        choice = input("Choose a story mode (enter the number): ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(STORY_MODES):
                selected_mode = STORY_MODES[index]
                logger.info(f"Story mode selected: {selected_mode}")
                return selected_mode
            else:
                logger.warning("Invalid story mode choice")
                print("Invalid choice. Please try again.")
        except ValueError:
            logger.warning("Invalid input for story mode selection")
            print("Please enter a number.")
def select_dnd_option():
    while True:
        choice = input("Choose an option (A, B, C, or D): ").upper()
        if choice in ['A', 'B', 'C', 'D']:
            logger.info(f"D&D option selected: {choice}")
            return choice
        else:
            logger.warning("Invalid D&D option choice")
            print("Invalid choice. Please enter A, B, C, or D.")
