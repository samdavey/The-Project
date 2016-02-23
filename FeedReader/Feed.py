import feedparser
import Article
import warnings
import time

class Feed:
    """
    Feed is a representation of an RSS feed.

    Attributes:
        name:            The string name of the feed.
        link:            The URL for the feed.
        accessed_date:    Timestamp for when this instance of the feed was accessed.
        articles:        List of Article objects.
    """
    def __init__(self, feed_url):
        # populate the link
        self.link = feed_url
        self.parsed = False
        self.name = ''
        self.accessed_date = None
        self.articles = []
        
 
    def __repr__(self):
        s = ''
        for item in self.articles:
            s = s + str(item) + '\n'
        return_date = ''
        if self.accessed_date != None:
            return_date = time.strftime('%Y-%m-%dT%H:%M:%SZ', self.accessed_date)

        return ('Feed(\n' + \
            '    link          : {0}\n' + \
            '    parsed        : {4}\n' + \
            '    name          : {1}\n' + \
            '    accessed_date : {2}\n' + \
            '    articles      :\n' + \
            '    [\n' + \
            '    {3}' + \
            '    ]\n' + \
            ')').format(self.link, self.name, return_date, s, self.parsed)

    def __str__(self):
        a = u''
        for item in self.articles:
            a = a + item.to_string_without_html() + '\n'
        return_date = ''
        if self.accessed_date != None:
            return_date = time.strftime('%Y-%m-%dT%H:%M:%SZ', self.accessed_date)

        return ('Feed:\n' + \
            '    link          : {0}\n' + \
            '    parsed        : {3}\n' + \
            '    name          : {1}\n' + \
            '    accessed_date : {2}\n' + \
            '    articles      :\n' + \
            '    [\n' + \
            '    ' + a + '\n' + \
            '    ]\n' + \
            ')').format(self.link, self.name, return_date, self.parsed)

    def parse(self, article_limit):
        """
        Downloads the RSS entries (not the article html itself) and populates the feed.
        """
        # parse the feed, giving us the 'feed' attributes and the 'entries'
        p = feedparser.parse(self.link)
        # use the feed attributes
        self.name = p.feed.title
        self.accessed_date = p.feed.updated_parsed
        # turn the entries into Articles
        self.articles = []
        i = 0
        for item in p['entries']:
            if i == article_limit: break
            try:
                i += 1
                #print('Found article: ', item.title)
                #print('         Link: ', item.link, '\n')
                a = Article.Article(item)
                self.articles.append(a)
            except ValueError as e:
                warnings.warn('A ValueError was raised: ', str(e))
        self.parsed = True

    def is_parsed(self):
        return self.parsed

    def has_articles(self):
        return self.articles.len > 0