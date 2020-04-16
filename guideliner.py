#!/usr/bin/env python3
# @author Joao Oliveira https://github.com/j-000/special-octo-scan
import re


class Rule:
    """
    <Rule> - a regex based check. Logic depends on the type 
    of check required.
    
    types:
        A - use re.findall - returns a list of matches 
        B - use re.match - returns the first Match object if there is a match
        C - use re.search - find a match
    """
    def __init__(self, name, regex, rtype, customlogic=None):
        self.logic = customlogic
        self.name = name
        if rtype not in 'ABC':
            raise ValueError(f'Expected rtype to be A, B OR C, got {rtype}.')
        self.type = rtype
        if not isinstance(regex, str):
            raise ValueError(f'Expected regex to be type str, got {type(regex)}.')
        self.rule_regex = re.compile(regex)

    def passes(self, html):
        if self.type == 'A':
            return self.rule_regex.findall(html)
        if self.type == 'B':
            return self.rule_regex.match(html)
        if self.type == 'C':
            return self.rule_regex.search(html)



class Guideliner:

    def __init__(self, crawler, *rules):
        self.crawler = crawler
        self.rules_list = [*rules]
        self.run_checks()

    def run_checks(self):
        for rule in self.rules_list:
            for linkprocessor in self.crawler.processed_urls:
                # Only HTML pages should be checked
                if 'html' in linkprocessor.metainfo.get('headers', {}).get('content-type'):
                    linkprocessor.rules_checks.update({rule.name : '✔ Pass' if rule.passes(linkprocessor.html) else '❌ Fail' })
                else:
                    linkprocessor.rules_checks.update({rule.name : 'N/A'})
