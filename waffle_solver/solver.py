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

possible_words_for_waffle_game_board = word_generator.get_possible_words(
    waffle_game_board,
    right_waffle_game_board
)

# Generate possible 6 word combinations for Waffle game board.
possible_word_combinations_for_waffle_game_board = word_combinations_generator.generate_words_combinations(
    waffle_game_board,
    right_waffle_game_board,
    possible_words_for_waffle_game_board
)

# Generate characters count for the Waffle game board.
all_character_count_for_waffle_game_board = utils.generate_minimum_maximum_strings_for_waffle_board(
        waffle_game_board,
        right_waffle_game_board
    )
character_count_for_waffle_game_board = all_character_count_for_waffle_game_board[0]
minimum_character_count_for_waffle_game_board = all_character_count_for_waffle_game_board[1]
maximum_character_count_for_waffle_game_board = all_character_count_for_waffle_game_board[2]


def generate_solution_waffle_game_boards():
    """Generate as many solutions for Waffle game board by creating
        waffle game boards with the word combinations.

    Note:
        The generated solution boards might not be final and have to
            be checked for validity once done.

    """
    print("Generating solution Waffle game boards for you...\n\n")
    waffle_game_board_solutions = []

    for word_combination in possible_word_combinations_for_waffle_game_board:
        # Create an empty solution board.
        solution_board = [[constants.EMPTY_WAFFLE_GAME_BOARD_CHARACTER for _ in range(5)] for _ in range(5)]
        # Keep track of total words used in the solution board.
        words_used = 1
        # Populate the rows of waffle game board.
        for row in range(0, 5, 2):
            current_word = word_combination[words_used - 1]
            for column in range(0, 5, 1):
                solution_board[row][column] = current_word[column]
            words_used += 1

        # Populate the columns of waffle game board.
        # Break out flag if the words are not compatible on
        # the solution Waffle board.
        break_out_flag = False
        for column in range(0, 5, 2):
            current_word = word_combination[words_used - 1]
            for row in range(0, 5, 1):
                # If the current position is not empty, and the current character is not equal
                # to the character already on the current position, the solution is invalid.
                if (solution_board[row][column] != constants.EMPTY_WAFFLE_GAME_BOARD_CHARACTER and
                        solution_board[row][column] != current_word[row]):
                    break_out_flag = True
                    break
                solution_board[row][column] = current_word[row]
            if break_out_flag:
                break
            words_used += 1

        # The total words used should be equal to 6, since the Waffle board solution
        # always has 6 words on it.
        if words_used != 6 and solution_board in waffle_game_board_solutions:
            continue
        waffle_game_board_solutions.append(solution_board)

    return waffle_game_board_solutions


def is_valid_waffle_board_solution(solution_bard):
    """Check validity of a solution Waffle game board generated.

    Note:
        The generated solution board is generated using the possible
            word combinations we generated above.

    """
    # If the count of empty tile is more than 4, the solution board
    # is invalid.
    if utils.get_empty_tile_count_for_waffle_board(solution_bard) > 4:
        return False

    character_counts_for_solution_board = utils.generate_waffle_board_solution_character_count(solution_bard)
    # Get minimum and maximum characters and character count for solution board.
    character_count_for_solution_board = character_counts_for_solution_board[0]
    maximum_character_count_for_solution_board = character_counts_for_solution_board[1]

    is_valid = True
    for character in character_count_for_solution_board:
        # If the current character count on the solution board doesn't match the
        # waffle game board character count, the solution is invalid.
        if not character_count_for_waffle_game_board[character] == character_count_for_solution_board[character]:
            is_valid = False
            break
        # The current character count on the solution board should be higher than
        # the minimum characters possible and less than the maximum characters
        # possible on Waffle game board. If any of these conditions
        # is not satisfied, the solution board is invalid.
        if not (minimum_character_count_for_waffle_game_board[character]
                <= maximum_character_count_for_solution_board[character]):
            is_valid = False
            break
        if not (maximum_character_count_for_solution_board[character]
                <= maximum_character_count_for_waffle_game_board[character]):
            is_valid = False
            break
    return is_valid


final_waffle_game_solution_boards = []
print("Checking validity for each solution waffle board...\n\n")

# Generate the solutions Waffle game boards.
waffle_game_solution_boards = generate_solution_waffle_game_boards()

for waffle_game_solution_board in waffle_game_solution_boards:
    if not is_valid_waffle_board_solution(waffle_game_solution_board):
        continue
    # Create final solution boards, after check the validity for
    # each solution board generated.
    final_waffle_game_solution_boards.append(waffle_game_solution_board)


# Return the final Waffle game solution board.
print("DAILY WAFFLE GAME SOLUTIONS:\n\n")
for final_waffle_game_solution_board in final_waffle_game_solution_boards:
    utils.display_waffle_game_board(final_waffle_game_solution_board)
    print("\n\n")
