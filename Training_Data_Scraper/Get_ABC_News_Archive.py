# coding: utf-8

import ABC_News_Archive_Scraper
import datetime

ABC_News_Archive_Scraper.save_article_links_to_csv(datetime.date(2003,2,19),
                          datetime.date.today(),
                          'entire_archive_meta_out.csv',
                          'entire_archive_topics_out.csv')
