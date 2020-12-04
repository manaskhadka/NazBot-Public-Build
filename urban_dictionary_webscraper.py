"""
Web Scraper for urbandictionary.com
OUTPUT: DICTIONARY
By: monozide
-------------------------------------------------------------------------------
This program takes a word or phrase input and returns important corresponding
information (word/phrase found, definition, example, likes/dislikes) from
the most popular urbandictionary result relating to that phrase.
-------------------------------------------------------------------------------
Last Updated: 12/2020
"""
import requests


def urbandict(phrase):
    """
    Input: phrase of interest (string with only alphanumeric characters)
    Output: dict containing "title", "definition", "example sentence", "author",
            "likes, dislikes, date" from the top urbandictionary.com result for
            the phrase. If phrase is not found, returns -1
    --------------------------------------------------------------------------
    This function is what grabs the important values from the urbandict search
    query using the python requests module. the starter and ender library need
    to be manually found in terminal
    """

    data = requests.get(f"https://www.urbandictionary.com/define.php?term={phrase}")
    text = data.text
    library = {}

    # text limiter: remove all text not related to the most popular entry
    limiting_phrase = '</span></a></div></div><div class="right text-right"><a class="circle-link"'
    limiting_index = text.find(limiting_phrase)

    # if the limiting phrase is not found in the text, the searched phrase does not exist
    if limiting_index < 0:
        return -1

    text = text[0:limiting_index]

    # find the title
    title_starter = "<title>Urban Dictionary: "
    title_ender = '</title><link href="https://fonts.googleapis.com'
    title = phrase_locator(text, title_starter, title_ender)
    title = phrase_cleaner(title)
    library['title'] = title

    # find the definition
    definition_starter = 'property="fb:app_id"><meta content="'
    definition_ender = '" name="Description" property='
    definition = phrase_locator(text, definition_starter, definition_ender)
    definition = phrase_cleaner(definition)
    library['definition'] = definition

    # find the example sentence
    example_starter = '</div><div class="example">'
    example_ender = '</div><div class="contributor">by'
    example = phrase_locator(text, example_starter, example_ender)
    example = phrase_cleaner(example)

    library['example'] = example

    # find the author and date (have to find both because they are adjacent)
    author_date_starter = 'by <a href="/author.php?author='
    author_date_ender = '</div><div class="def-footer">'
    author_date = phrase_locator(text, author_date_starter, author_date_ender)

    author_starter = '">'
    author_ender = '</a> '
    author = phrase_locator(author_date, author_starter, author_ender)
    author = phrase_cleaner(author)
    library['author'] = author

    date_starter = author_ender
    date_starter_index = author_date.find(date_starter) + len(date_starter)
    date = author_date[date_starter_index:]
    library['date'] = date

    # find the likes
    # due to the nature of the database, have to narrow down text first
    likes_text_starter = "upvote"
    likes_text_ender = "downvote"
    likes_text = phrase_locator(text, likes_text_starter, likes_text_ender)

    likes_starter = 'class="count">'
    likes_ender = "</span></a><a"
    likes = phrase_locator(likes_text, likes_starter, likes_ender)
    library['likes'] = likes

    # find the dislikes
    # the dislikes are the last 1-5 chars of the main text body so using
    # rfind() to locate its index will be better than phrase_locator
    dislikes_locator = 'class="count">'
    dislikes_locator_index = text.rfind(dislikes_locator)
    dislikes_locator_index += len(dislikes_locator)
    dislikes = text[dislikes_locator_index:]
    library['dislikes'] = dislikes

    return library


def phrase_locator(text, phrase_starter, phrase_ender):
    """
    Inputs:
        text: text body (one massive string)
        phrase_starter: a phrase that always appears directly before the phrase of interest
        phrase_ender: a phrase that always appears directly after the phrase of interest
    Output:
        phrase: the phrase of interest
    ----------------------------------------------------------------------------------------
    This function looks through a response.text object (massive string) in order to
    find and return a dynamic phrase that changes for each urbandict search but is
    surrounded by text that is static (same regardless of search), thus enabling
    the dynamic phrase to be found with different searches
    """

    # find the starting index of the phrase
    phrase_starter_index = text.find(phrase_starter)

    # the starter index needs to be at the end of the starter string
    phrase_starter_index = phrase_starter_index + len(phrase_starter)

    # find the ending index of the phrase
    phrase_ender_index = text.find(phrase_ender)

    # use the indices to determine the phrase
    phrase = text[phrase_starter_index:phrase_ender_index]

    return phrase


def phrase_locator_inclusive(text, phrase_starter, phrase_ender):
    """
    This function is identical to the phrase_locator function, but the
    starting and ending library are inclusive in the output
    """

    # find the starting index of the phrase
    phrase_starter_index = text.find(phrase_starter)

    # find the ending index of the phrase
    phrase_ender_index = text.find(phrase_ender) + len(phrase_ender)

    # use the indices to determine the phrase
    phrase = text[phrase_starter_index:phrase_ender_index]

    return phrase


def phrase_cleaner(phrase):
    """
    Input: phrase (a string)
    Output: a cleaned phrase (a string)
    ------------------------------------------------------------------------
    This function parses a given string and removes html formatting (</>) and
    adds certain characters in place of placeholders (i.e. &apos; -> ')
    """
    starting_point = '<'
    ending_point = '>'

    while starting_point in phrase and ending_point in phrase:
        bad_phrase = phrase_locator_inclusive(phrase, starting_point, ending_point)
        phrase = phrase.replace(bad_phrase, "")

    placeholders = {'&apos;': "'", '&quot;': '"', '&lt;': '<', '&rt;': '>'}

    for placeholder in placeholders.keys():
        while placeholder in phrase:
            phrase = phrase.replace(placeholder, placeholders[placeholder])

    return phrase
