#!/usr/bin/env python3
# @author Joao Oliveira github.com/j-000

import unittest
from collections import Counter

import requests

from crawler import BasicCrawler


follow_accept_rules = [r'(?si)https://www\.sapo\.pt.*?']
starting_url = 'https://www.sapo.pt'
max_downloads = 10


class TestBasicCrawler(unittest.TestCase):

    def setUp(self) -> None:
        self.crawler = BasicCrawler(starting_url,
                                    max_downloads,
                                    follow_accept_rules)

    def tearDown(self) -> None:
        pass

    def test_initialise_crawler(self):
        self.assertEqual(self.crawler.follow_accept_rules, follow_accept_rules)
        self.assertEqual(self.crawler.cap_downloads_at, max_downloads)
        self.assertEqual(self.crawler.starting_url, starting_url)
        self.assertEqual(len(self.crawler.new_urls), 1)
        self.assertEqual(len(self.crawler.processed_urls), 0)

    def test_link_approved_method(self):
        acceptable_link = 'https://www.sapo.pt/something'
        unacceptable_link = 'https://www.sapo-visao.pt/'
        al_method_result = self.crawler.link_approved(acceptable_link)
        ul_method_result = self.crawler.link_approved(unacceptable_link)
        self.assertTrue(al_method_result)
        self.assertFalse(ul_method_result)

    def test_process_links_on_page_method(self):
        html = '''<html>
        <head></head>
        <body>
            <h1>Fake Page</h1>
            <a href="https://www.sapo.pt/this-link-should-be-included">
            Include me</a>
            <a href="https://www.frog.pt/this-link-should-not-be-included">
            Exclude me</a>            
            <a href="">Exclude me coz I am empty</a>
            <a>Exclude me coz href?</a>
            <a href="https://www.sapo.pt/this-link-should-be-included">
            Do not include me coz I am repeated</a>
        </body>
        </html>'''
        self.crawler.process_links_on_page(html)
        self.assertIn('https://www.sapo.pt/this-link-should-be-included',
                      self.crawler.new_urls)
        # Each url should not have duplicates
        new_urls_counter = Counter(self.crawler.new_urls).values()
        # Assert all urls have a max frequency of 1
        self.assertTrue(
            all([i == 1 for i in new_urls_counter])
        )
        self.assertNotIn(
            'https://www.frog.pt/this-link-should-not-be-included',
            self.crawler.new_urls)
        self.assertNotIn('', self.crawler.new_urls)

    def test_fetch_html_page_method(self):
        valid_html_url = 'https://palletsprojects.com/p/flask/'
        asset_url = 'https://palletsprojects.com/static/styles.css?h=8f5826ef'
        html = self.crawler.fetch_html_page(valid_html_url)
        expected_html = requests.get(valid_html_url).text
        self.assertEqual(self.crawler.fetch_html_page(valid_html_url), expected_html)
        response = self.crawler.fetch_html_page(asset_url)
        self.assertFalse(response)

    def test_normalize_url_method(self):
        no_changes_url = 'https://www.sapo.pt'
        double_slashed = '//double-slashed-link'
        single_slashed = '/this-is-single-slashed'
        hashed_url = '#noticias'
        slash_at_the_end = 'https://www.sapo.pt/'
        self.assertEqual(
            self.crawler.normalize_url(no_changes_url),
            no_changes_url
        )
        self.assertEqual(
            self.crawler.normalize_url(double_slashed),
            'https://www.sapo.pt/double-slashed-link'
        )
        self.assertEqual(
            self.crawler.normalize_url(single_slashed),
            'https://www.sapo.pt/this-is-single-slashed'
        )
        self.assertEqual(
            self.crawler.normalize_url(hashed_url),
            'https://www.sapo.pt#noticias'
        )
        self.assertEqual(
            self.crawler.normalize_url(slash_at_the_end),
            'https://www.sapo.pt'
        )

    def test_run_method(self):
        self.crawler.run()
        # After the scan, processed_urls count should not be greater
        # than max_downloads + 1
        self.assertLessEqual(
            len(self.crawler.processed_urls), max_downloads)


if __name__ == '__main__':
    unittest.main()
