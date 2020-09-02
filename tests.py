from profanity import ProfanityFilter
import requests
from trie import Trie

profanity_filter = ProfanityFilter()


def text_check():
    print(profanity_filter.censor("you douchebag"))
    profanity_filter.load_profane_words(custom_profane_wordlist={'douche'}, whitelist={'shit'})
    print(profanity_filter.censor("you shit douche"))


def get_image_analysis(URL):
    r = requests.post(
        "https://api.deepai.org/api/nsfw-detector",
        data={
            'image': URL,
        },
        headers={'api-key': '7b0ebb62-4127-46a7-877f-2d520f635a75'}
    )
    print(r.json()['output'])


def censor_image(URL):
    profanity_filter.censor_image(URL)


def trie_test():
    test = Trie()
    test.insert('helloworld')
    test.insert('ilikeapple')
    test.insert('helloz')

    print(test.search('hello'))
    print(test.startsWith('hello'))
    print(test.search('ilikeapple'))


def count():  # returns count of profane words including the ones generated using dfs
    print(profanity_filter.count)
    


