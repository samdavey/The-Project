import feedparser
import Article
import warnings
import time

class Feed:
	"""
	Feed is a representation of an RSS feed.

	Attributes:
		name:			The string name of the feed.
		link:			The URL for the feed.
		accessed_date:	Timestamp for when this instance of the feed was accessed.
		articles:		List of Article objects.
	"""
	def __init__(self, feed_url, article_limit):
		# populate the link
		self.link = feed_url
		# parse the feed, giving us the 'feed' attributes and the 'entries'
		p = feedparser.parse(feed_url)
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
 
	def __repr__(self):
		s = ''
		for item in self.articles:
			s = s + str(item) + '\n'

		return ('Feed(\n' + \
			'    link          : {0}\n' + \
			'    name          : {1}\n' + \
			'    accessed_date : {2}\n' + \
			'    articles      :\n' + \
			'    [\n' + \
			'    {3}' + \
			'    ]\n' + \
			')').format(self.link, self.name, time.strftime('%Y-%m-%dT%H:%M:%SZ', self.accessed_date), s)

	def __str__(self):
		a = ''
		for item in self.articles:
			a = a + item.to_string_without_html() + '\n'

		return ('Feed:\n' + \
			'    link          : {0}\n' + \
			'    name          : {1}\n' + \
			'    accessed_date : {2}\n' + \
			'    articles      :\n' + \
			'    [\n' + \
			'    ' + a + '\n' + \
			'    ]\n' + \
			')').format(self.link, self.name, time.strftime('%Y-%m-%dT%H:%M:%SZ', self.accessed_date))
