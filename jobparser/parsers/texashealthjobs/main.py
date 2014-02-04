#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["title"].func = lambda doc: doc.find("span", {'class': "jobTitle"}).a.string
        self.fields["company_joburl"].func = lambda doc: "http://www.texashealth-jobs.org" + doc.find("span", {'class': "jobTitle"}).a["href"]
        self.fields["source_joburl"].func = lambda doc: "http://www.texashealth-jobs.org" + doc.find("span", {'class': "jobTitle"}).a["href"]
        self.fields["city"].func = lambda doc: doc.find("span", {'class': "jobLocation"}).string
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.find("span", {'class': "jobLocation"}).string
        self.fields["state"].patterns = [r", (\w\w)\W", r", (\w\w)$"]
        self.fields["state"].process = lambda t: t[0].strip()
        self.fields["source"].func = lambda doc: "texashealth-jobs.org"
        self.fields["posting_date"].func = lambda doc: "".join(doc.find("p", id="job-date").findAll(text=True))
        self.fields["posting_date"].patterns = [r"(\w\w\w) (\d\d?), (\d\d\d\d)"]
        self.fields["posting_date"].process = common.mmm_dd_yyyy
        self.fields["posting_date"].depth = 2
        self.fields.update(kwargs)
        
        self.cookie = False
        
        def nextpage(doc, page):
            links = doc.find("span", {'class': "pagination-links"}).findAll("a")
            if len(links) < page+2:
                return None
            m = re.search(r"^(.*?&q=[^&]+).*?(&startrow=.*)", "http://www.texashealth-jobs.org" + links[page]["href"])
            return "".join(m.groups())
        
        self.datafunc = lambda doc: doc.findAll("tr", {'class': re.compile("dbOutputRow")}) if doc else None
        self.url = "http://www.texashealth-jobs.org/search?q=%s"
        self.nextlink = nextpage
    
    