#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.findAll("td")[3].p.string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: "".join(doc.find("a", {'class': "colour"}).parent.findAll(text=True))
        self.fields["company_joburl"].func = lambda doc: "http://www.hirediversity.com/jobseekers/jobs/" + doc.find("a", {'class': "colour"})["href"]
        self.fields["source_joburl"].func = lambda doc: "http://www.hirediversity.com/jobseekers/jobs/" + doc.find("a", {'class': "colour"})["href"]
        self.fields["city"].func = lambda doc: doc.findAll("td")[4].p.string
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.findAll("td")[4].p.string
        self.fields["state"].patterns = [r", (\w\w)\W", r", (\w\w)$"]
        self.fields["state"].process = lambda t: t[0].strip()
        self.fields["source"].func = lambda doc: "hirediversity.com"
        self.fields["posting_date"].func = lambda doc: doc.findAll("td")[6].p.string
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
        self.fields.update(kwargs)
        
        def nextpage(doc, page):
            links = doc.find("div", {'class': "text"}).h3.findAll("a")
            if len(links) < page:
                return None
            return "http://www.hirediversity.com/jobseekers/jobs/" + links[page-1]["href"]
        
        self.datafunc = lambda doc: doc.find("div", {'class': "content"}).table.findAll("tr")[1:] if doc else None
        self.url = "http://www.hirediversity.com/jobseekers/jobs/list.asp?quicksearch=yes&ambiguouslocation=City%2C+State&zipcode=ZipCode&industryids=&keywords=%s&Search.x=57&Search.y=10"
        self.nextlink = nextpage
        self.dev_mode=True