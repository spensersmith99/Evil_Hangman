from __future__ import annotations
from collections import defaultdict # You might find this useful
import os

"""
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************

If you worked in a group on this project, please type the EIDs of your groupmates below (do not include yourself).
Leave it as TODO otherwise.
Groupmate 1: TODO
Groupmate 2: TODO
"""

class WordMakerHuman():
    def __init__(self, words_file, verbose):
        # we need to prompt the player for a word, then clear the screen so that player 2 doesn't see the word.
        self.verbose = verbose
        self.words = {} # Make sure that you understand dictionaries. They will be extremely useful for this project.
        with open(words_file) as wordfile:
            for line in wordfile:
                word = line.strip()
                if len(word) > 0:
                    self.words[word] = True # I could have made this a set() instead.

    def reset(self, word_length):
        # Your AI code should not call input() or print().
        question = ""
        while True:
            question = input(f"Please type in your word of length {word_length}: ")
            if question in self.words and len(question) == word_length:
                break
            print("Invalid word.")
        if not self.verbose:
            print("\n" * 100) # Clear the screen
        self.word = question

    def get_valid_word(self):
        return self.word

    def get_amount_of_valid_words(self):
        return 1 # the only possible word is self.word

    def guess(self, guess_letter):
        idx = self.word.find(guess_letter)
        ret = []
        while idx != -1:
            ret.append(idx)
            idx = self.word.find(guess_letter, idx + 1)
        return ret


# ----------------------------------------------------------------------------------------------------------------------

class WordMakerAI():
    def __init__(self, words_file: str, verbose=False):
        self.verbose = verbose
        self.dict = {}
        with open(words_file) as file_obj:
            for line in file_obj:
                word = line.strip()
                if len(word) > 0 and len(word) in self.dict:
                    self.dict[len(word)].append(word)
                else:
                    self.dict[len(word)] = [word]
        self.remaining_words = list(self.dict.values())[0]

    def reset(self, word_length: int) -> None:
        self.remaining_words = self.dict[word_length]

    def get_valid_word(self) -> str:
        return self.remaining_words[0]

    def get_amount_of_valid_words(self) -> int:
        return len(self.remaining_words)

    def get_letter_positions_in_word(self, word: str, guess_letter: str) -> tuple[int, ...]:
        result = []
        count = 0
        for letter in word:
            if letter == guess_letter:
                result.append(count)
            count += 1
        return tuple(result)

    def guess(self, guess_letter) -> list[int]:
        my_dict = {}
        for word in self.remaining_words:
            letter_pos = self.get_letter_positions_in_word(word, guess_letter)
            if letter_pos in my_dict:
                my_dict[letter_pos].append(word)
            else:
                my_dict[letter_pos] = [word]
        self.remaining_words = sorted(my_dict.items(), key=lambda x: (-len(x[1]), len(x[0])))[0][1]
        print(self.remaining_words)
        ## choose the family with the biggest length
        for key in my_dict:
            length = len(my_dict[key])
            my_dict[key] = length

        v = sorted(my_dict.items(), key=lambda x: (-x[1], len(x[0])))
        return list(v[0][0])