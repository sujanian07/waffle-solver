import itertools
from collections import Counter

import utils


def generate_words_combinations(
        waffle_game_board,
        right_waffle_game_board,
        possible_words_for_waffle_game_board
):
    # Get counters for all of the above strings.
    # Get product of all possible words that can be generated from the list of
    # possible words.
    print("Generating possible word combinations for Waffle board game...\n\n")
    all_character_count_for_waffle_board = utils.generate_minimum_maximum_strings_for_waffle_board(
        waffle_game_board,
        right_waffle_game_board
    )
    character_count_for_waffle_board = all_character_count_for_waffle_board[0]
    minimum_character_count_for_waffle_board = all_character_count_for_waffle_board[1]
    maximum_character_count_for_waffle_board = all_character_count_for_waffle_board[2]

    word_combinations_for_waffle_board = itertools.product(
        possible_words_for_waffle_game_board[0],
        possible_words_for_waffle_game_board[1],
        possible_words_for_waffle_game_board[2],
        possible_words_for_waffle_game_board[3],
        possible_words_for_waffle_game_board[4],
        possible_words_for_waffle_game_board[5]
    )
    # Store it in memory.
    word_combinations_for_waffle_board = list(set(word_combinations_for_waffle_board))
    possible_word_combinations_for_waffle_board = []

    for word_combination in word_combinations_for_waffle_board:
        # Each word combination should have 6 separate words if
        # not, continue to the next word combination.
        merged_word = "".join(word_combination)
        merged_word_character_count = Counter(merged_word)
        # All keys in the current words counter should be present in
        # waffle character string. ex.
        # If AB is a waffle string, ABC can't be the word that makes
        # the waffle array since C is extra and can't be accommodated
        # in the waffle solution.
        if merged_word_character_count.keys() != character_count_for_waffle_board.keys():
            continue

        # The count of characters in the waffle string (combinations of
        # all words) should be between minimum and maximum waffle character
        # that are in the waffle array. ex.
        # If the minimum/maximum number of H's in waffle array can be 2/4 and the current
        # word has 1 or 5 H's, current word can't constitute the waffle array, so we can
        # continue to the next word.
        break_out_flag = False
        for character, count in merged_word_character_count.items():
            # The merged word counter character count should be higher than
            # or equal to minimum character count for the Waffle game board.
            if not minimum_character_count_for_waffle_board.get(character, 0) <= count:
                break_out_flag = True
                break
            # The merged word counter character count should be lesser than
            # or equal to maximum character count for the Waffle game board.
            if not count <= maximum_character_count_for_waffle_board.get(character, 0):
                break_out_flag = True
                break

        # If the break-out flag is marked True in above conditions, continue from here.
        if break_out_flag:
            continue
        possible_word_combinations_for_waffle_board.append(word_combination)

    return possible_word_combinations_for_waffle_board
