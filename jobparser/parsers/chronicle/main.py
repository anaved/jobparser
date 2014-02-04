#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.findAll("p")[0].string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.h4.a.string
        self.fields["company_joburl"].func = lambda doc: "http://chronicle.com" + doc.h4.a["href"]
        self.fields["source_joburl"].func = lambda doc: "http://chronicle.com" + doc.h4.a["href"]
        self.fields["state"].func = lambda doc: doc.div.find("dl", {'class': None}).dd.string
        self.fields["state"].patterns = [r"(.*)"]
        self.fields["state"].process = lambda doc : doc[0]#common.shorten
        self.fields["state"].mandatory = True
        self.fields["source"].func = lambda doc: "chronicle.com"
        self.fields["posting_date"].func = lambda doc: doc.findAll("p")[1].string
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
        self.fields.update(kwargs)
        
        def nextpage(doc, page):
            links = doc.find("div", {'class': "pagination"})
            if len(links.ul.findAll("li")) >= page+1 and links.findChildren('li')[-1].findChild('a'):
                url= "http://chronicle.com/jobSearch" + links.ul.findAll("li")[page].a["href"]                
                return url
            return None
            
        
        self.datafunc = lambda doc: doc.findAll("div", {'class': "result"})
        self.url = "http://chronicle.com/jobSearch?contextId=434&facetClear=1&searchQueryString=%s&position=&location=&locationmulti[]=ODg6OjpVbml0ZWQgU3RhdGVz"
        self.nextlink = nextpage
        self.dev_mode=True
    