# profanity-filter

Most of the words which are in the `profane_wordlist.txt` are taken from Bad Words list for Facebook. <br/>
Supports modified spellings like `D@mn`, `$h1t` etc. <br/>
This library is significantly faster than other profanity filters which use regex. <br/>
The filter also censors words if their prefixes match with any profane word. 

## Working

```python
from profanity import ProfanityFilter
profanity_filter = ProfanityFilter()
clean_text = profanity_filter.censor("D*mn you!")
print(clean_text) 
# **** you!
```

## Add your custom profane wordlist and custom whitelist
```python
profanity_filter.load_profane_words(custom_profane_wordlist = {'damn', 'douche'}, whitelist = {'shit'})
```

## Check if your text has any profane word
```python
profanity_filter.isProfane('You piece of $h*t')
# returns true
```

## How this profanity filter works for text words

```python
MAP = {
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
```
This map maps characters with set of similar looking characters. Using this map and DFS, we generate modified spelling words of the words present in the `profane_wordlist.txt` and add them into a trie data structure. So if the prefix of the word is present in the trie, then it is profane otherwise not. For example the filter will detect `D@mnyou` as profane as it's prefix `Damn` is a profane word <br/>

For example if our profane word is 'abe', then the DFS algorithm would generate:
```abe, @be, *be, 4be, a6e, ab*, ab5...etc```

The purpose of using DFS is to generate distorted profane words. <br/>

The wordlist contains a total of **1,48,549** words, including 162 words from the default profanity_wordlist.txt and their variants by modified spellings. <br/>

Time Complexity to check whether a word is profane is `O(length of the word)`.

## Check whether your image is profane or not
```python
r = profanity_filter.get_image_analysis(IMAGE_URL)
print(r.json())
# json output which contains profanity_score of the image and other details
```
This is done with the help of `DeepAI` Api <br/>
<https://deepai.org/machine-learning-model/nsfw-detector>

## Censor your profane image
```python
profanity_filter.censor(image_url)
```
This is done with the help of pillow library which is a Photo imaging library <br/>
<https://pypi.org/project/Pillow/>



