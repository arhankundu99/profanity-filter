from profanity import ProfanityFilter

profanity_filter = ProfanityFilter()

print(profanity_filter.censor("you fuck fucker"))
print(profanity_filter.censor("you fuck fucker", WHITELIST_WORDSET={'fuck'}))
print(profanity_filter.isProfane("fuck"))

