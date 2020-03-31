#!/usr/bin/env python3
# @author Joao Oliveira https://github.com/j-000/special-octo-scan

import datetime
import random

import xlsxwriter


def generate_random_filename():
    random_characters = random.choices('abcdefghijklmnopqrstuvwxyz', k=7)
    random_part = ''.join(random_characters)
    filename = f'octoscan_{random_part}_data.xlsx'
    return filename


class CrawlReporter:

    def __init__(self, crawler):
        self.filename = generate_random_filename()
        self.crawler = crawler
        self.workbook = xlsxwriter.Workbook(filename=self.filename)
        self.worksheets = dict()
        self.styles = dict(bold=self.workbook.add_format({'bold': True}))
        self.col = 0
        self.row = 0
        self.main()

    def main(self):
        self.write_worksheet_1()
        self.write_worksheet_2()
        self.workbook.close()

    def write_to_file(self, data_array, worksheet, write_null=False,
                      row_style=None, reset=False, custom=None):
        if reset:
            self.row = 0
            self.col = 0
        if custom:
            self.row = custom[0]
            self.col = custom[1]
        for data_row in data_array:
            for i, p in enumerate(data_row):
                if write_null:
                    if not p:
                        p = 0
                worksheet.write(self.row, self.col + i, p, row_style)
            self.row += 1

    def add_worksheet(self, name):
        next_number = len(self.worksheets) + 1
        self.worksheets.update(
            {
                f'worksheet_{next_number}':
                self.workbook.add_worksheet(name=name)
            }
        )

    def write_worksheet_1(self):
        self.add_worksheet('Page Inventory')
        worksheet_1 = self.worksheets.get('worksheet_1')
        worksheet_1.hide_gridlines(2)
        info_headers = [
            [f'Generated on {datetime.date.today()} '
             f'by OctoScan https://github.com/j-000/special-octo-scan']
        ]
        self.write_to_file(worksheet=worksheet_1, data_array=info_headers,
                           row_style=self.styles.get('bold'))

        data_headers = [['URL',
                         'Status Code',
                         'Total links found on page',
                         'Content-Type']]
        self.write_to_file(worksheet=worksheet_1, data_array=data_headers,
                           custom=(4, 0), row_style=self.styles.get('bold'))

        urls_col = [[link.url,
                     link.response.status_code,
                     link.metainfo.get('total_links_found_on_page', 'None'),
                     link.metainfo.get('headers', {}).get(
                         'content-type', 'None')]
                    for link in self.crawler.processed_urls]

        self.write_to_file(worksheet=worksheet_1, data_array=urls_col,
                           custom=(5, 0))

    def write_worksheet_2(self):
        self.add_worksheet('Other Assets')
        worksheet_2 = self.worksheets.get('worksheet_2')
