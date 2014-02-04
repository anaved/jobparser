#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["code"].func = lambda x: (x["pre"] or "") + " " + (x["post"] or "")
        self.fields["code"].depth = 2
        self.fields["title"].func = lambda doc: doc.p.string
        self.fields["title"].patterns = [r"\. (.*)"]
        self.fields["title"].process = lambda t: t[0].strip()
        self.fields["text"].func = lambda doc: "".join(doc.findAll("p")[1].findAll(text=True))
        self.filterfields = {"pre": CourseField.CourseField(False), "post": CourseField.CourseField(False)}
        
        def prefunc(doc):
            d = doc
            while True:
                try:
                    if d.name == 'h3': break
                except: pass
                d = d.previousSibling
            return d.string
        self.filterfields["pre"].func = prefunc
        self.filterfields["pre"].patterns = [r":(.*)"]
        self.filterfields["pre"].process = lambda t: t[0].strip()
        self.filterfields["post"].func = lambda doc: doc.p.string
        self.filterfields["post"].patterns = [r"(.*?)\."]
        self.filterfields["post"].process = lambda t: t[0].strip()
        self.fields.update(kwargs)
        
        def blow(data):
            lst = []
            for entry in data:
                en = str(entry)
                en = en.replace(str(entry.strong), "")
                s = entry.strong.string
                x = s.find(".")
                for num in s[:x].split(","):
                    new = num.strip() + s[x:]
                    soup = self.getsoup(new+en)
                    soup.previousSibling = entry.previousSibling
                    lst.append(soup)
            return lst 
        
        self.datafunc = lambda doc: blow(doc.findAll("p", {'class': "desc"}))
        self.url = "http://registrar.utexas.edu/catalogs/ug08-10/ch02/ug08.cr02.html#courses"
    
    