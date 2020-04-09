#!/usr/bin/env python3
# @author Joao Oliveira https://github.com/j-000/special-octo-scan

import requests
from bs4 import BeautifulSoup


class LinkProcessorList:

    def __init__(self):
        self.processed_links_set = set()
        self.processed_urls = list()

    def __contains__(self, key):
        if not isinstance(key, LinkProcessor):
            raise ValueError('key must be type LinkProcessor')
        return key.url in self.processed_links_set

    def add(self, new_link_processor):
        if new_link_processor.url in self.processed_links_set:
            return
        self.processed_links_set.add(new_link_processor.url)
        self.processed_urls.append(new_link_processor)
        

class LinkProcessor:

    def __init__(self, url):
        self.url = url
        self.html = None
        self.response = None
        self.metainfo = {
            'total_links_found_on_page': 0,
            'headers': None,
            'link_tags_found': 0,
            'script_tags_found': 0
        }
        self.exceptions = list()
        self.trawl()

    def trawl(self):
        try:
            self.response = requests.get(self.url)
            self.html = self.response.text
            self.metainfo.update({'headers': self.response.headers})
        except Exception as e:
            self.exceptions.append(e)

    def get_all_hrefs_on_page(self):
        parse_html = BeautifulSoup(self.html, 'html.parser')
        # Only a tags with an href attribute are considered
        page_hrefs = [a.attrs.get('href')
                      for a in parse_html.find_all('a')
                      if 'href' in a.attrs]
        self.metainfo.update({'total_links_found_on_page': len(page_hrefs)})
        return page_hrefs

    def get_all_links_on_page(self):
        parse_html = BeautifulSoup(self.html, 'html.parser')
        link_tags = parse_html.find_all('link')
        self.metainfo.update({'link_tags_found': len(link_tags)})
        valid_link_tags_hrefs = [link.attrs.get('href') for link in link_tags
                                 if link.has_attr('href')]
        return valid_link_tags_hrefs

    def get_all_scripts_on_page(self):
        parse_html = BeautifulSoup(self.html, 'html.parser')
        script_tags = parse_html.find_all('script')
        self.metainfo.update({'script_tags_found': len(script_tags)})
        valid_script_tags_srcs = [script.attrs.get('src') for script
                                   in script_tags
                                   if script.has_attr('src')]
        return valid_script_tags_srcs
