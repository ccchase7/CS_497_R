def searchify_news_title(news_title):
    char_replacements = [("%", "%25"), ("'", "%27"), (":", "%3A"), ("$", "%24"), ("#", "%23")]

    for replacements in char_replacements:
        news_title = news_title.replace(replacements[0], replacements[1])

    return news_title