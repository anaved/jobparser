#!/usr/bin/env python

class ParserField:
    
    def __init__(self, mandatory=False, func=lambda doc: False, patterns=[], process=lambda t: False):
        self.mandatory = mandatory
        self.func = func
        self.patterns = patterns
        self.process = process
        self.depth = 1