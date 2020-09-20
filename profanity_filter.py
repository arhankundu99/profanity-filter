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
        self.censor_urls = set()
        self.profane_trie = Trie()
        self.whiteList_trie = Trie()
        self.default_wordlist_filename = get_complete_path('data/profanity_wordlist.txt')
        self.default_urls_filename = get_complete_path('data/profane_sites.txt')
        self.load_profane_words()
        self.load_profane_urls()

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

    def load_profane_words(self, custom_profane_wordlist=None, whitelist=None):
        if custom_profane_wordlist is not None:
            self.profane_trie = Trie()
            self.whiteList_trie = Trie()

            for word in whitelist:
                self.whiteList_trie.insert(word)
            self.fill_profane_wordset(custom_profane_wordlist)
        else:
            profane_words = read_wordList(self.default_wordlist_filename)
            self.fill_profane_wordset(profane_words)

    def fill_profane_wordset(self, profane_words):
        for profane_word in profane_words:
            if self.whiteList_trie.hasPrefix(profane_word, 0, self.whiteList_trie.root):
                continue
            self.profane_trie.insert(profane_word)

    def censor_profane_words(self, message, censor_char):
        message = message.split()
        clean_message = ''
        for word in message:
            curr_word = ''
            if self.profane_trie.hasPrefix(word.lower(), 0, self.profane_trie.root):
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
