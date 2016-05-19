#! /usr/bin/env python                                                            
# -*- coding:utf-8 -*-

import re

class MochaParameter :
    
    def __init__ (self) :
        self.name = ''
        self.desc = ''
    
    def set_name (self, name) :
        self.name = name
    
    def set_desc (self, desc) :
        self.desc = desc

class VariableCase :
    
    @staticmethod
    def chaincaseToCamelcase (chaincase) :
        words = chaincase.split('-')
        if len(words) == 0 :
            return ''
        camelcase = words[0]
        for word in words[1:] :
            camelcase += word[0].upper() + word[1:]
        return camelcase

    @staticmethod
    def chaincaseToUppercaseWithUnderbar (chaincase) :
        return chaincase.replace('-', '_').upper()

class AutoJcon :
    
    def __init__ (self) :
        self.html = ''
        self.parameters = []

    def read_html (self, fname='table.html') :
        if self.html != '' :
            return
        for line in open(fname, 'r') :
            self.html += line

    def parse_table (self) :
        tmp_html = self.html.replace('\n', '\t')
        for row_no, row in enumerate(AutoJcon.extract_rows(tmp_html)) :
            parameter = MochaParameter()
            for data_no, data in enumerate(AutoJcon.extract_data(row)) :
                if data_no > 1 :
                    break
                string = AutoJcon.remove_tag(data)
                if data_no == 0 :
                    parameter.set_name(AutoJcon.extract_chaincase(string))
                elif data_no == 1 :
                    split = string.split('\t')
                    parameter.set_desc(split[0] if split[0]!='' else split[1])
            if parameter.name != '' and parameter.desc != '' :
                self.parameters.append(parameter)
        self.condition_parameters()
        self.to_condition_content()
        self.search_content()

    def condition_parameters (self) :
        for parameter in self.parameters :
            camelcase = VariableCase.chaincaseToCamelcase(parameter.name)
            print '/**', parameter.desc, '*/'
            print 'private String', camelcase + ';'
            print

    def to_condition_content (self) :
        for parameter in self.parameters :
            camelcase = VariableCase.chaincaseToCamelcase(parameter.name)
            string = 'condition.set'
            string += camelcase[0].upper() + camelcase[1:]
            string += '(req.getParameter("' + parameter.name + '"));'
            print string
        print 'return condition;'
        print

    def search_content (self) :
        for p in self.parameters :
            uppercase = VariableCase.chaincaseToUppercaseWithUnderbar(p.name)
            camelcase = VariableCase.chaincaseToCamelcase(p.name)
            string = 'request.addParameter(MochaParameter.'
            string += uppercase + ', condition.get'
            string += camelcase[0].upper() + camelcase[1:]
            string += '());'
            print string
        print
    
    @staticmethod
    def extract_rows (html) :
        pattern_tr = re.compile(r'<tr.*?tr>')
        for table_row in pattern_tr.findall(html) :
            yield table_row
    
    @staticmethod
    def extract_data (table_row) :
        pattern_td = re.compile(r'(<td.*?td>)|(<div.*?div>)')
        for table_data in pattern_td.findall(table_row) :
            yield table_data[0].lstrip()
    
    @staticmethod
    def remove_tag (html) :
        pattern_tag = re.compile(r'<[^>]*?>')
        return re.sub(pattern_tag, '', html)

    @staticmethod
    def extract_chaincase (string) :
        pattern_chain = re.compile(r'[a-zA-Z\-]+')
        return pattern_chain.findall(string)[0]

if __name__ == '__main__' :
    auto_jcon = AutoJcon()
    auto_jcon.read_html(fname='table2.html')
    auto_jcon.parse_table()