#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.tr.findAll("td", recursive=False)[4].a.string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.tr.findAll("td", recursive=False)[1].a.string
        self.fields["company_joburl"].func = lambda doc: "http://careers.nwjobs.com" + doc.tr.findAll("td", recursive=False)[1].a["href"]
        self.fields["source_joburl"].func = lambda doc: "http://careers.nwjobs.com" + doc.tr.findAll("td", recursive=False)[1].a["href"]
        self.fields["city"].func = lambda doc: doc.tr.findAll("td", recursive=False)[2].a.string
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.tr.findAll("td", recursive=False)[2].a.string
        self.fields["state"].patterns = [r", (.*?)\s+\d", r", ([^,/]*)$"]
        self.fields["state"].process = common.shorten
        self.fields["source"].func = lambda doc: "nwjobs.com"
        self.fields["posting_date"].func = lambda doc: doc.tr.findAll("td", recursive=False)[3].string
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
        self.filterfields["zipcode"].func = lambda doc: doc.tr.findAll("td", recursive=False)[2].a.string
        self.filterfields["zipcode"].patterns = [r"(\d{5})"]
        self.filterfields["zipcode"].process = lambda t: t[0].strip()
        self.fields.update(kwargs)
        
        self.datafunc = lambda doc: doc.findAll("tbody", {'class': re.compile("displayTableRow")})
        self.url = "http://careers.nwjobs.com/careers/jobsearch/results?kAndEntire=%s;pageSize=50;sortBy=moddate"
    