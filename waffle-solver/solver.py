import copy
import itertools
import json

import enchant
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Get the en_US dictionary.
dictionary = enchant.Dict("en_US")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# The website we are trying to scrape.
waffle_daily_game = "https://wafflegame.net/"
driver.get(waffle_daily_game)

# Covert it to a html parsed document.
soup = BeautifulSoup(driver.page_source, "html.parser")

# Get the waffle board div from waffle_daily_game.
board_div = soup.find("div", class_="board")
# Get all the tiles from board_div of waffle_daily_game.
tiles = board_div.find_all("div", class_="tile")

# Create a 2D array and replicate the waffle game.
waffle_arr = [["_" for i in range(5)] for j in range(5)]
for tile in tiles:
    character = tile.text
    character_position = json.loads(tile.attrs["data-pos"])
    # This is the 2d array with waffle game.
    waffle_arr[character_position["y"]][character_position["x"]] = character

# This is the 2d array with characters that are in the right position.
right_waffle_arr = [["_" for i in range(5)] for j in range(5)]
for tile in tiles:
    character = tile.text
    character_position = json.loads(tile.attrs["data-pos"])
    character_class = tile.attrs["class"]
    if "green" in character_class:
        right_waffle_arr[character_position["y"]][character_position["x"]] = character

# Quit the driver once we have required details about the waffle daily game.
driver.quit()

print(waffle_arr)
print(right_waffle_arr)
titled_waffle_arr = list(zip(*waffle_arr))
titled_right_waffle_arr = list(zip(*right_waffle_arr))

waffle_characters = []
swappable_waffle_characters = []
for i in range(len(waffle_arr)):
    for j in range(len(waffle_arr[0])):
        waffle_characters.append(waffle_arr[i][j])
        if i == j:
            waffle_characters.append(waffle_arr[i][j])
        if waffle_arr[i][j] == right_waffle_arr[i][j]:
            continue
        swappable_waffle_characters.append(waffle_arr[i][j])

# Create a string for swappable characters.
swappable_characters_str = "".join(swappable_waffle_characters)
waffle_characters_str = "".join(waffle_characters)
waffle_characters_str = waffle_characters_str.replace("_", "")
permutations_of_waffle_arr = [
    "".join(character) for character in set(
        itertools.product(waffle_characters_str, repeat=len(waffle_arr))
    )
]

# Calculate for possible words that can come out from waffle array.
possible_words = []
for word in permutations_of_waffle_arr:
    if dictionary.check(word):
        possible_words.append(word)

# Create arrays of words to complete.
all_words_to_complete = [
    waffle_arr[0],
    waffle_arr[2],
    waffle_arr[4],
    titled_waffle_arr[0],
    titled_waffle_arr[2],
    titled_waffle_arr[4]
]

# Create array of words to complete, with only non-swappable
# characters.
all_words_to_complete_non_swappable = [
    right_waffle_arr[0],
    right_waffle_arr[2],
    right_waffle_arr[4],
    titled_right_waffle_arr[0],
    titled_right_waffle_arr[2],
    titled_right_waffle_arr[4]
]

# Eliminate words based on words in the right position. From the
# non-swappable characters.
possible_words_for_waffle = []
for word in all_words_to_complete:
    right_word = all_words_to_complete_non_swappable[all_words_to_complete.index(word)]
    word_idx_map = {}
    words_maybe = []
    for idx in range(len(word)):
        if word[idx] == right_word[idx]:
            word_idx_map[idx] = right_word[idx]

    possible_word_maybe = []
    for idx, w in word_idx_map.items():
        words_maybe = list(set(possible_words) & set(possible_word_maybe)) if possible_word_maybe else copy.deepcopy(
            possible_words)
        possible_word_maybe = []
        for pw in words_maybe:
            if pw[idx] == w:
                possible_word_maybe.append(pw)
    # for possible_word in possible_word_maybe:
    possible_words_for_waffle.append(possible_word_maybe)

all_characters_for_waffle = ""
min_waffle_character_possible_str = ""
max_waffle_character_possible_str = ""
for i in range(len(waffle_arr)):
    for j in range(len(waffle_arr[0])):
        if waffle_arr[i][j] == "_":
            continue
        all_characters_for_waffle += waffle_arr[i][j]
        if waffle_arr[i][j] == right_waffle_arr[i][j] and (i + j) % 2 != 0:
            min_waffle_character_possible_str += waffle_arr[i][j]
            max_waffle_character_possible_str += waffle_arr[i][j]
        elif waffle_arr[i][j] == right_waffle_arr[i][j] and (i + j) % 2 == 0:
            min_waffle_character_possible_str += (2 * waffle_arr[i][j])
            max_waffle_character_possible_str += (2 * waffle_arr[i][j])
        else:
            min_waffle_character_possible_str += waffle_arr[i][j]
            max_waffle_character_possible_str += (2 * waffle_arr[i][j])

all_characters_for_waffle = "".join(sorted(all_characters_for_waffle))
max_waffle_character_possible_str = "".join(sorted(max_waffle_character_possible_str))
min_waffle_character_possible_str = "".join(sorted(min_waffle_character_possible_str))

# Get product of all possible words that can be generated from the list of
# possible words.
product_of_possible_words_for_waffle = itertools.product(
    possible_words_for_waffle[0],
    possible_words_for_waffle[1],
    possible_words_for_waffle[2],
    possible_words_for_waffle[3],
    possible_words_for_waffle[4],
    possible_words_for_waffle[5]
)
# Store it in memory.
product_of_possible_words_for_waffle = list(set(product_of_possible_words_for_waffle))

possible_waffle_arrays = []
for word_tuple in product_of_possible_words_for_waffle:
    print(word_tuple)
    if len(word_tuple) != 6:
        continue
    new_arr = [["_" for i in range(5)] for j in range(5)]
    words_used = 0
    # Fill in the rows.
    for i in range(0, 5, 2):
        arr = word_tuple[words_used]
        for j in range(0, 5, 1):
            new_arr[i][j] = arr[j]
        words_used += 1

    # Fill in the columns.
    break_out_flag = False
    for i in range(0, 5, 2):
        arr = word_tuple[words_used]
        for j in range(0, 5, 1):
            if new_arr[j][i] != "_" and new_arr[j][i] != arr[j]:
                break_out_flag = True
                break
            new_arr[j][i] = arr[j]
        if break_out_flag:
            break
        words_used += 1
    # If all the words are not used and new_arr is already present
    # in possible waffle arrays continue from here.
    if words_used != 5 and new_arr in possible_waffle_arrays:
        continue
    possible_waffle_arrays.append(new_arr)


def is_possible_waffle_array(possible_array):
    # Get the empty count of tiles.
    empty_tile_count = 0
    for a in possible_array:
        empty_tile_count += a.count("_")
    if empty_tile_count > 4:
        return False

    possible_waffle_array_str = ""
    all_characters_for_waffle_array_str = ""
    for i in range(len(possible_array)):
        for j in range(len(possible_array[0])):
            if possible_array[i][j] == "_":
                continue
            if (i + j) % 2 == 0:
                all_characters_for_waffle_array_str += possible_array[i][j]
                possible_waffle_array_str += 2 * possible_array[i][j]
            else:
                all_characters_for_waffle_array_str += possible_array[i][j]
                possible_waffle_array_str += possible_array[i][j]

    is_possible = True
    for i in possible_waffle_array_str:
        if not all_characters_for_waffle.count(i) == all_characters_for_waffle_array_str.count(i):
            is_possible = False
        if min_waffle_character_possible_str.count(i) <= possible_waffle_array_str.count(i) \
                <= max_waffle_character_possible_str.count(i):
            continue
        else:
            is_possible = False

    return is_possible


final_waffle_arrays = []
for arr in possible_waffle_arrays:
    if not is_possible_waffle_array(arr):
        continue
    final_waffle_arrays.append(arr)

for waffle_array in final_waffle_arrays:
    import pprint
    pprint.pprint(waffle_array)
    print("\n\n\n")
