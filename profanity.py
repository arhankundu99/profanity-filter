from utils import (get_complete_path, read_wordList)


class ProfanityFilter:
    def __init__(self):
        self.PROFANE_WORDSET = set()
        self.CHARS_MAPPING = {
            "a": ("a", "@", "*", "4"),
            "b": ("b", "6"),
            "i": ("i", "*", "l", "1"),
            "o": ("o", "*", "0", "@"),
            "u": ("u", "*", "v"),
            "v": ("v", "*", "u"),
            "l": ("l", "1", "I"),
            "e": ("e", "*", "3"),
            "s": ("s", "$", "5"),
            "t": ("t", "7")
        }
        self.default_wordlist_filename = get_complete_path('data/profanity_wordlist.txt')
        self.load_censor_words()

    def censor(self, text, censor_char="*", CUSTOM_WORDSET=None, WHITELIST_WORDSET=None):
        if CUSTOM_WORDSET is not None:
            self.PROFANE_WORDSET = CUSTOM_WORDSET
        if type(text) != str:
            text = str(text)
        if type(censor_char) != str:
            censor_char = str(censor_char)

        if len(self.PROFANE_WORDSET) == 0:
            self.load_censor_words()

        return self.censor_profane_words(text, censor_char, WHITELIST_WORDSET)

    def load_censor_words(self):
        profane_words = read_wordList(self.default_wordlist_filename)
        self.fill_profane_wordset(profane_words)

    def fill_profane_wordset(self, profane_words):
        all_censor_words = self.generate_possible_profane_words(profane_words)
        self.PROFANE_WORDSET = all_censor_words

    def generate_possible_profane_words(self, profane_words):
        all_censor_words = []
        for profane_word in profane_words:
            self.dfs(profane_word, 0, [], all_censor_words)
        return all_censor_words

    def dfs(self, profane_word, idx, char_list, all_censor_words):
        if idx == len(profane_word):
            possible_profane_word = ''
            for char in char_list:
                possible_profane_word += char
            all_censor_words.append(possible_profane_word)
            return

        if profane_word[idx] not in self.CHARS_MAPPING:
            char_list.append(profane_word[idx])
            self.dfs(profane_word, idx+1, char_list, all_censor_words)
            char_list.pop(len(char_list)-1)

        else:
            for char in self.CHARS_MAPPING[profane_word[idx]]:
                char_list.append(char)
                self.dfs(profane_word, idx + 1, char_list, all_censor_words)
                char_list.pop(len(char_list) - 1)

    def censor_profane_words(self, message, censor_char, WHITELIST_WORDSET):
        message = message.split()
        clean_message = ''
        for word in message:
            curr_word = ''
            if (word.lower()) in self.PROFANE_WORDSET and (WHITELIST_WORDSET is None or word.lower() not in WHITELIST_WORDSET):
                for i in range(len(word)):
                    curr_word += censor_char
            else:
                curr_word = word
            clean_message += curr_word + ' '
        return clean_message

    def isProfane(self, word):
        if word.lower() in self.PROFANE_WORDSET:
            return True
        return False

