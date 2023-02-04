from cmath import inf
import json
import random
import time
from bot import bot

starting_word = "react"
config = json.load(open("config.json"))

def main():
    global config
    
    starting_word = config["startingWord"]

    # Get the words
    words_list = get_words()

    # Prompt the user to play
    print("Welcome to Wordle Bot!")
    print("~" * 29)
    print("Current Starting Word: " + starting_word)
    print("~" * 29)
    print("Here are your options:")
    user_response = input("1. Custom word\n2. Random word\n3. All words\n4. Change starting word\n5. Compare two words\n6. Find best starting word (will take several hours)\n7. Exit\n>  ")

    # Remove spaces from user input to help with user error
    user_response = user_response.replace(" ", "")


    # User wants to use a custom word
    if (user_response == "1"):
        config["printGuesses"] = True
        actual_word = custom_word()

    # Random word
    elif (user_response == "2"):
        config["printGuesses"] = True
        actual_word = pick_random_word(words_list)

    # Run the bot on all words
    elif (user_response == "3"):
        all_words(words_list)
        play_again()
        return

    # Change the starting word
    elif (user_response == "4"):
        change_starting_word()
        return

    # Compare two words
    elif user_response == "5":
        compare_two_words(words_list)
        return

    # Find the best starting word
    elif user_response == "6":
        config["printStats"] = False
        config["printGuesses"] = False

        print(get_best_starting_word(words_list))
        return


    # User wants to exit
    elif (user_response == "7"):
        print("Goodbye!")
        exit()

    else:
        print("Invalid input. Please try again.")
        main()
        return

    # Run the bot
    bot(starting_word, words_list, actual_word, config)

    # Ask the user if they want to play again
    play_again()


def play_again():
    play_again = input("Would you like to play again? (y/n) ")

    if (play_again == "y"):
        main()
    else:
        print("Goodbye!")
        exit()

# User wants to change the starting word
def change_starting_word():
    global starting_word
    starting_word = input("Enter a 5 letter word: ")

    # Remove spaces
    starting_word = starting_word.replace(" ", "").lower()

    # Check if word is valid (Needs to be exactly 5 letters)
    if (len(starting_word) != 5):
        print("Invalid word. Please try again.")
        change_starting_word()
    
    else: 
        config["startingWord"] = starting_word

        print("Starting word changed to " + starting_word + ".\n")
        with open("config.json", "w") as f:
            json.dump(config, f)
        main()


# Run the bot on all words
def all_words(words):
    global config
    start_time = time.time()

    guess_count = []
    for i in range(len(words)):
        count = bot(starting_word, words, words[i], config)
        guess_count.append(count)

    return get_stats(guess_count, start_time)


# Get the stats of the bot
def get_stats(guess_count, start_time):
    global config

    max_guesses = 0
    min_guesses = 1
    avg_guesses = 0

    for i in range(len(guess_count)):
        if (guess_count[i] > max_guesses):
            max_guesses = guess_count[i]

        if (guess_count[i] < min_guesses):
            min_guesses = guess_count[i]

        avg_guesses += guess_count[i]

    avg_guesses = avg_guesses / len(guess_count)

    end_time = time.time()

    if config["printStats"]:
        print("~" * 29)
        print("Max guesses: " + str(max_guesses))
        print("Min guesses: " + str(min_guesses))
        print("Avg guesses: " + str(round(avg_guesses, 2)))
        print("Time taken: " + str(round(end_time - start_time, 2)) + " seconds")
        print("~" * 29)

    return ["%.2f" % round(avg_guesses, 2), "%.2f" % round(max_guesses, 2)]


# User says use a custom word
def custom_word():
    word = input("Enter a 5 letter word: ")

    # Remove spaces
    word = word.replace(" ", "").lower()

    # Check if word is valid (Needs to be exactly 5 letters)
    if (len(word) != 5):
        print("Invalid word. Please try again.")
        return custom_word()

    else:
        return word


def compare_two_words(words):
    global starting_word

    print()

    word_1 = input("Enter the first word: ")
    word_2 = input("Enter the second word: ")

    # Remove spaces
    word_1 = word_1.replace(" ", "").lower()
    word_2 = word_2.replace(" ", "").lower()

    # Check if word is valid (Needs to be exactly 5 letters)
    if (len(word_1) != 5 or len(word_2) != 5):
        print("Invalid word. Please try again.")
        return compare_two_words()

    else:
        config["printStats"] = False
        config["printGuesses"] = False

        print()
        print("Testing word 1... " + word_1)
        starting_word = word_1
        count = all_words(words)
        [avg_guesses_1, max_guesses_1] = count

        print("Testing word 2... " + word_2)
        starting_word = word_2
        count_2 = all_words(words)
        [avg_guesses_2, max_guesses_2] = count_2
        
        print()
        print("~" * 53)
        print("Word 1: " + word_1 + " | Avg guesses: " + str(avg_guesses_1) + " | Max guesses: " + str(max_guesses_1))
        print("Word 2: " + word_2 + " | Avg guesses: " + str(avg_guesses_2) + " | Max guesses: " + str(max_guesses_2))
        print("~" * 53)


def get_best_starting_word(words):
    global starting_word

    start_time = time.time()

    best_word_avg = ""
    best_avg = inf

    worst_avg = 0
    worst_word_avg = ""

    best_max = inf
    best_word_max = ""

    worst_max = 0
    worst_word_max = ""

    for i in range(len(words)):
        print("Testing " + words[i])
        starting_word = words[i]

        [avg, max_guesses] = all_words(words)

        avg = float(avg)
        max_guesses = float(max_guesses)

        if avg < best_avg:
            best_avg = avg
            best_word_avg = words[i]

        elif avg > worst_avg:
            worst_avg = avg
            worst_word_avg = words[i]

        if max_guesses < best_max:
            best_max = max_guesses
            best_word_max = words[i]

        elif max_guesses > worst_max:
            worst_max = max_guesses
            worst_word_max = words[i]

    
    end_time = time.time()
    
    print("~" * 50)
    print("Best starting word for avg: " + best_word_avg + " with an average of " + str(best_avg))
    print("Worst starting word for avg: " + worst_word_avg + " with an average of " + str(worst_avg))
    print("~" * 50)
    print("Best starting word for max: " + best_word_max + " with a max of " + str(best_max))
    print("Worst starting word for max: " + worst_word_max + " with a max of " + str(worst_max))
    print("~" * 50)
    print("Time taken: " + str(end_time - start_time) + " seconds")
    print("Average time per word: " + str((end_time - start_time) / len(words)) + " seconds")
    print("~" * 50)

    
# Put all the words in a list
def get_words():
    words = []
    with open("words.txt", "r") as f:
        for line in f:
            line = line.strip()
            words.append(line)

    return words
    

def pick_random_word(words):
    return random.choice(words)


if __name__ == '__main__':
    main()