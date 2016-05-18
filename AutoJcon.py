#! /usr/bin/env python
# -*- coding:utf-8 -*-

class AutoJcon :
    
    def __init__ (self) :
        pass

    def read_html (self, fname='table.html') :
        for line in open(fname, 'r') :
            print line,

if __name__ == '__main__' :
    auto_jcon = AutoJcon()
    auto_jcon.read_html()
