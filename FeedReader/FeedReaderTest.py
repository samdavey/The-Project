import FeedReader

if __name__ == '__main__':
    # this script executed as a script
    
    feed = 'https://news.google.com/news?cf=all&hl=en&pz=1&ned=au&q=lucapa+diamond+company+kimberlite&output=rss'
    print('Testing Feed_Reader')
    print('The test feed is:\n', feed)
    FeedReader.print_feed_summary(FeedReader.get_articles_from_feed(feed))