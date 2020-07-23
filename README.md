# profanity-filter

Most of the words which are in the `profane_wordlist.txt` are taken from Bad Words list for Facebook.

## Working

```python
from profanity import ProfanityFilter
profanity_filter = ProfanityFilter()
clean_text = profanity_filter.censor("you f*uk")
print(clean_text) 
# you ****
```

You can add your custom profane wordlist and custom whitelist
```python
profanity_filter.load_profane_words(custom_profane_wordlist = {'damn', 'douche'}, whitelist = {'shit'})
```

Check if your text has any profane word
```python
profanity_filter.isProfane('You piece of $h*t')
# returns true
```

# How this profanity filter works

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
This map maps characters with set of similar looking characters. Using this map and DFS, we can generate modified spelling words of the words present in the `profane_wordlist.txt` and add them into a set. So if the word is present in the set, then it is profane otherwise not.

For example if our profane word is 'abe', then the DFS algorithm would generate:
```abe, @be, *be, 4be, a6e, ab*, ab5...etc```




