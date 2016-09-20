import Feed

if __name__ == '__main__':
    # this script executed as a script
    
    url = 'https://news.google.com/news?cf=all&hl=en&pz=1&ned=au&q=lucapa+diamond+company&output=rss'
    print('Testing Feed_Reader')
    print('The test feed is:\n', url, '\n')
    
    # This will create the Feed object, which will get the feed items from the URL,
    #	and store them in it's datastructure of feed metadata and a list of Articles
    # Second arg limits the parser to tht first 5 feed items
    print('Feed({0})'.format(url))
    a = Feed.Feed(url)
    print(a)

    print('\Parsing the feed')
    a.parse(5)
    print(a)

    print('\nDownloading the feed articles')
    for article in a.articles:
        article.download()
    print(a)

    print('\nParsing the feed articles')
    for article in a.articles:
        article.parse()
    print(a)