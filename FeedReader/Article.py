# coding: utf-8

# Sam Davey
# Version 1.0   :   19-Feb-2016 : Basic functionality

import feedparser
from bs4 import BeautifulSoup
import requests
import hashlib
import warnings
import time


class Article:
    """
    An Article represents a news article with its associated metadata.
    
    Attributes:
        link:       Clean link to the article 
                        (minus the referrer attributes where possible)
        title:      Title of the article
        publisher:  News source of the article
        date:       Timestamp when the article was published
        html:       The full HTML text of the article
    """
    
    def __init__(self, feedparser_entry):
        """
        Create a new Article.
        Downloads and reads the article on creation.
        
        Arguments:
            feedparser_entry: An 'entry' object from a feed parsed by feedreader.
        """
        
        # ---------- Initiate the object attributes ---------- #

        # Get the article link
        if 'link' in feedparser_entry:
            self.link = feedparser_entry.link        # Attempt to clean below
        else:
            raise ValueError('The feedparser entry used to create this Article instance does not have a link. Cannot continue.')
        
        # Get the article HTML and initiate a BeautifulSoup parser
        #   to read the article HTML for additional attributes
        self.html = requests.get(self.link).text
        soup = BeautifulSoup(self.html, 'lxml')
        
        # Get the article title
        if 'title' in feedparser_entry:
            self.title = feedparser_entry.title
        elif soup.title.string:
            self.title = soup.title.string
        else:
            self.title = ''
            warnings.warn('Article title could not be found. Continuing.')
       
        # Get the article published date
        if 'published_parsed' in feedparser_entry:
            self.date = feedparser_entry.published_parsed
        else:
            self.date = None
            warnings.warn('Article published date could not be determined. Continuing.')

        # Get the publisher
        self.publisher = ''
        # Use the publisher parsed from the RSS feed inf possible
        if 'publisher' in feedparser_entry:
            self.publisher = feedparser_entry.publisher
        else:
            # Wasn't parsed from the feed, so try to find it in the <head>
            # Check for a standard meta-publisher tag first
            publisher_search = soup.find('meta', attrs={'property': 'publisher', 'content': True})
            if publisher_search == None:
                # No meta-publisher, so look for a Facebook publisher tag
                publisher_search = soup.find('meta', attrs={'property': 'og:site_name', 'content': True})
            # Note: The Twitter equivalents (twitter:site and twitter:creator) are Twitter handles and not of use to us.
            # If we found something in either of these, use it. If not, publisher will hold the blank string.
            if publisher_search:
                self.publisher = publisher_search['content']
        # If the published wasn't found, we've retained the empty string
        
        # ---------- Clean the article link ---------- #
        # Article links are often full of referrer detail and other junk.
        # Attempt to clean it by looking in the <head> tags of the articls HTML

        # Check for a Facebook URL (og:url) first
        link_search = soup.find('meta', attrs={'property': 'og:url', 'content': True})
        if link_search:
            self.link = link_search['content']
            
        # If that failed, try for a Twitter one (twitter:url)
        if link_search == None:
            link_search = soup.find('meta', attrs={'property': 'twitter:url', 'content': True})
            if link_search:
                self.link = link_search['content']
                
        # If that failed, try for a 'link rel="canonical"'
        if link_search == None:
            link_search = soup.find('link', attrs={'rel': 'canonical', 'href': True})
            if link_search:
               self.link = link_search['href']
        
        # If we found a result (link_search != None), then we've updated 
        #   'self.link', else it still contains the messy link that the class 
        #   was instantiated with
        
        # ---------- End ---------- #

    def __repr__(self):
        return ('Article:\n' + \
            '    link:      {0}\n' + \
            '    title:     {1}\n' + \
            '    publisher: {2}\n' + \
            '    date:      {3}\n' + \
            '    html:      {4}').format(self.link, self.title, self.publisher, time.strftime('%Y-%m-%dT%H:%M:%SZ', self.date), self.html)

    def to_string_without_html(self):
        return ('Article:\n' + \
            '    link:      {0}\n' + \
            '    title:     {1}\n' + \
            '    publisher: {2}\n' + \
            '    date:      {3}\n').format(self.link, self.title, self.publisher, time.strftime('%Y-%m-%dT%H:%M:%SZ', self.date))

    def get_html_body(self):
        """
        Return the complete <body> of the article HTML, with tags.
        """
        return BeautifulSoup(self.html, 'lmxl').body
        
    def get_html_head(self):
        """
        Return the complete <head> of the article HTML, with tags.
        """
        return BeautifulSoup(self.html, 'lmxl').head
        

# def get_articles_from_feed(feed_url):
#     """
#     Objective:
#         Capture all articles in an RSS feed and return them in a summary list.
#     Arguments:
#         feed_url: A URL string for the RSS feed.
#     Returns:
#         A list containing a number of feed summaries. Each feed summary is a 
#         dictionary with the following keys:
#             id                     : a md5 hash of the article URL; only the 
#                                         real bits not the click-through crap
#             metadata_feed_name     : name of the RSS feed or search criteria 
#                                         that returned this article
#             metadata_feed_link     : URL for the feed that the article was sourced from
#             metadata_feed_accessed : timestamp when the article was obtained                                         
#             article_title          : title of the article
#             article_published      : timestamp when the article was first published
#             article_publisher      : the news source
#             article_link           : link to the article (minus the click-through crap)
#             article_content        : the full html string of the article
#     """
#     # Use the feedparser to get an RSS feed. 
#     parser = feedparser.parse(feed_url)

#     # Create the list to return
#     summary = []

#     for item in parser['entries']:
#         # Send GET request for the article and store the full html string
#         article_html = requests.get(item.link).text

#         # Clean the link to use in both the ID hash and the stored article_link
#         link = get_clean_link(article_html, item.link)

#         summary.append({'id': hashlib.md5(link.encode('utf-8')).hexdigest(),
#                         'metadata_feed_name': parser.feed.title, 
#                         'metadata_feed_link': parser.feed.link,
#                         'metadata_feed_accessed': parser.feed.updated, 
#                         'article_title': item.title, 
#                         'article_published': item.published, 
#                         'article_publisher': get_publisher(article_html),
#                         'article_link': link,
#                         'article_content': article_html
#                        })

#     return summary






# def get_publisher(article_html):
#     """
#     Objective:
#         Return an article's publisher by searching the <head> tags of the article.
#     Arguments:
#         An html string of an article
#     Returns:
#         The publisher name (string) if found, else a blank string.
#     """
    
#     # Initiate a BeautifulSoup parser
#     soup = BeautifulSoup(article_html, 'html.parser')
#     publisher = ''
    
#     # The publisher might be in the meta-publisher tag. E.g.: <meta name="publisher" content="Business Insider Australia" />
#     # It may also be in Facebook OpenGraph site_name tag. E.g.: <meta property="og:site_name" content="Business Insider Australia" />
#     # The Twitter equivalents (twitter:site and twitter:creator) are Twitter handles and not of use to us.
    
#     # Check for a standard meta-publisher tag first
#     publisher_search = soup.find('meta', attrs={'property': 'publisher', 'content': True})
#     if publisher_search == None:
#         # No meta-publisher, so look for a Facebook publisher tag
#         publisher_search = soup.find('meta', attrs={'property': 'og:site_name', 'content': True})

#     # If we found something in either of these, use it. If not, publisher will hold the blank string.
#     if publisher_search:
#         publisher = publisher_search['content']

#     return publisher





# def get_clean_link(article_html, messy_link):
#     """
#     Objective:
#         Return a clean version of messy_link by searching the <head> tags of the article.
#     Arguments:
#         article_html: an html string of the article
#         messy_link: URL to the article in the BeautifulSoup object. messy_link 
#             is assumed to contain redundant URL stuff tracking the click-through.
#     Returns:
#         A cleaned link (string) iff a better version was found, else returns the provided messy_link.
#     """
    
#     # Initiate a BeautifulSoup parser
#     soup = BeautifulSoup(article_html, 'html.parser')
#     link = messy_link
    
#     # Check for a Facebook URL (og:url)
#     link_search = soup.find('meta', attrs={'property': 'og:url', 'content': True})
#     if link_search:
#         link = link_search['content']
        
#     # That failed, so try for a Twitter one (twitter:url)
#     if link_search == None:
#         link_search = soup.find('meta', attrs={'property': 'twitter:url', 'content': True})
#         if link_search:
#             link = link_search['content']
            
#     # That failed, so try for a 'link rel="canonical"'
#     if link_search == None:
#         link_search = soup.find('link', attrs={'rel': 'canonical', 'href': True})
#         if link_search:
#             link = link_search['href']
    
#     # If we found a result (link_search != None), then we've updated 'link', else it still contains the messy link 
#     return link








# Bugs:
# - Needs to be tested on non-googlenews feeds
# - Has absolutely no error recovery

