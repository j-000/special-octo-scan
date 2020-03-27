#!/usr/bin/env python3
# @author Joao Oliveira github.com/j-000

import datetime
import random

import xlsxwriter


class CrawlReporter:

    def __init__(self, crawler):
        self.filename = self.set_filename()
        self.crawler = crawler
        self.workbook = xlsxwriter.Workbook(filename=self.filename)
        self.col = 0
        self.row = 0
        self.main()

    def main(self):
        self.write_file_info()
        self.workbook.close()

    def write_to_file(self, data_array, worksheet, write_null=False,
                      row_style=None, reset=False, custom=False):
        if reset:
            self.row = 0
            self.col = 0
        if custom:
            self.row = custom[0]
            self.col = custom[1]
        for data_row in data_array:
            for i in range(len(data_row)):
                if write_null:
                    if not data_row[i]:
                        data_row[i] = 0
                worksheet.write(self.row, self.col + i, data_row[i], row_style)
            self.row += 1

    def set_filename(self):
        filename = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=7))
        filename += '_data.xlsx'
        return filename

    def write_file_info(self):
        bold = self.workbook.add_format({'bold': True})
        worksheet_1 = self.workbook.add_worksheet(name='Page Inventory')
        worksheet_1.hide_gridlines(2)
        info_headers = [[f'Generated on {datetime.datetime.now()}']]
        self.write_to_file(worksheet=worksheet_1, data_array=info_headers,
                           row_style=bold)

        data_headers = [['URL', 'Status Code']]
        self.write_to_file(worksheet=worksheet_1, data_array=data_headers,
                           custom=(0, 4), row_style=bold)

        urls_col = [[url] for url in self.crawler.processed_urls]
        self.write_to_file(worksheet=worksheet_1, data_array=urls_col,
                           custom=(0, 5))


    def compile_report(self):
        pass