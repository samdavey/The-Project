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
        Does not download the article or attempt to parse additional attributes until requested.
        
        Arguments:
            feedparser_entry: An 'entry' object from a feed parsed by feedreader.
        """
        self.downloaded = False
        self.parsed = False
        self.link = ''
        self.title = ''
        self.publisher = ''
        self.date = None
        self.html = u''
        # Get the article link
        if 'link' in feedparser_entry:
            self.link = feedparser_entry.link        # Will attempt to clean when parse()d
        else:
            raise ValueError('The feedparser entry used to create this Article instance does not have a link. Cannot continue.')
        
    def __repr__(self):
        return_date = ''
        if self.date != None:
            return_date = time.strftime('%Y-%m-%dT%H:%M:%SZ', self.date)

        return ('Article:\n' + \
            '    link:       {0}\n' + \
            '    downloaded: {5}\n' + \
            '    parsed:     {6}\n' + \
            '    title:      {1}\n' + \
            '    publisher:  {2}\n' + \
            '    date:       {3}\n' + \
            '    html:       {4}').format(self.link, self.title, self.publisher, return_date, self.html, self.downloaded, self.parsed)

    def to_string_without_html(self):
        return_date = ''
        if self.date != None:
            return_date = time.strftime('%Y-%m-%dT%H:%M:%SZ', self.date)
            
        return ('Article:\n' + \
            '    link:       {0}\n' + \
            '    downloaded: {4}\n' + \
            '    parsed:     {5}\n' + \
            '    title:      {1}\n' + \
            '    publisher:  {2}\n' + \
            '    date:       {3}\n').format(self.link, self.title, self.publisher, return_date, self.downloaded, self.parsed)

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

    def download(self):
        """
        Download the article HTML.
        """
        # Get the article HTML
        try:
            html_response = requests.get(self.link).text
        except Exception as e:
            raise e
        else:
            self.html = html_response
            self.downloaded = True    

    def parse(self):
        """
        Parse the downloaded article HTML, save the html and use it to parse additional article attributes.
        Prerequisite: article must be downloaded. Check with .is_downloaded()
        """
        
        if not self.is_downloaded():
            # ### BUG need a better exception
            raise Exception('Article has not been downloaded. Call download() before calling parse().')

        # Initiate a BeautifulSoup parser
        #   to read the article HTML for additional attributes
        soup = BeautifulSoup(self.html, 'lxml')
        
        # Get the article title
        if self.title == '' and soup.title.string:
            self.title = soup.title.string
        else:
            self.title = ''
            warnings.warn('Article title could not be found. Continuing.')
       
        # Get the publisher
        if self.publisher == '':
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
        self.parsed = True
        # ---------- End ---------- #

    def is_downloaded(self):
        """
        Returns True iff the article has been downloaded, else False.
        """
        return self.downloaded

    def is_parsed(self):
        """
        Returns True iff the article has been downloaded and parsed, else False.
        """
        return self.is_downloaded() and self.parsed


# Bugs:
# - Needs to be tested on non-googlenews feeds
# - Has absolutely no error recovery
# - Raises generic exceptions
