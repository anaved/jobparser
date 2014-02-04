#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: "".join(doc.find("td", {'class': "resultsCompanyUrl resultsStandard"}).findAll(text=True))
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.find("a", id="results.job.title").string
        self.fields["company_joburl"].func = lambda doc: "http://jobs.pharmacyjobcenter.com" + doc.find("a", id="results.job.title")["href"]
        self.fields["source_joburl"].func = lambda doc: "http://jobs.pharmacyjobcenter.com" + doc.find("a", id="results.job.title")["href"]
        self.fields["city"].func = lambda doc: doc.find("a", id="results.job.location").string
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.find("a", id="results.job.location").string
        self.fields["state"].patterns = [r", (\w\w)\s+United States"]
        self.fields["state"].process = lambda t: t[0].strip()
        self.fields["source"].func = lambda doc: "pharmacyjobcenter.com"
        self.fields["posting_date"].func = lambda doc: doc.findAll("td")[3].string
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
        self.filterfields["zipcode"].func = lambda doc: "".join(doc.find("span", text=re.compile("Location :")).parent.parent.findAll(text=True))
        self.filterfields["zipcode"].patterns = [r"\D(\d{5})\D", r"\D(\d{5})$"]
        self.filterfields["zipcode"].process = lambda t: t[0].strip()
        self.filterfields["zipcode"].depth = 2
        self.fields.update(kwargs)
        
        self.datafunc = lambda doc: doc.findAll("tbody", {'class': re.compile("displayTableRow")})
        self.url = "http://jobs.pharmacyjobcenter.com/careers/jobsearch/results?searchType=quick;kAndTitle=%s;country=United+States;sortBy=moddate;pageSize=50"
        
    
    