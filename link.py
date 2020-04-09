#!/usr/bin/env python3
# @author Joao Oliveira https://github.com/j-000/special-octo-scan

import requests
from bs4 import BeautifulSoup


class LinkProcessorList:
    """
    LinkProcessorList - special list that holds <LinkProcessor> objects.
    """

    def __init__(self):
        self.processed_links_set = set()
        self.processed_urls = list()

    def __iter__(self):
        return self.processed_urls.__iter__()

    def __contains__(self, key):
        if not isinstance(key, (str, LinkProcessor)):
            raise ValueError(f'key must be type LinkProcessor or str - got {type(key)} -> {key}')
        if isinstance(key, LinkProcessor):
            return key.url in self.processed_links_set
        if isinstance(key, str):
            return key in self.processed_links_set

    def __len__(self):
        return len(self.processed_urls)

    def add(self, new_link_processor):
        if new_link_processor.url in self.processed_links_set:
            return
        self.processed_links_set.add(new_link_processor.url)
        self.processed_urls.append(new_link_processor)
        

class LinkProcessor:
    """
    <LinkProcessor> - trawls one single page based on a given URL. 
    Processes the response from the request and stores the html and 
    response as properties. There is also some metainfo collected.
    """

    def __init__(self, url):
        self.url = url
        self.html = None
        self.response = None
        self.metainfo = {
            'total_links_found_on_page': 0,
            'headers': None,
            'link_tags_found': 0,
            'script_tags_found': 0,
            'exception': None,
        }
        self.rules_checks = dict()
        self.trawl()

    def trawl(self):
        try:
            self.response = requests.get(self.url)
            self.html = self.response.text
            self.metainfo.update({'headers': self.response.headers})
        except Exception as e:
            self.metainfo.update({'exception': e})

    def get_all_hrefs_on_page(self):
        parse_html = BeautifulSoup(self.html, 'html.parser')
        # Only a tags with an href attribute are considered
        page_hrefs = [a.attrs.get('href')
                      for a in parse_html.find_all('a')
                      if 'href' in a.attrs]
        self.metainfo.update({'total_links_found_on_page': len(page_hrefs)})
        return page_hrefs
