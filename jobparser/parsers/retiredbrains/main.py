#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.findAll("div", {'class': "jt_jobs_company"}).pop().a.string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.find("div", {'class': "jt_jobs_title"}).string
        self.fields["company_joburl"].func = lambda doc: "http://retirementjobs.retiredbrains.com" + doc.find("div", {'class': "jt_jobs_title"}).parent["href"]
        self.fields["source_joburl"].func = lambda doc: "http://retirementjobs.retiredbrains.com" + doc.find("div", {'class': "jt_jobs_title"}).parent["href"]
        self.fields["city"].func = lambda doc: doc.find("td", {'class': "jt_jobs_location"}).a.string
        self.fields["city"].patterns = [r"^([^,]{3,})"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.find("td", {'class': "jt_jobs_location"}).a.string
        self.fields["state"].patterns = [r"\W+(\w\w)\W", r"\W+(\w\w)$", r"^(\w\w)\W", r"^(\w\w)$"]
        self.fields["state"].process = lambda t: t[0].strip()
        self.fields["source"].func = lambda doc: "retiredbrains.com"
        self.fields["posting_date"].func = lambda doc: doc.find("td", {'class': "jt_jobs_date"}).a.string
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
        self.filterfields["zipcode"].func = lambda doc: "".join(doc.find("th", text=re.compile("Location")).parent.parent.findAll(text=True))
        self.filterfields["zipcode"].patterns = [r"(\d{5})"]
        self.filterfields["zipcode"].process = lambda t: t[0].strip()
        self.filterfields["zipcode"].depth = 2
        self.fields.update(kwargs)
        
        self.cookie = False
        
        self.datafunc = lambda doc: doc.findAll("tr", id=re.compile("^jt_jobrow_\d+$"))
        self.url = "http://retirementjobs.retiredbrains.com/c/search_results.cfm?site_id=9182&vnet=0&max=50&keywords=%s&search=Search"
    