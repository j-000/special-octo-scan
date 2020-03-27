#!/usr/bin/env python3
# @author Joao Oliveira github.com/j-000

import re
import argparse
from collections import deque

import tqdm

from reporter import CrawlReporter
from link import LinkProcessor


class BasicCrawler:

    def __init__(self, starting_url, max_downloads, follow_accept_rules):
        self.starting_url = starting_url
        self.cap_downloads_at = max_downloads
        self.follow_accept_rules = follow_accept_rules
        self.new_urls = deque([self.starting_url])
        self.processed_urls = list()

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
            return url[:-1]
        return url

    def process_links_on_page(self, processed_link):
        for link in processed_link.find_all_links_on_page():
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
                            processed_link.increment_approved_links_count()

    def run(self):
        pbar = tqdm.tqdm(total=self.cap_downloads_at)
        while len(self.new_urls) \
                and len(self.processed_urls) < self.cap_downloads_at:
            # Update progress bar
            pbar.update(1)
            # Pop url from deque. URL has been normalized before being added
            url = self.new_urls.popleft()
            # Continue if url has been processed
            if url in self.processed_urls:
                continue
            processed_link = self.create_link_processor(url)
            # Continue if not valid content type
            if not processed_link.html:
                continue
            # Process new links on new processed_link page
            self.process_links_on_page(processed_link)
        # Close progress bar
        pbar.close()

    def create_link_processor(self, url):
        new_link = LinkProcessor(url)
        self.processed_urls.append(new_link)
        return new_link


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', help='URL to scan.',
                        type=str, required=True)

    parser.add_argument('-md', help='Max downloads. Default 1000',
                        type=int, default=1000)

    parser.add_argument('-far', help='Link follow accept rules. '
                                     'Use single quotes.',
                        nargs='+', required=True)
    args = parser.parse_args()
    bc = BasicCrawler(starting_url=args.u,
                      max_downloads=args.md,
                      follow_accept_rules=args.far)
    bc.run()
    CrawlReporter(crawler=bc)
