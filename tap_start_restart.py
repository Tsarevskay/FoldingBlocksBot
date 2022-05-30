import easyocr
import pyautogui
import os


def tap_start_game(region: tuple[int, int, int, int]) -> bool:
    """
    Presses the button on the screen to start the game and start the next level.
    Args:
        region: Coordinates for the screenshot of the screen.

    Returns:
        True if the buttons are found, False otherwise.
    """
    screen_start = pyautogui.screenshot(os.path.join('../images', 'screenshot.png'), region=region)
    img_path = '../images/screenshot.png'
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img_path)
    if result:
        text = str(result[0][1]).lower()
        if (text.startswith('tap')) or (text.startswith('con')):
            pyautogui.click(x=832, y=789)
            return True
    else:
        return False
