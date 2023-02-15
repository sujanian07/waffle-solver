import copy
import itertools

import enchant
import nltk
from nltk.corpus import words

import constants

# Get all nltk valid words.
nltk.download("words", quiet=True)
nltk_valid_words = set(words.words())

# Get the en_US dictionary from pyenchant.
dictionary = enchant.Dict("en_US")


def get_possible_words(waffle_game_board, right_waffle_game_board):
    """Returns possible words that can be used to complete the Waffle game board.

    Returns:
        List[List[str]]. The resultant array will consist of list of words
            for each row and column of Waffle game board, words indexed as following:
            0,0 -> 4,0
            0,0 -> 0,4
            2,0 -> 2,4
            0,2 -> 4,2
            4,0 -> 4,4
            0,4 -> 4,4

    """
    print("Generating possible words that can be on the Waffle game board...\n\n")
    waffle_board_characters = ""
    for i in range(len(waffle_game_board)):
        for j in range(len(waffle_game_board[0])):
            if waffle_game_board[i][j] == constants.EMPTY_WAFFLE_GAME_BOARD_CHARACTER:
                continue
            elif i == j:
                waffle_board_characters += 2 * waffle_game_board[i][j]
            else:
                waffle_board_characters += waffle_game_board[i][j]

    permutations_of_waffle_board_characters = [
        "".join(character) for character in set(
            itertools.product(waffle_board_characters, repeat=len(waffle_game_board))
        )
    ]

    # Calculate for possible words that can come out from Waffle game
    # board characters.
    words_for_waffle_game_board = []
    for word in permutations_of_waffle_board_characters:
        if dictionary.check(word):
            words_for_waffle_game_board.append(word)
        if word.lower() in nltk_valid_words:
            words_for_waffle_game_board.append(word)

    # Exchange row with columns and get all the words we have
    # complete to solve Waffle board game.
    swapped_waffle_game_board = list(zip(*waffle_game_board))
    swapped_right_waffle_game_board = list(zip(*right_waffle_game_board))
    # Array of words to complete, with swappable
    # characters only.
    swappable_words_on_waffle_board = [
        waffle_game_board[0],
        waffle_game_board[2],
        waffle_game_board[4],
        swapped_waffle_game_board[0],
        swapped_waffle_game_board[2],
        swapped_waffle_game_board[4]
    ]
    # Array of words to complete, with right/unswappable
    # characters only.
    unswappable_words_on_waffle_board = [
        right_waffle_game_board[0],
        right_waffle_game_board[2],
        right_waffle_game_board[4],
        swapped_right_waffle_game_board[0],
        swapped_right_waffle_game_board[2],
        swapped_right_waffle_game_board[4]
    ]

    words_for_waffle_based_on_position = []
    # Eliminate words that can be filled on the board, based on characters
    # in the right/unswappable position on the right Waffle game board.
    for current_position_swappable in swappable_words_on_waffle_board:
        # Get the right word against the word we have to complete/fill on
        # the Waffle game board.
        current_position_unswappable_word = unswappable_words_on_waffle_board[
            swappable_words_on_waffle_board.index(current_position_swappable)
        ]
        # Create a map of unswappable character on right waffle game board, to the
        # index of the right character.
        character_on_unswappable_index_map = {}
        for position in range(len(current_position_swappable)):
            if current_position_swappable[position] != current_position_unswappable_word[position]:
                continue
            # If the current word's character is right/unswappable, add it
            # to the dictionary at the current index.
            character_on_unswappable_index_map[position] = current_position_unswappable_word[position]

        # Narrow down possible words this word can become on the Waffle game board, and
        # append it to the array.
        possible_words_for_position_on_waffle_board = []
        # For index of right/unswappable character on the Waffle game board
        # and character, check which of the possible list of all words
        # can are eligible for the current position.
        for index, character in character_on_unswappable_index_map.items():
            # Update the right words for current position based on the
            # unswappable character position on the Waffle game board.
            right_words_for_current_position = list(
                set(words_for_waffle_game_board)
                & set(possible_words_for_position_on_waffle_board)
            ) if possible_words_for_position_on_waffle_board else copy.deepcopy(words_for_waffle_game_board)
            possible_words_for_position_on_waffle_board = []
            # For each word in current word, if the right/unswappable character, is
            # not present at the same position as in the right Waffle game board, the word
            # can't be the right word for current position on the Waffle game  board.
            for current_position_word in right_words_for_current_position:
                if current_position_word[index] != character:
                    continue
                possible_words_for_position_on_waffle_board.append(current_position_word)

        # Append possible words for the current position of Waffle game board.
        words_for_waffle_based_on_position.append(possible_words_for_position_on_waffle_board)

    # Return all possible words. The resultant array would be of an array of arrays
    # and will contain row and column words respectively for the Waffle game board.
    return words_for_waffle_based_on_position
