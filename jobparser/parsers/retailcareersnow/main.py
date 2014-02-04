#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.find("td", {'class': "resultsCompanyUrl resultsStandard"}).string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.find("div", {'class': "jobTitle"}).a.string
        self.fields["company_joburl"].func = lambda doc: "http://jobs.retailcareersnow.com" + doc.find("div", {'class': "jobTitle"}).a["href"]
        self.fields["source_joburl"].func = lambda doc: "http://jobs.retailcareersnow.com" + doc.find("div", {'class': "jobTitle"}).a["href"]
        self.fields["city"].func = lambda doc: doc.find("a", {'id': "results.job.location"}).string
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.find("a", {'id': "results.job.location"}).string
        self.fields["state"].patterns = [r", (\w\w)\W", r", (\w\w)$"]
        self.fields["state"].process = lambda t: t[0].strip()
        self.fields["source"].func = lambda doc: "retailcareersnow.com"
        self.fields["posting_date"].func = lambda doc: doc.findAll("td", {'class': "resultsStandard"})[2].string
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
        self.fields.update(kwargs)
        
        def nextpage(doc, page):
            links = doc.find("ul", {'class': "paginationLineup"})
            if links is None or links.findAll("li").pop().a is None:
                return None
            return "http://jobs.retailcareersnow.com/careers/jobsearch/" + links.findAll("li").pop().a["href"]
        
        self.datafunc = lambda doc: doc.findAll("tbody", {'class': re.compile("^displayTableRow")})
        self.url = "http://jobs.retailcareersnow.com/careers/jobsearch/results?searchType=quick;kAndEntire=%s;country=United+States"
        self.nextlink = nextpage
    
    