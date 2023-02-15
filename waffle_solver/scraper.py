import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import constants, utils


def get_waffle_word_game():
    """Parses the Waffle Daily Game page and creates and
        returns waffle word game matrix and right waffle word
        game matrix.

    Returns:
        Tuple of 2-D matrix. Waffle word game replicated and
            Waffle word game replicated with only the
             characters into the right positions.

    """
    print("\n\nFetching the game board...")
    service = Service(ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    browser = webdriver.Chrome(service=service, chrome_options=chrome_options)
    # Start the selenium driver to get the waffle word game.
    browser.get(constants.WAFFLE_DAILY_GAME_URL)

    # Parse to get board tiles from the Waffle word game.
    soup = BeautifulSoup(browser.page_source, "html.parser")
    waffle_board = soup.find("div", class_="board")
    waffle_tiles = waffle_board.find_all("div", class_="tile")

    # Create 2-D matrix once we have the tiles from the Waffle
    # word game.

    # 2D array with the waffle word game matrix.
    waffle_game_board = [[constants.EMPTY_WAFFLE_GAME_BOARD_CHARACTER for _ in range(5)] for _ in range(5)]
    # 2-D array with only characters in the right positions
    # on the waffle word game board.
    right_waffle_game_board = [[constants.EMPTY_WAFFLE_GAME_BOARD_CHARACTER for _ in range(5)] for _ in range(5)]

    for tile in waffle_tiles:
        character = tile.text
        character_position = json.loads(tile.attrs["data-pos"])
        row_index, column_index = character_position["y"], character_position["x"]
        character_class = tile.attrs["class"]
        waffle_game_board[row_index][column_index] = character
        if "green" not in character_class:
            continue
        # The character is in the right position if the tile is green on the
        # Waffle game board. Only append characters in this matrix,
        # if they are in the right position on Waffle word game board.
        right_waffle_game_board[row_index][column_index] = character

    # Quit the driver once we have loaded the program into memory.
    browser.quit()
    print("Done\n\n")
    print("DAILY WAFFLE BOARD\n")
    utils.display_waffle_game_board(waffle_game_board)
    print("\n\n")
    return waffle_game_board, right_waffle_game_board
