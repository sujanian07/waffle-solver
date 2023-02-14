from collections import Counter

import constants


def generate_minimum_maximum_strings_for_waffle_board(waffle_game_board, right_waffle_game_board):

    waffle_board_characters = ""
    minimum_waffle_board_characters = ""
    maximum_waffle_board_characters = ""

    row_count = len(waffle_game_board)
    column_count = len(waffle_game_board[0])
    for row_index in range(row_count):
        for column_index in range(column_count):
            if waffle_game_board[row_index][column_index] == constants.EMPTY_WAFFLE_GAME_BOARD_CHARACTER:
                continue
            waffle_board_characters += waffle_game_board[row_index][column_index]
            if waffle_game_board[row_index][column_index] == right_waffle_game_board[row_index][column_index]:
                if (row_index + column_index) % 2 != 0:
                    minimum_waffle_board_characters += waffle_game_board[row_index][column_index]
                    maximum_waffle_board_characters += waffle_game_board[row_index][column_index]
                else:
                    minimum_waffle_board_characters += (2 * waffle_game_board[row_index][column_index])
                    maximum_waffle_board_characters += (2 * waffle_game_board[row_index][column_index])
            else:
                minimum_waffle_board_characters += waffle_game_board[row_index][column_index]
                maximum_waffle_board_characters += (2 * waffle_game_board[row_index][column_index])

    character_count_for_waffle_board = Counter(waffle_board_characters)
    minimum_character_count_for_waffle_board = Counter(minimum_waffle_board_characters)
    maximum_character_count_for_waffle_board = Counter(maximum_waffle_board_characters)

    return (
        character_count_for_waffle_board,
        minimum_character_count_for_waffle_board,
        maximum_character_count_for_waffle_board
    )


def generate_waffle_board_solution_character_count(solution_board):
    characters_for_solution_board = ""
    min_max_characters_for_solution_board = ""
    rows = len(solution_board)
    columns = len(solution_board[0])
    for row in range(rows):
        for column in range(columns):
            if solution_board[row][column] == constants.EMPTY_WAFFLE_GAME_BOARD_CHARACTER:
                continue
            if (row + column) % 2 == 0:
                characters_for_solution_board += solution_board[row][column]
                min_max_characters_for_solution_board += 2 * solution_board[row][column]
            else:
                characters_for_solution_board += solution_board[row][column]
                min_max_characters_for_solution_board += solution_board[row][column]

    character_count_for_solution_board = Counter(characters_for_solution_board)
    min_max_character_for_solution_board = Counter(min_max_characters_for_solution_board)
    return character_count_for_solution_board, min_max_character_for_solution_board


def get_empty_tile_count_for_waffle_board(waffle_board):
    empty_tile_count = 0
    for waffle_word in waffle_board:
        empty_tile_count += waffle_word.count(constants.EMPTY_WAFFLE_GAME_BOARD_CHARACTER)
    return empty_tile_count
