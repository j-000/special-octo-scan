#!/usr/bin/env python3
# @author Joao Oliveira https://github.com/j-000/special-octo-scan

import requests
from bs4 import BeautifulSoup


class LinkProcessor:

    def __init__(self, url):
        self.url = url
        self.html = None
        self.response = None
        self.metainfo = {
            'total_links_found_on_page': 0,
            'headers': None,
        }
        self.exceptions = list()
        self.trawl()

    def trawl(self):
        try:
            self.response = requests.get(self.url)
            if 'text/html' not in self.response.headers['content-type']:
                return
            self.html = self.response.text
            self.metainfo.update({'headers': self.response.headers})
        except Exception as e:
            self.exceptions.append(e)

    def get_all_hrefs_on_page(self):
        parse_html = BeautifulSoup(self.html, 'html.parser')
        # Only links with an href attribute are considered
        page_hrefs = [a.attrs.get('href')
                      for a in parse_html.find_all('a')
                      if 'href' in a.attrs]
        self.metainfo.update({'total_links_found_on_page': len(page_hrefs)})
        return page_hrefs
