### PythonBasic1
This problem set will introduce you to the topic of creating functions in Python, as well 
as looping mechanisms for repeating a computational process until a condition is 
reached.  
Note on Collaboration​:  
	You may work with other students. However, each student should write up and hand 
	in his or her assignment separately. Be sure to indicate with whom you have worked 
	in the comments of your submission.

# Problem 1: Basic Hangman 
You will implement a variation of the classic word game Hangman. If you are unfamiliar with the rules of the game, read 
http://en.wikipedia.org/wiki/Hangman_(game). Don’t be intimidated by this problem 
it's actually easier than it looks! We will 'scaffold' this problem, guiding you through 
the creation of helper functions before you implement the actual game.

# A.Getting Started 
Download the files “hangman.py” and “words.txt”, and save them both in the same 
directory​. Run the file hangman.py before writing any code to ensure your files are 
saved correctly. The code we have given you loads in words from a file. You should 
see the following output in your shell:  
	```
	
	Loading word list from file... 
 
	55900 words loaded. 
 
	```
If you see the above text, continue on to Hangman Game Requirements.  
If you don’t, double check that both files are saved in the same place! 
# B) Hangman Game Requirements 
You will implement a function called hangman that will allow the user to play hangman 
against the computer. The computer picks the word, and the player tries to guess 
letters in the word.  
Here is the general behavior we want to implement. Don’t be intimidated! This is just 
a description; we will break this down into steps and provide further 
functional specs later on in the pset so keep reading!  
	```

	1. The computer must select a word at random from the list of available words 
	that was provided in words.txt Note that words.txt contains words in all lowercase letters.

	2. The user is given a certain number of guesses at the beginning. 
 
	3. The game is interactive; the user inputs their guess and the computer either:
  
		a. reveals the letter if it exists in the secret word  

		b. penalize the user and updates the number of guesses remaining  

	4. The game ends when either the user guesses the secret word, or the user runs 
	out of guesses. 

	```
