"""
Python basics, Problem Set, hangman.py
Name: Luong Minh Tung
Collaborators: TODO
Time spent: 1 day
"""

# ---------------------------------------------------------------------------- #
#                                 Hangman Game                                 #
# ---------------------------------------------------------------------------- #


# -------------------------------- Helper code ------------------------------- #
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string
from colorama import init, Fore, Style
import time

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    with open(WORDLIST_FILENAME, "r") as inFile:
        # line: string
        line = inFile.readline()
        # wordlist: list of strings
        wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# ---------------------------- end of helper code ---------------------------- #


# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing; assumes all letters are lowercase
    letters_guessed: list (of letters), which letters have been guessed so far, assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed, False otherwise
    """
    # TODO: FILL IN YOUR CODE HERE AND DELETE "pass"
    """
    for letter in secret_word.lower():
        if letter not in letters_guessed:
            return False
    return True
    """
    return all(letter in letters_guessed for letter in secret_word.lower())

def get_guessed_word(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
        which letters in secret_word have been guessed so far.
    """
    # TODO: FILL IN YOUR CODE HERE AND DELETE "pass"
    #secret_word = choose_word(wordlist) 
    """
    result = ""
    for char in secret_word:
        if char in letters_guessed:
            result += letter
        else:
            result += "_"
    """
    result = "".join([char if char in letters_guessed else "_" for char in secret_word])
    return result


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not yet been guessed.
    """
    # TODO: FILL IN YOUR CODE HERE AND DELETE "pass"
    import string
    all_letters = string.ascii_lowercase #type = str
    """
    available_letters = ""
    for letter in all_letters:
        if letter not in letters_guessed:
            available_letters += letter
    """
    available_letters = "".join([letter if letter not in letters_guessed else "_" for letter in all_letters])
    return available_letters

def Make_Color():
    """
    Make color for text
    """ 
    return ("Pleas guess letter: " + Fore.BLUE)

def hangman(secret_word):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
    letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
    s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
    sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
    about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
    partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    """
    # TODO: FILL IN YOUR CODE HERE AND DELETE "pass"

    letters_guessed = [] 
    letters_guessed_2 = ""
    available_letters = ""
    s = ""
    # guesses left
    nums = 6
    # Combat score         
    TotalScore = 1
    # Vowels and Consonants 
    Vowels = ['a', 'i', 'e', 'o', 'u']
    Consonants = "".join([char if char not in Vowels else "_" for char in string.ascii_lowercase])
    
    secret_word
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", nums, "letters long") 
    #get_guessed_word(secret_word, letters_guessed)
    warning_point = 3
    print("You have",warning_point,"warnings left")
    
    while True:
        if nums <= 0:
            print("Your guesses left is 0")
            print("The result is", secret_word)
            break

        available_letters = get_available_letters(letters_guessed)
        letters_guessed_2 = "".join([char for char in letters_guessed])

        print("----------------------------------------------")
        print("You have", nums , "guesses left")
        print("Available letters:", get_available_letters(letters_guessed))
        
        init() 
        s = str(input(Make_Color()))
        print(Style.RESET_ALL) 
        letters_guessed.append(s) 

        if nums <= 0: 
            print("Sorry, you ran out of guesses.")
            print("The result is", secret_word)
            break

        elif s not in available_letters:
            warning_point -= 1
            if warning_point > 0: 
                print("Oops! You've already guessed that letter. You have", warning_point, "warnings left:", get_guessed_word(secret_word, letters_guessed))
                
            elif warning_point <= 0:
                print("Oops! You've already guessed that letter. You have 0 warnings left, you lose one guess", get_guessed_word(secret_word, letters_guessed))
                nums -= 1

        elif is_word_guessed(secret_word, letters_guessed) == True:
            # The total score is the number of guesses_remaining once the user has guessed the secret_word times the number of unique letters in secret_word. 
            TotalScore = len(secret_word)*nums
            print("Good guess:", secret_word)
            print("Congratulations, you won!")
            print("----------------------------------------------")
            print("Your total score for this game is: ", TotalScore)
            break

        elif s in secret_word and (str.isalpha(s) == True or str.lower(s) == True):
            # Check if user correctly guessed the letter of secret_word -> show the user
            print("Good guess:", get_guessed_word(secret_word, letters_guessed))

        # If users inputs a consonant that hasn’t been guessed and the consonant is not in the secret word
        elif s not in secret_word and (str.isalpha(s) == True or str.lower(s) == True): 
            print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed)) 
            if s not in letters_guessed_2:
                if s in Consonants:
                    nums -= 1
                elif s in Vowels:
                    nums -= 2
        
        # If user inputs anythings besides an alphabet
        elif str.isalpha(s) == False or str.lower(s) == False:
            warning_point -= 1
            if warning_point > 0:
                print("Oops! That is not a valid letter. You have", warning_point, "warnings left:", get_guessed_word(secret_word, letters_guessed))
            elif warning_point <= 0:
                print("you have 0 warning, you lose one guess")
                nums -= 1
                #warning_point = 0
   

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# ---------------------------------------------------------------------------- #


def match_with_gaps(my_word, other_word):
    """
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular english word
    returns: boolean, true if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        false otherwise:
    """
    # todo: fill in your code here and delete "pass"
    if len(my_word) != len(other_word):
        return False 
    for i in range(len(my_word)):
        if my_word[i] != "_" and my_word[i] != other_word[i]:
            return False
    return True

def show_possible_matches(my_word):
    """
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word

    Keep in mind that in hangman when a letter is guessed, all the positions
    at which that letter occurs in the secret word are revealed.
    Therefore, the hidden letter(_) cannot be one of the letters in the word
    that has already been revealed.

    """
    # Load the wordlist
    wordlist = load_words()

    # Create a list to store matching words
    matching_words = []

    # Iterate over each word in the wordlist
    for word in wordlist:
        if len(my_word) == len(word):
            # Check if the word matches the pattern of my_word
            is_match = True
            for i in range(len(my_word)):
                if my_word[i] != '_' and my_word[i] != word[i]:
                    is_match = False
                    break
            if is_match:
                matching_words.append(word)

    for word in matching_words:
        print(word)


def hangman_with_hints(secret_word):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman with the ability to request hints.

    * At the start of the game, let the user know how many
    letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
    s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
    about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
    partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
    matches the current guessed word as hints.

    Follows the other limitations detailed in the problem write-up.
    """

    """
    letters_guessed: list (of letters), which letters have been guessed so far, assumes that all letters are lowercase

    letters_guessed_2: string, converted to letters_guessed to check the character input is Vowels or Consonants

    available_letters:  string (of letters), comprised of letters that represents which letters have not yet been guessed.
    
    TotalScore: int, combat score 
    """
    letters_guessed = [] 
    letters_guessed_2 = ""
    available_letters = ""
    s = ""
    # guesses left
    nums = 6
    # Combat score         
    TotalScore = 1
    # Vowels and Consonants 
    Vowels = ['a', 'i', 'e', 'o', 'u']
    Consonants = "".join([char if char not in Vowels else "_" for char in string.ascii_lowercase])
    
    secret_word
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", nums, "letters long") 
    #get_guessed_word(secret_word, letters_guessed)
    warning_point = 3
    print("You have",warning_point,"warnings left")
    
    while True:
        if nums <= 0:
            print("Your guesses left is 0")
            print("The result is", secret_word)
            break

        available_letters = get_available_letters(letters_guessed)
        letters_guessed_2 = "".join([char for char in letters_guessed])

        print("----------------------------------------------")
        print("You have", nums , "guesses left")
        print("Available letters:", get_available_letters(letters_guessed))
        
        init() 
        s = str(input(Make_Color()))
        print(Style.RESET_ALL) 
        letters_guessed.append(s) 
        #print("ZIA",zia)

        if s == '*':
            print("Possible word matches:")
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            continue

        elif nums <= 0: 
            print("Sorry, you ran out of guesses.")
            print("The result is", secret_word)
            break

        elif s not in available_letters:
            warning_point -= 1
            if warning_point > 0: 
                print("Oops! You've already guessed that letter. You have", warning_point, "warnings left:", get_guessed_word(secret_word, letters_guessed))
                
            elif warning_point <= 0:
                print("Oops! You've already guessed that letter. You have 0 warnings left, you lose one guess", get_guessed_word(secret_word, letters_guessed))
                nums -= 1

        elif is_word_guessed(secret_word, letters_guessed) == True:
            # The total score is the number of guesses_remaining once the user has guessed the secret_word times the number of unique letters in secret_word. 
            TotalScore = len(secret_word)*nums
            print("Good guess:", secret_word)
            print("Congratulations, you won!")
            print("----------------------------------------------")
            print("Your total score for this game is: ", TotalScore)
            break

        elif s in secret_word and (str.isalpha(s) == True or str.lower(s) == True):
            # Check if user correctly guessed the letter of secret_word -> show the user
            print("Good guess:", get_guessed_word(secret_word, letters_guessed))

        # If users inputs a consonant that hasn’t been guessed and the consonant is not in the secret word
        elif s not in secret_word and (str.isalpha(s) == True or str.lower(s) == True): 
            print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed)) 
            if s not in letters_guessed_2:
                if s in Consonants:
                    nums -= 1
                elif s in Vowels:
                    nums -= 2
        
        # If user inputs anythings besides an alphabet
        elif str.isalpha(s) == False or str.lower(s) == False:
            warning_point -= 1
            if warning_point > 0:
                print("Oops! That is not a valid letter. You have", warning_point, "warnings left:", get_guessed_word(secret_word, letters_guessed))
            elif warning_point <= 0:
                print("you have 0 warning, you lose one guess")
                nums -= 1
                #warning_point = 0


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass
 
    # Test the function after build
    """   
    secret_word = choose_word(wordlist)
    letters_guessed = []
    print(secret_word)
    print("Func1 ",is_word_guessed(secret_word, letters_guessed))
    print("Func2 ",get_guessed_word(secret_word, letters_guessed))
    print("Func3 ",get_available_letters(letters_guessed))
    """

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
     

    secret_word = choose_word(wordlist)
    #print(secret_word)
    #hangman(secret_word)

# ---------------------------------------------------------------------------- #

# To test part 3 re-comment out the above lines and
# uncomment the following two lines.

    # Test the func 
    #print(match_with_gaps("a_ple", "apple"))
    #show_possible_matches("t__t")
    #secret_word = choose_word(wordlist)

    hangman_with_hints(secret_word)

