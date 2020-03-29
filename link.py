#!/usr/bin/env python3
# @author Joao Oliveira github.com/j-000

import requests
from bs4 import BeautifulSoup


class LinkProcessor:

    def __init__(self, url):
        self.url = url
        self.html = None
        self.response = None
        self.metainfo = {
            'total_links_found_on_page': 0,
            'total_links_approved': 0,
            'document_size': 0,
            'headers': None,

        }
        self.exceptions = list()
        self.trawl()

    def __str__(self):
        return f'< Link(url={self.url}) >'

    def trawl(self):
        try:
            self.response = requests.get(self.url)
            if 'text/html' not in self.response.headers['content-type']:
                return
            self.html = self.response.text
        except Exception as e:
            self.exceptions.append(e)

    def find_all_links_on_page(self):
        parse_html = BeautifulSoup(self.html, 'html.parser')
        page_links = parse_html.find_all('a')
        self.metainfo.update({'total_links_found_on_page': len(page_links)})
        return page_links

    def increment_approved_links_count(self):
        self.metainfo['total_links_approved'] += 1