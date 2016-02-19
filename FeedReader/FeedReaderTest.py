import Feed

if __name__ == '__main__':
    # this script executed as a script
    
    url = 'https://news.google.com/news?cf=all&hl=en&pz=1&ned=au&q=lucapa+diamond+company+kimberlite&output=rss'
    print('Testing Feed_Reader')
    print('The test feed is:\n', url, '\n')
    
    # This will create the Feed object, which will get the feed items from the URL,
    #	and store them in it's datastructure of feed metadata and a list of Articles
    # Second arg limits the parser to tht first 5 feed items
    a = Feed.Feed(url, 5)

    # Prove it
    print(a)