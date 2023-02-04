
guess_count = 0
remaining_words = []
stats = {
    "correct": ['', '', '', '', ''],
    "wrong_spot": [[], [], [], [], []],
    "incorrect": []
}


def bot(starting_word, words_list, actual_word, config):
    global guess_count
    global remaining_words
    global stats

    # Reset stats
    stats = {
        "correct": ['', '', '', '', ''],
        "wrong_spot": [[], [], [], [], []],
        "incorrect": []
    }

    # Reset remaining words
    remaining_words = words_list

    # Reset guess count
    guess_count = 0

    # Here are the basic steps I want
    # 1. Go through each word in the words.txt file
    # 2. Make the starting guess
    # 3. Check the stats of the guess
    # 4. If all the letters are correct, then the word is correct
    # 5. If not, remove the un matching words from the list
    # 6. The new guess should be the most common letter in the remaining words
    # 7. Repeat until the word is correct

    # Make the first guess
    check_word(starting_word, actual_word)

    remaining_words = get_remaining_words(stats)
    next_guess = get_most_probable_word(remaining_words)
    guess_count += 1

    # Guess until the word is correct
    while (next_guess != actual_word):
        guess_count += 1

        # print("Guessing: " + next_guess)
        check_word(next_guess, actual_word)
        remaining_words = get_remaining_words(stats)
        next_guess = get_most_probable_word(remaining_words)

        if (next_guess == "No words left"):
            break


    if config["printGuesses"]:
        print(actual_word + " was guessed in " + str(guess_count) + " guesses")

    return guess_count


def get_remaining_words(stats):
    global remaining_words

    possible_words = []
    
    # Go through each word in the list
    for i in range(len(remaining_words)):
        word = remaining_words[i]

        # Go through each letter of that word
        for j in range(len(word)):
            letter = word[j]

            # Do_break is used to break out of the j loop from the k loop
            do_break = False
            for k in range(len(stats["wrong_spot"][j])):
                if stats["wrong_spot"][j][k] == letter:
                    do_break = True
                    break

            # Break out of j loop
            if do_break:
                break

            # Check if the letter is in the correct spot
            if stats["correct"][j] != '' and stats["correct"][j] != letter:
                break
            
            # Check if the letter is in the incorrect list
            if letter in stats["incorrect"]:
                break

            # If we've gone through all the letters and they all match
            if (j == len(word) - 1):
                possible_words.append(word)


    return possible_words


def get_most_probable_word(words):
    # Steps
    # 1. Count each letter in remaining words
    # 2. Assign each remaining word a score based on the number of letters in the word
    # 4. Pick the word with the highest score

    # Go through the words and count the letters
    letter_count = {}

    for i in range(len(words)):
        word = words[i]

        for j in range(len(word)):
            letter = word[j]

            if (letter in letter_count):
                letter_count[letter] += 1
            else:
                letter_count[letter] = 1

    # Go through the words and assign a score
    word_scores = {}
    for i in range(len(words)):
        word = words[i]
        score = 0

        for j in range(len(word)):
            letter = word[j]

            score += letter_count[letter]

            # If they are in the correct spot, add to the score
            if i == j:
                score += 100

        word_scores[word] = score

    if (len(word_scores) == 0):
        return "No words left"

    # Find the word with the highest score
    return max(word_scores, key=word_scores.get)


# Get the correct letters in the right spot, in the wrong spot, and letters not in the word
def check_word(guess, word):
    global stats

    correct = ['', '', '', '', '']
    wrong_spot = [[], [], [], [], []]
    incorrect = []

    for i in range(len(guess)):
        # Correct letters in the right spot
        # print(guess, word, i)
        if (guess[i] == word[i]):
            correct[i] = guess[i]

        # Correct letter in the wrong spot
        elif (guess[i] in word):
            wrong_spot[i].append(guess[i])

        # Incorrect Letter
        else:
            incorrect.append(guess[i])

    # Append to stats
    for i in range(len(correct)):
        # print(stats["correct"])

        if (stats["correct"][i] == ''):
            stats["correct"][i] = correct[i]
        
    for i in range(len(wrong_spot)):
        for j in range(len(wrong_spot[i])):
            if (wrong_spot[i][j] not in stats["wrong_spot"][i]):
                stats["wrong_spot"][i].append(wrong_spot[i][j])

    for i in range(len(incorrect)):
        if (incorrect[i] not in stats["incorrect"]):
            stats["incorrect"].append(incorrect[i])

