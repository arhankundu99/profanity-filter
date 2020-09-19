# profanity-filter

Most of the words which are in the `profane_wordlist.txt` are taken from Bad Words list for Facebook. <br/>
Supports modified spellings like `D@mn`, `$h1t` etc. <br/>
This library is significantly faster than other profanity filters which use **regex or string.contains() methods**. <br/>
The filter also censors words if their prefixes match with any profane word. 

## Working

```python
import profanity_filter
filter = profanity_filter.ProfanityFilter()
clean_text = profanity_filter.censor("D*mnn you!")
print(clean_text) 
# ***** you!
```

All modified spellings of profane words will be detected
Example: `D*mn, D@mn, $h17, 4r53` etc

## Add your custom profane wordlist and custom whitelist
```python
filter.load_profane_words(custom_profane_wordlist = {'damn', 'douche'}, whitelist = {'shit'})
```

## Check if your text has any profane word
```python
filter.isProfane('You piece of $h*t')
# returns true
```

## How this profanity filter works for text words
The entire profanity wordlist which consists of 130 mostly profane words are inserted into a trie.
```python
CHARS_MAPPING = {
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
```
This map maps characters with set of similar looking alphabets.Then checking whether the word has a prefix which is present in the trie is done recursively. When we encounter numbers or symbols like `@` or `*` we use the map, replace the character and continue searching recursively <br/>

Time Complexity to check whether a word is profane is `O(length of the word)`.

## Add more profane words
```python
filter.add_profane_words(['abc', 'def'])
```

## Add more whitelist words
```python
filter.add_whitelist_words(['abc', 'def'])
```

## Censor profane urls
```python
filter.censor_url(url)
```

## Check whether your image is profane or not
```python
r = filter.get_image_analysis(IMAGE_URL)
print(r.json())
# json output which contains profanity_score of the image and other details
```
This is done with the help of `DeepAI` Api <br/>
<https://deepai.org/machine-learning-model/nsfw-detector>

## Censor your profane image
```python
filter.censor(image_url)
```
This is done with the help of pillow library which is a Photo imaging library <br/>
<https://pypi.org/project/Pillow/>




