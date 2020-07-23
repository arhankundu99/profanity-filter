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




