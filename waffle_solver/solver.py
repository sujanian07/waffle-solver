import warnings

import constants
import scraper
import utils
import word_combinations_generator
import word_generator

# Ignoring warnings from the NLTK package.
warnings.filterwarnings("ignore")

# Get complete waffle game board and right waffle game board from the
# scaper.
waffle_game_board, right_waffle_game_board = scraper.get_waffle_word_game()
print("Wait for it, starting to solve Waffle for you!!!\n")

possible_words_for_waffle_game_board = word_generator.get_words_for_waffle_game_board(
    waffle_game_board,
    right_waffle_game_board
)

possible_word_combinations_for_waffle_board = word_combinations_generator.generate_words_combinations(
    waffle_game_board,
    right_waffle_game_board,
    possible_words_for_waffle_game_board
)

all_character_count_for_waffle_board = utils.generate_minimum_maximum_strings_for_waffle_board(
        waffle_game_board,
        right_waffle_game_board
    )
character_count_for_waffle_board = all_character_count_for_waffle_board[0]
minimum_character_count_for_waffle_board = all_character_count_for_waffle_board[1]
maximum_character_count_for_waffle_board = all_character_count_for_waffle_board[2]


def generate_solution_waffle_game_boards():
    print("Generating solution Waffle game boards for you...\n\n")
    waffle_game_board_solutions = []
    for word_combination in possible_word_combinations_for_waffle_board:
        solution_board = [[constants.EMPTY_WAFFLE_GAME_BOARD_CHARACTER for _ in range(5)] for _ in range(5)]
        words_used = 0
        # Populate the rows of waffle game board.
        for row in range(0, 5, 2):
            current_word = word_combination[words_used]
            for column in range(0, 5, 1):
                solution_board[row][column] = current_word[column]
            words_used += 1

        # Populate the columns of waffle game board.
        break_out_flag = False
        for column in range(0, 5, 2):
            current_word = word_combination[words_used]
            for row in range(0, 5, 1):
                if solution_board[row][column] != constants.EMPTY_WAFFLE_GAME_BOARD_CHARACTER and solution_board[row][column] != current_word[row]:
                    break_out_flag = True
                    break
                solution_board[row][column] = current_word[row]
            if break_out_flag:
                break
            words_used += 1
        # If all the words are not used and new_arr is already present
        # in possible waffle arrays continue from here.
        if words_used != 5 and solution_board in waffle_game_board_solutions:
            continue
        waffle_game_board_solutions.append(solution_board)
    return waffle_game_board_solutions


def is_valid_waffle_board_solution(solution_bard):
    # Get the empty count of tiles.
    if utils.get_empty_tile_count_for_waffle_board(solution_bard) > 4:
        return False

    character_counts_for_solution_board = utils.generate_waffle_board_solution_character_count(solution_bard)
    character_count_for_solution_board = character_counts_for_solution_board[0]
    min_max_character_for_solution_board = character_counts_for_solution_board[1]

    is_valid = True
    for character in character_count_for_solution_board:
        if not character_count_for_waffle_board[character] == character_count_for_solution_board[character]:
            is_valid = False
            break
        if not minimum_character_count_for_waffle_board[character] <= min_max_character_for_solution_board[character]:
            is_valid = False
            break
        if not min_max_character_for_solution_board[character] <= maximum_character_count_for_waffle_board[character]:
            is_valid = False
            break
    return is_valid


final_waffle_game_solution_boards = []
print("Checking validity for each solution waffle board...\n\n")
waffle_game_solution_boards = generate_solution_waffle_game_boards()
for waffle_game_solution_board in waffle_game_solution_boards:
    if not is_valid_waffle_board_solution(waffle_game_solution_board):
        continue
    final_waffle_game_solution_boards.append(waffle_game_solution_board)


print("DAILY WAFFLE GAME SOLUTIONS:\n\n")
for final_waffle_game_solution_board in final_waffle_game_solution_boards:
    utils.display_waffle_game_board(final_waffle_game_solution_board)
    print("\n\n")
