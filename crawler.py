#!/usr/bin/env python3
# @author Joao Oliveira https://github.com/j-000/special-octo-scan

import re
import argparse
from collections import deque

import tqdm

from reporter import CrawlReporter
from link import LinkProcessor, LinkProcessorList


class BasicCrawler:

    def __init__(self, starting_url, max_downloads, follow_accept_rules):
        self.starting_url = starting_url
        self.cap_downloads_at = max_downloads
        self.follow_accept_rules = follow_accept_rules
        self.new_urls = deque([self.starting_url])
        self.processed_urls = LinkProcessorList()
        self.run()

    def href_approved(self, anchor):
        result = all(
          [re.match(rule, anchor) for rule in self.follow_accept_rules]
        )
        return result

    def normalize_url(self, url):
        protocol, domain = self.starting_url.split('://')
        if domain.endswith('/'):
            # remove trailing slash
            domain = domain[:-1]
        if len(url) == 1:
            return self.starting_url
        if url.startswith('//'):
            # remove one of the double slashes
            url = url[1:]
            return f'{protocol}://{domain}{url}'
        if url.startswith('/') or url.startswith('#'):
            return f'{protocol}://{domain}{url}'
        if url.endswith('/'):
            return url[:-1]
        return url

    def run(self):
        progress_bar = tqdm.tqdm(total=self.cap_downloads_at)
        while len(self.new_urls) \
                and len(self.processed_urls) < self.cap_downloads_at:
            # Update progress bar
            progress_bar.update(1)

            # Pop href from deque. href has been normalized before being added
            # also, href is assured not to have been processed before.
            url = self.new_urls.popleft()

            # Create processed link object
            link_processor = LinkProcessor(url)

            # Add link object to processed_urls list
            self.processed_urls.add(link_processor)

            # Skip if not valid content type
            if not link_processor.html:
                continue

            # Loop all <a> href found on page
            for href in link_processor.get_all_hrefs_on_page():
                # Normalize href
                normalized_href = self.normalize_url(href)
                # Proceed if the href conforms to follow accept rules
                if self.href_approved(normalized_href):
                    # Proceed if href has not been processed
                    if normalized_href not in self.processed_urls:
                        # Proceed if href is not already in the queue
                        if normalized_href not in self.new_urls:
                            # Add this new href to queue to be processed
                            self.new_urls.append(normalized_href)
        # Close progress bar
        progress_bar.close()


if __name__ == '__main__':
    help_info = '''
     ██████╗  ██████╗████████╗ ██████╗     ███████╗ ██████╗ █████╗ ███╗   ██╗
    ██╔═══██╗██╔════╝╚══██╔══╝██╔═══██╗    ██╔════╝██╔════╝██╔══██╗████╗  ██║
    ██║   ██║██║        ██║   ██║   ██║    ███████╗██║     ███████║██╔██╗ ██║
    ██║   ██║██║        ██║   ██║   ██║    ╚════██║██║     ██╔══██║██║╚██╗██║
    ╚██████╔╝╚██████╗   ██║   ╚██████╔╝    ███████║╚██████╗██║  ██║██║ ╚████║
     ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝     ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝

    [-h]     For help
    [-u]     URL to scan
    [-md]    Max downloads. Default 1000.
    [-far]   Link follow accept rules. Use single quotes.

    Example:
    ~:$ python crawler.py -u https://www.comandscan.com -md 5000 -far \
'(?si)https://www.commandscan.com.*'
    ~:$ 100%|████████████████████████████████████████| 5000/5000 \
[05:00<05:00, 30954.27it/s]

    More info @ https://github.com/j-000/special-octo-scan
    '''
    print(help_info, '\n')
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', help='URL to scan.', type=str, required=True)
    parser.add_argument('-md', help='Max downloads. Default 1000', type=int,
                        default=1000)
    parser.add_argument('-far', help='Link follow accept rules. '
                                     'Use single quotes.',
                        nargs='+', required=True)
    args = parser.parse_args()
    bc = BasicCrawler(
        starting_url=args.u,
        max_downloads=args.md,
        follow_accept_rules=args.far
    )
    CrawlReporter(crawler=bc)
