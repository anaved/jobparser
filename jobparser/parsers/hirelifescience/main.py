#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: "".join(doc.findAll("td")[0].findAll(text=True))
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.findAll("td")[4].b.a.string
        self.fields["company_joburl"].func = lambda doc: "http://hirelifescience.com/" + doc.findAll("td")[4].b.a["href"]
        self.fields["source_joburl"].func = lambda doc: "http://hirelifescience.com/" + doc.findAll("td")[4].b.a["href"]
        self.fields["city"].func = lambda doc: doc.findAll("td")[1].string
        self.fields["state"].func = lambda doc: doc.findAll("td")[2].string
        self.fields["source"].func = lambda doc: "hirelifescience.com"
        self.fields["posting_date"].func = lambda doc: doc.findAll("td")[3].string
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
        self.fields.update(kwargs)
        
        def getall(doc):
            trs = doc.find("div", {'class': "indent"}).div.findAll("table")[1].findAll("tr")[2:-1]
            for i in range(0, len(trs)-1, 3):
                trs[i].append(trs[i+1])
            return trs[::3]
        
        self.datafunc = getall

        def nextpage(doc, page):
            trs = doc.find("div", {'class': "indent"}).div.findAll("table")[1].findAll("tr")[0]
            links = trs.findAll("a")
            if len(links) < page:
                return None
            return "http://hirelifescience.com/" + links[page-1]["href"]

        self.nextlink = nextpage
        self.url = "http://hirelifescience.com/seeker_jobs.asp?search=yes&page=&keyword=%s&pagesize=500&updown=&orderby=date"
    