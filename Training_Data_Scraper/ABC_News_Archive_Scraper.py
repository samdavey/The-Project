# coding: utf-8

# # Scrape all news articles from the ABC News archives
# 
# http://www.abc.net.au/news/archive/
# 
# @author: Sam Davey 2016-09-20
# @version: 1.0

import sys
from bs4 import BeautifulSoup
import requests
import datetime
import json
import hashlib
import csv
import time

# Static variables
first_date = datetime.date(2003, 2, 19)
archive_base_url = 'http://www.abc.net.au/news/archive/'
abc_url = 'http://abc.net.au'


class ArticleLink:
    '''
    Represents an entry in ABC News's news archive article list.
    Attributes:
       title: The article title (from the link text)
       url: The URL of the linked article
       timestamp: The posting timestamp of the article
       summary: A short summary of the article
       topics: A list of topics that this article relates to
       md5: MD5 hash of the article link for duplicate checking
       raw_list_element: (optional) the raw html list element that the 
           ArticleLink was parsed from
    '''
    title = None
    url = None
    timestamp = None
    summary = None
    topics = None
    raw_list_element = None
    md5 = None
    
    
    def __init__(self, title, url, timestamp, summary, topics, raw_list_element=None):
        self.title = title
        self.url = url
        self.timestamp = timestamp
        self.summary = summary
        self.topics = topics
        self.raw_list_element = raw_list_element
        if self.url != None:
            b = bytearray()
            b.extend(map(ord, self.url))
            self.md5 = hashlib.md5(b).hexdigest()
    
    def __str__(self):
        result = (
            'Title:\t\t' + str(self.title) + '\n' +
            'URL:\t\t' + str(self.url) + '\n' +
            'Timestamp:\t' + str(self.timestamp) + '\n' +
            'Summary:\t' + str(self.summary) + '\n' +
            'MD5:\t\t' + str(self.md5) + '\n' +
            'Topics:\n'
        )
        if self.topics == None or len(self.topics) == 0:
            result = result + '\tNone\n'
        else:
            for topic in self.topics:
                result = result + '\t' + str(topic) + '\n'
        return result
    
    def __repr__(self):
        return self.md5
    
    def full_string_representation(self):
        '''
        Returns the extended string representation of the ArticleLink object.
        In addition to what is returned by str(), the full raw HTML of the
        article list item is appended to the string.
        '''
        return str(self) + 'Raw HTML:\n' + str(self.raw_list_element)
    
    def to_metadata_list(self):
        '''
        Returns the metadata elements of the ArticleLink object as a list:
        [title, url, timestamp, summary, md5]
        Does not include the topics, which are a list of their own.
        '''
        return [self.title, self.url, self.timestamp, self.summary, self.md5]
    
    def to_dict(self):
        '''
        Returns the ArticleLink object as a dictionary:
        {
         'title': title, 
         'url': url, 
         'timestamp': timestamp, 
         'summary': summary, 
         'md5': md5,
         'topics': [topics]
        }
        '''
        return {
            'title': self.title, 
            'url': self.url, 
            'timestamp': self.timestamp, 
            'summary': self.summary, 
            'md5': self.md5,
            'topics': self.topics 
        }
    
    def to_dict_with_index(self, index):
        '''
        Returns the ArticleLink object as a dictionary:
        {
         'index': index,
         'title': title, 
         'url': url, 
         'timestamp': timestamp, 
         'summary': summary, 
         'md5': md5,
         'topics': [topics]
        }
        '''
        return {
            'index': index,
            'title': self.title, 
            'url': self.url, 
            'timestamp': self.timestamp, 
            'summary': self.summary, 
            'md5': self.md5,
            'topics': self.topics 
        }
    

def make_archive_url(date, page):
    '''
    Given a date object and a page number (n), returns the url for the ABC News archive in the following format:
    http://www.abc.net.au/news/archive/yyyy,mm,dd?page=n
    
    Parameters:
    date: a date object
    page: a numeric representing the page number of the results
    '''
    dd = ('0' + str(date.day))[-2:]    # forces the day into a dd format (with leading zero if needed)
    mm = ('0' + str(date.month))[-2:]  # forces the month into an mm format (with leading zero if needed)
    yyyy = str(date.year)
    p = '?page=' + str(page)
    return archive_base_url + yyyy + ',' + mm + ',' + dd + p


def get_article_links_from_page(url):
    '''
    Given a URL of an ABC News Archive page, returns a list of ArticleLinks.
    '''
    result = []
    
    # attempt to get the URL
    try:
        get_result = requests.get(url)
        get_result.raise_for_status()
        html_response = get_result.text
    except:
        print('Error requesting the following URL:', url, '\n', sys.exc_info()[0])
        raise
    
    
    # setup the parser
    soup = BeautifulSoup(html_response, 'lxml')
    
    # get the articles. Note that every second may be a blank ()'\n').
    article_list = soup.find('ul', {'class' : 'article-index'})   
    # print('Length of article_list.contents: ', 
    #       len([a for a in article_list.contents if len(a)>1]))
    for article in article_list.contents:
        if len(article) > 1:
            # initiate the article elements as None incase we can't parse them
            tmp_title = None
            tmp_link = None
            tmp_timestamp = None
            tmp_summary = None
            tmp_topics = None
            tmp_list_elem = None
            # parse the article meta-data from the list of links
            try:
                tmp_list_elem = article
            except AttributeError:
                print('!! Could not parse raw_article:\n',
                     '   URL:', url, '\n',
                     '   HTML:', article, '\n')
            try:
                tmp_title = article.h3.text.strip()
            except AttributeError:
                print('!! Could not parse title:\n',
                     '   URL:', url, '\n',
                     '   HTML:', article, '\n')
            try:
                tmp_link = abc_url + str(article.h3.a['href'])
            except AttributeError:
                print('!! Could not parse link:\n',
                     '   URL:', url, '\n',
                     '   HTML:', article, '\n')
            try:
                tmp_timestamp = article.p.span.text
            except AttributeError:
                print('!! Could not parse timestamp:\n',
                     '   URL:', url, '\n',
                     '   HTML:', article, '\n')
            try:
                tmp_summary = article.p.next_sibling.string
            except AttributeError:
                print('!! Could not parse summary:\n',
                     '   URL:', url, '\n',
                     '   HTML:', article, '\n')
            try:
                # Many articles are not tagged with topics
                if '<strong>Topics:</strong>' in str(article):
                    tmp_topics = [tag.text for tag in 
                              article.p.next_sibling.next_element.next_element.next_element.findAll('a')]
            except AttributeError:
                print('!! Could not parse topics:\n',
                     '   URL:', url, '\n',
                     '   HTML:', article, '\n')
            # add to the resultign list of article links
            result.append(ArticleLink(
                    tmp_title, tmp_link, tmp_timestamp, tmp_summary, tmp_topics, tmp_list_elem))
    return result


def get_all_article_links_for_date(date):
    '''
    For a given date, get all ArticleLinks from ABC News Archive and return them as a
        dict using the md5 of the ArticleLink as the key and the ArticleLink itself as 
        the value.
    Parameters:
        date: A datetime.date object representing the requested date
    '''
    article_list = {} # all articles found to date; key is md5, value is article object

    # loop through all pages for a single date
    no_duplicates = True # will be set to False when the first duplicate is found
    page = 1

    while no_duplicates:
        page_articles = get_article_links_from_page(make_archive_url(date, page))
        # add any article not already seen
        # this is done because an invalid page# returns the final page rather than a 404
        for article in page_articles:
            if article.md5 in article_list:
                no_duplicates = False
                break
            else:
                # add it to the dict
                article_list[article.md5] = article
        page += 1
    return article_list


def save_article_links_to_csv(start_date, 
                              end_date, 
                              metadata_file_out, 
                              topics_file_out, 
                              index=0,
                              pause_after_day=60):
    '''
    Extract all ArticleLinks between a specified date range (inclusive) and save 
    them to two csv files: one for the metadata and one for the topics/tags.
    A unique ID (numeric) is recorded for each article, allowing the metadata and the
    topics csvs to be linked after extraction.
    Parameters:
        start_date: a datetime.date object representing the desired start date (inclusive)
        end_date: a datetime.date object representing the desired end date (inclusive).
        metadata_file_out: file name to which is written the article metadata 
            (excluding topic tags) in csv format. File will be overwritten!
        topics_file_out: file name to which is recorded the article topic tags in csv format.
             File will be overwritten!
        index: the starting id field (numeric) for the article list. Default=0
        pause_after_day: seconds to pause for after getting all articles for a single day.
            Default=60
    '''
    
    index_id = index
    metadata_output_fields = ['index', 'title', 'url', 'timestamp', 'summary', 'md5']
                
    # prepare the output files: meta_out for the metadata, topics_out for the topics
    with open(metadata_file_out, 'w', newline='') as meta_out, open(topics_file_out, 'w', newline='') as topics_out:
        meta_writer = csv.DictWriter(meta_out, 
                                     fieldnames=metadata_output_fields, 
                                     extrasaction='ignore')
        topics_writer = csv.writer(topics_out)
        # for every date in the range
        date_index = start_date
        while date_index <= end_date:
            print('Starting date:\t', date_index, flush=True)
            # get the day's ArticleLinks
            tmp_articles = get_all_article_links_for_date(date_index)
            print('   Found', len(tmp_articles), 'articles.', flush=True)
            # prepare them as dicts with the addition of an index 
            # starting from the specified index value
            articles = [article.to_dict_with_index(index_id+i) 
                        for (i, article) 
                        in enumerate(tmp_articles.values(), start=index_id)]
            # prepare the topics into a list of [index, topic] where the index
            # is repeated for each topic in the topic list for a single ArticleLink
            tmp_topics = [article['topics'] for article in articles]
            topics_rows = []
            for i in range(len(tmp_topics)):
                if tmp_topics[i] != None:
                    for j in range(len(tmp_topics[i])):
                        topics_rows.append([index_id+i, tmp_topics[i][j]])
            # write the header once only for each set
            if date_index == start_date:
                meta_writer.writeheader()
                topics_writer.writerow(['index', 'topic'])
            # write all the rows at once
            print('   Writing articles to file.', flush=True)
            meta_writer.writerows(articles)
            topics_writer.writerows(topics_rows)
            # increment the date_index the right way and pause for politeness
            date_index += datetime.timedelta(days=1)
            # increment the index_id so that the article links have a unique id
            index_id = index_id + len(articles)
            print('   Articles written to file. Pausing for politeness...', flush=True)
            time.sleep(pause_after_day)
        meta_out.close()
        topics_out.close()
        print('Complete.', flush=True)
        
    return None
