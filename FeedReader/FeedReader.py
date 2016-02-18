# coding: utf-8

# Sam Davey
# Version 1.0   :   19-Feb-2016 : Basic functionality

import feedparser
from bs4 import BeautifulSoup
import requests
import hashlib

def get_articles_from_feed(feed_url):
    """
    Objective:
        Capture all articles in an RSS feed and return them in a summary list.
    Arguments:
        feed_url: A URL string for the RSS feed.
    Returns:
        A list containing a number of feed summaries. Each feed summary is a 
        dictionary with the following keys:
            id                     : a md5 hash of the article URL; only the 
                                        real bits not the click-through crap
            metadata_feed_name     : name of the RSS feed or search criteria 
                                        that returned this article
            metadata_feed_link     : URL for the feed that the article was sourced from
            metadata_feed_accessed : timestamp when the article was obtained                                         
            article_title          : title of the article
            article_published      : timestamp when the article was first published
            article_publisher      : the news source
            article_link           : link to the article (minus the click-through crap)
            article_content        : the full html string of the article
    """
    # Use the feedparser to get an RSS feed. 
    parser = feedparser.parse(feed_url)

    # Create the list to return
    summary = []

    for item in parser['entries']:
        # Send GET request for the article and store the full html string
        article_html = requests.get(item.link).text

        # Clean the link to use in both the ID hash and the stored article_link
        link = get_clean_link(article_html, item.link)

        summary.append({'id': hashlib.md5(link.encode('utf-8')).hexdigest(),
                        'metadata_feed_name': parser.feed.title, 
                        'metadata_feed_link': parser.feed.link,
                        'metadata_feed_accessed': parser.feed.updated, 
                        'article_title': item.title, 
                        'article_published': item.published, 
                        'article_publisher': get_publisher(article_html),
                        'article_link': link,
                        'article_content': article_html
                       })

    return summary






def get_publisher(article_html):
    """
    Objective:
        Return an article's publisher by searching the <head> tags of the article.
    Arguments:
        An html string of an article
    Returns:
        The publisher name (string) if found, else a blank string.
    """
    
    # Initiate a BeautifulSoup parser
    soup = BeautifulSoup(article_html, 'html.parser')
    publisher = ''
    
    # The publisher might be in the meta-publisher tag. E.g.: <meta name="publisher" content="Business Insider Australia" />
    # It may also be in Facebook OpenGraph site_name tag. E.g.: <meta property="og:site_name" content="Business Insider Australia" />
    # The Twitter equivalents (twitter:site and twitter:creator) are Twitter handles and not of use to us.
    
    # Check for a standard meta-publisher tag first
    publisher_search = soup.find('meta', attrs={'property': 'publisher', 'content': True})
    if publisher_search == None:
        # No meta-publisher, so look for a Facebook publisher tag
        publisher_search = soup.find('meta', attrs={'property': 'og:site_name', 'content': True})

    # If we found something in either of these, use it. If not, publisher will hold the blank string.
    if publisher_search:
        publisher = publisher_search['content']

    return publisher





def get_clean_link(article_html, messy_link):
    """
    Objective:
        Return a clean version of messy_link by searching the <head> tags of the article.
    Arguments:
        article_html: an html string of the article
        messy_link: URL to the article in the BeautifulSoup object. messy_link 
            is assumed to contain redundant URL stuff tracking the click-through.
    Returns:
        A cleaned link (string) iff a better version was found, else returns the provided messy_link.
    """
    
    # Initiate a BeautifulSoup parser
    soup = BeautifulSoup(article_html, 'html.parser')
    link = messy_link
    
    # Check for a Facebook URL (og:url)
    link_search = soup.find('meta', attrs={'property': 'og:url', 'content': True})
    if link_search:
        link = link_search['content']
        
    # That failed, so try for a Twitter one (twitter:url)
    if link_search == None:
        link_search = soup.find('meta', attrs={'property': 'twitter:url', 'content': True})
        if link_search:
            link = link_search['content']
            
    # That failed, so try for a 'link rel="canonical"'
    if link_search == None:
        link_search = soup.find('link', attrs={'rel': 'canonical', 'href': True})
        if link_search:
            link = link_search['href']
    
    # If we found a result (link_search != None), then we've updated 'link', else it still contains the messy link 
    return link






def print_feed_summary(parsed_feed):
    """
    Objective:
        Prints the results of a parsed feed.
    Arguments:
        parsed_feed: A list of dictionary objects representing the articles in the feed.
    Returns:
        None.
        The printed summary contains all article fields except the article_content 
            (containing the full html).
    """
    for items in parsed_feed:
        print('--- Article Start ---')
        for keys,values in items.items():
            if keys != 'article_content':
                print(keys, ':\t', values)
        print('--- Article End ---\n')
    return


# Bugs:
# - Parse time stamps into useable formats
# - Needs to be tested on non-googlenews feeds
# - Has absolutely no error recovery

