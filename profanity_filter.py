from utils import (get_complete_path, read_wordList)
import requests
from PIL import Image, ImageFilter
from io import BytesIO
from trie import Trie


def get_image_profanity_score(image_url):
    r = requests.post(
        "https://api.deepai.org/api/nsfw-detector",
        data={
            'image': image_url,
        },
        headers={'api-key': 'YOUR_API_KEY'}
    )
    # if nsfw_score is more than 0.7 it is definitely profane
    return r.json()['output']['nsfw-score']


def get_image_analysis(url):
    r = requests.post(
        "https://api.deepai.org/api/nsfw-detector",
        data={
            'image': url,
        },
        headers={'api-key': 'YOUR_API_KEY'}
    )
    return r.json()['output']


def censor_image(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    # Applying GaussianBlur filter
    gaussImage = img.filter(ImageFilter.GaussianBlur(100))
    # gaussImage.show()

    # Save Gaussian Blur Image
    image_name = hash(image_url)
    gaussImage.save('images/'+str(image_name)+'.jpg')


class ProfanityFilter:
    def __init__(self):
        self.CHARS_MAPPING = {
            "a": ("a", "@", "*", "4"),
            "i": ("i", "*", "l", "1"),
            "o": ("o", "*", "0", "@"),
            "u": ("u", "*", "v"),
            "v": ("v", "*", "u"),
            "l": ("l", "1"),
            "e": ("e", "*", "3"),
            "s": ("s", "$", "5"),
            "t": ("t", "7")
        }
        self.censor_urls = set()
        self.profane_trie = Trie()
        self.default_wordlist_filename = get_complete_path('data/profanity_wordlist.txt')
        self.default_urls_filename = get_complete_path('data/profane_sites.txt')

        self.load_profane_words(profane_words=None, whitelist_words=None)
        self.load_profane_urls()

    def load_profane_words(self, profane_words, whitelist_words):
        self.profane_trie = Trie()
        if profane_words is None:
            profane_words = read_wordList(self.default_wordlist_filename)
        self.generate_possible_profane_words(profane_words, whitelist_words)

    def generate_possible_profane_words(self, profane_words, whitelist_words):
        for profane_word in profane_words:
            self.dfs(profane_word, 0, [], whitelist_words)

    def dfs(self, profane_word, idx, char_list, whitelist_words):
        if idx == len(profane_word):
            possible_profane_word = ''
            for char in char_list:
                possible_profane_word += char
            if whitelist_words is None or possible_profane_word not in whitelist_words:
                self.profane_trie.insert(possible_profane_word)
            return

        if profane_word[idx] not in self.CHARS_MAPPING:
            char_list.append(profane_word[idx])
            self.dfs(profane_word, idx + 1, char_list, whitelist_words)
            char_list.pop(len(char_list) - 1)

        else:
            for char in self.CHARS_MAPPING[profane_word[idx]]:
                char_list.append(char)
                self.dfs(profane_word, idx + 1, char_list, whitelist_words)
                char_list.pop(len(char_list) - 1)

    def load_profane_urls(self):
        profane_urls = read_wordList(self.default_urls_filename)
        for url in profane_urls:
            self.censor_urls.add(url)

    def censor_url(self, url):
        if self.censor_urls.__contains__(url):
            return '*'*len(url)
        return url

    def censor(self, text, censor_char="*"):

        if type(text) != str:
            text = str(text)
        if type(censor_char) != str:
            censor_char = str(censor_char)

        if self.profane_trie.root is None:
            self.load_profane_words()

        return self.censor_profane_words(text, censor_char)

    def censor_profane_words(self, message, censor_char):
        message = message.split()
        clean_message = ''
        for word in message:
            curr_word = ''
            if self.profane_trie.hasPrefix(word.lower()):
                for i in range(len(word)):
                    curr_word += censor_char
            else:
                curr_word = word
            clean_message += curr_word + ' '
        return clean_message

    def isProfane(self, word):
        if self.profane_trie.hasPrefix(word):
            return True
        return False

    def add_profane_words(self, words):
        for word in words:
            self.profane_trie.insert(word)

    def add_whitelist_words(self, words):
        for word in words:
            self.whiteList_trie.insert(word)
