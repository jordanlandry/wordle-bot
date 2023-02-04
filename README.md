# Wordle Bot

A bot designed to solve the word guessing game, Wordle

## Features

- Type a word for the bot to guess
- Pick a random word for the bot to guess
- Change the starting word
- Compare the stats of two starting words
- Run the bot on every single word
- Run every single starting word, on every single word to get the best starting words for lowest average number of guesses, and lowest maximum number of guesses. Will also print out the worst words.

## How it works

The bot uses a starting word to guess the solution to the puzzle. It follows an algorithm to determin the most optimal next guess and continues to guess until it solves the word.

The bot eliminates words that cannot be the solution based on the information known about the word. For example, if the first letter is known to be 'w', all words that do not start with 'w' are removed.

The remaining words are then scored based on the number of letters they contain and the position of those letters. The word with the highest score is chosen as the next guess. This process continues until the word is solved.

## Scoring system

The scoring system works by first getting the total number of each letter in the remaining words. Then each word is assigned a score, which is just the total times each letter appears. For example, if there are 10 w's, and 4 o's, in the remaining words, then "World" will have a score of 14 (10 + 4). The position of the letters is also taken into consideration. When you are adding the score, the bot checks if the letters are in the same position, adding to the score if so.

## Getting Started

### Prerequisites

Before downloading the Wordle bot, make sure you have the following

1. [Python 3.x](https://www.python.org/downloads/)
2. [Git](https://git-scm.com/downloads) (Optional)

### Download and run

#### With Git

1. Clone the repository using `git clone https://github.com/jordanlandry/wordle-bot.git`.

2. Run the bot with `python main.py`

#### Without Git

1. Download bot.zip from the [releases section](https://www.github.com/wordle-bot/releases/tag/v1.0.0)
2. Extract the contents of bot.zip
3. Run the bot with `python main.py`

## Troubleshooting

If you encounter any issues while downloading or using the bot, please refer to the [issues page](https://github.com/jordanlandry/wordle-bot/issues) for troubleshooting tips or create a new issue for further assistance.

## Best and worst starting words

Average guesses per word
| Word | Avg guesses per word |
| ----- | -------------------- |
| trace | 3.7 |
| fuzzy | 4.7 |

Maximum number of guesses
| Word | Max guesses |
| ----- | ----------- |
| abled | 7 |
| equal | 11 |
