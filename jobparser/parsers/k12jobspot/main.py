#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.find("div", {'class': "jobList_Employer"}).a.string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.find("div", {'class': "jobList_Title"}).a.string
        self.fields["company_joburl"].func = lambda doc: "http://k12jobspot.com/" + doc.find("div", {'class': "jobList_Title"}).a["href"]
        self.fields["source_joburl"].func = lambda doc: "http://k12jobspot.com/" + doc.find("div", {'class': "jobList_Title"}).a["href"]
        self.fields["city"].func = lambda doc: ", ".join([a.string for a in doc.find("div", {'class': "jobList_Address"}).span.findAll("a")])
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: ", ".join([a.string for a in doc.find("div", {'class': "jobList_Address"}).span.findAll("a")])
        self.fields["state"].patterns = [r", (\w\w)\W", r", (\w\w)$"]
        self.fields["state"].process = lambda t: t[0].strip()
        self.fields["source"].func = lambda doc: "k12jobspot.com"
        self.fields["posting_date"].func = lambda doc: doc.find("div", {'class': "jobList_PostDate"}).span.string
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
        self.filterfields["zipcode"].func = lambda doc: ", ".join([a.string for a in doc.find("div", {'class': "jobList_Address"}).span.findAll("a")])
        self.filterfields["zipcode"].patterns = [r"(\d{5})"]
        self.filterfields["zipcode"].process = lambda t: t[0].strip()
        self.fields.update(kwargs)
        
        self.datafunc = lambda doc: doc.findAll("table", {'class': "jobList_Job"})
        self.url = "http://k12jobspot.com/?Keyword=%s"
        
        def nextpage(doc, page):
            x = doc.findAll("span", {'class': "pager"}).pop()
            pages=x.findAll("a")
            if pages[-1].string.startswith('Next'):
                return "http://k12jobspot.com" + x.find('b').findNext()['href']
            return None
        
        self.nextlink = nextpage
    