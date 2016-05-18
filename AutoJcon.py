#! /usr/bin/env python
# -*- coding:utf-8 -*-

import re

class AutoJcon :
    
    def __init__ (self) :
        self.html = ''

    def read_html (self, fname='table.html') :
        if self.html != '' :
            return
        for line in open(fname, 'r') :
            self.html += line

    def parse_table (self) :
        tmp_html = self.html.replace('\n', '')
        print tmp_html
        pattern_tr = re.compile(r"<tr.*?tr>");
        for match_string in pattern_tr.findall(tmp_html) :
            print 'matches', match_string
            print

if __name__ == '__main__' :
    auto_jcon = AutoJcon()
    auto_jcon.read_html()
    print auto_jcon.html
    auto_jcon.parse_table()

