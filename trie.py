from collections import defaultdict


class Trie:
    def __init__(self):
        self.root = defaultdict()
        self.CHARS_MAPPING = {
            "@": ("a", "o"),
            "*": ("a", "i", "o", "u", "v", "e"),
            "4": "a",
            "6": "b",
            "1": ("i", "l"),
            "0": "o",
            "3": ("e", "b"),
            "$": "s",
            "5": "s",
            "7": "t"
        }

    # @param {string} word
    # @return {void}
    # Inserts a word into the trie.
    def insert(self, word):
        current = self.root
        for letter in word:
            current = current.setdefault(letter, {})
        current.setdefault("_end")

    # @param {string} word
    # @return {boolean}
    # Returns if the word is in the trie.
    def search(self, word):
        current = self.root
        for letter in word:
            if letter not in current:
                return False
            current = current[letter]
        if "_end" in current:
            return True
        return False

    def hasPrefix(self, word, idx, current):
        if "_end" in current:
            return True
        if idx == len(word):
            return False
        if word[idx] in self.CHARS_MAPPING:
            for char in self.CHARS_MAPPING[word[idx]]:
                if char in current:
                    if self.hasPrefix(word, idx+1, current[char]):
                        return True
        elif word[idx] in current:
            return self.hasPrefix(word, idx+1, current[word[idx]])
        return False

    # @param {string} prefix
    # @return {boolean}
    # Returns if there is any word in the trie
    # that starts with the given prefix.
    def startsWith(self, prefix):
        prefix = prefix.lower()
        current = self.root
        for letter in prefix:
            if letter not in current:
                return False
            current = current[letter]
        return True



