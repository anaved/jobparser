#!/usr/bin/env python

import time

from core.JobsiteParser import JobsiteParser
import re
from util import common

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.find("p", {'class': "title_1"}).findAll("a")[1].string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.find("p", {'class': "title_1"}).findAll("a")[0].string
        self.fields["company_joburl"].func = lambda doc: doc.find("p", {'class': "title_1"}).findAll("a")[0]["href"]
        self.fields["source_joburl"].func = lambda doc: doc.find("p", {'class': "title_1"}).findAll("a")[0]["href"]
        self.fields["city"].func = lambda doc: doc.find("p", {'class': "title_1"}).findAll("a")[2].string
        self.fields["state"].func = lambda doc: doc.find("p", {'class': "title_1"}).findAll("a")[3].string
        self.fields["source"].func = lambda doc: "amightyriver.com"
        self.fields["posting_date"].func = lambda doc: doc.find("div", {'id': "title_1"}).font.string
        self.fields["posting_date"].patterns = [r"(\d\d)-(\d\d)-(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
        self.filterfields["zipcode"].func = lambda doc: "".join(doc.find("div", text=re.compile("Location:")).parent.parent.findAll(text=True))
        self.filterfields["zipcode"].patterns = [r"(\d{5})"]
        self.filterfields["zipcode"].process = lambda t: t[0].strip()
        self.filterfields["zipcode"].depth = 2
        self.fields.update(kwargs)
        
        def nextpage(doc, page):
            links = doc.find("div", id="note_right").findAll("a")
            if len(links) < page+1 or links[-1].string=='First':
                return None
            return links[page]["href"]
        
        self.datafunc = lambda doc: doc.findAll("div", id="l_item")
        self.url = "http://www.amightyriver.com/job/search-result?sh_keyword=%s"
        self.nextlink  = nextpage
        self.dev_mode=True
