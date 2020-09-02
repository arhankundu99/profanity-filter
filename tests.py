from profanity import ProfanityFilter
import requests
from trie import Trie

profanity_filter = ProfanityFilter()


def text_check():
    print(profanity_filter.censor("you shitty asshole"))
    profanity_filter.load_profane_words(custom_profane_wordlist={'fucker'}, whitelist={'shit'})
    print(profanity_filter.censor("you shit fucker"))


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


text_check()
url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSeoDsxkN3DuFG41gXq1-jggFC3mH9YjnMcbw&usqp=CAU'
# censor_image(url)


