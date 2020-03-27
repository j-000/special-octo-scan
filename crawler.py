#!/usr/bin/env python3
# @author Joao Oliveira github.com/j-000

import re
import requests
import argparse
from collections import deque
from random import choices
from bs4 import BeautifulSoup

from reporter import CrawlReporter


class BasicCrawler(object):

    def __init__(self, starting_url, max_downloads, follow_accept_rules):
        self.starting_url = starting_url
        self.cap_downloads_at = max_downloads
        self.follow_accept_rules = follow_accept_rules
        self.new_urls = deque([self.starting_url])
        self.processed_urls = set()

    def __str__(self):
        return f'BasicCrawler(u={self.starting_url}, ' \
               f'md={self.cap_downloads_at}, ' \
               f'far={self.follow_accept_rules})'

    def link_approved(self, anchor):
        result = all(
          [re.match(rule, anchor) for rule in self.follow_accept_rules]
        )
        return result

    def normalize_url(self, url):
        protocol, domain = self.starting_url.split('://')
        if domain.endswith('/'):
            # remove trailing slash
            domain = domain[:-1]
        if url.startswith('//'):
            # remove one of the double slashes
            url = url[1:]
            return f'{protocol}://{domain}{url}'
        if url.startswith('/') or url.startswith('#'):
            return f'{protocol}://{domain}{url}'
        if url.endswith('/'):
            url = url[:-1]
        return url

    def process_links_on_page(self, page_html):
        parse_html = BeautifulSoup(page_html, 'html.parser')
        page_links = parse_html.find_all('a')

        for link in page_links:
            # Only links with href are valid
            if 'href' in link.attrs:
                anchor = link.attrs['href']
                # Only links that conform to
                # follow accept rule are valid
                normalized_anchor = self.normalize_url(anchor)
                if self.link_approved(normalized_anchor):
                    # Proceed if link has not been processed
                    if normalized_anchor not in self.processed_urls:
                        # Proceed if link is not already in the queue
                        # to be processed
                        if normalized_anchor not in self.new_urls:
                            self.new_urls.append(normalized_anchor)

    def run(self):
        while len(self.new_urls) and \
         len(self.processed_urls) < self.cap_downloads_at:

            print(f'new_url={len(self.new_urls)}, processed_urls={len(self.processed_urls)}')

            # Pop url from deque. URL has been normalized before being added
            url = self.new_urls.popleft()

            # Continue if url has been processed
            if url in self.processed_urls:
                continue

            html = self.fetch_html_page(url)

            # Continue if not valid content type
            if not html:
                continue

            # Process new links on new html page
            self.process_links_on_page(html)


    def fetch_html_page(self, url):

        try:
            response = requests.get(url)
            headers = response.headers
            if 'text/html' not in headers['content-type']:
                return False
            html = response.text
            self.processed_urls.add(url)
            return html
        except Exception as e:
            return False
        return False





if __name__ == '__main__':
    random_generated_file_name = ''.join(choices(
        'abcdefghijklmnopqrstuvwxyz', k=7)) + '_data.csv'

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', help='URL to scan.', type=str, required=True)
    parser.add_argument('-md', help='Max downloads.', type=int, required=True)
    parser.add_argument('-far', help='Link follow accept rules. '
                                     'Use single quotes.', nargs='+',
                        required=True)
    parser.add_argument('-fn', help='File name.', type=str,
                        default=random_generated_file_name)
    args = parser.parse_args()

    bc = BasicCrawler(starting_url=args.u,
                      max_downloads=args.md,
                      follow_accept_rules=args.far)
    bc.run()
    CrawlReporter(filename=args.fn, crawler=bc)

