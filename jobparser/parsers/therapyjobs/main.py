#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["title"].func = lambda doc: doc.div.a.string
        self.fields["company_joburl"].func = lambda doc: "http://www.therapyjobs.com" + doc.div.a["href"]
        self.fields["source_joburl"].func = lambda doc: "http://www.therapyjobs.com" + doc.div.a["href"]
        self.fields["city"].func = lambda doc: doc.findAll("div", recursive=False)[2].findAll("span").pop().string
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.findAll("div", recursive=False)[2].findAll("span").pop().string
        self.fields["state"].patterns = [r", (.*?)\s+\d", r", ([^,/]*)$"]
        self.fields["state"].process = common.shorten
        self.fields["source"].func = lambda doc: "therapyjobs.com"
        self.fields["posting_date"].func = lambda doc: doc.findAll("div", recursive=False).pop().span.string
        self.fields["posting_date"].patterns = [r"(\w\w\w) (\d\d?), (\d\d\d\d)", r"()\d+ hours? ago"]
        self.fields["posting_date"].process = common.mmm_dd_yyyy
        self.filterfields["zipcode"].func = lambda doc: doc.findAll("div", recursive=False)[2].findAll("span").pop().string
        self.filterfields["zipcode"].patterns = [r"(\d{5})"]
        self.filterfields["zipcode"].process = lambda t: t[0].strip()
        self.fields.update(kwargs)
        
        self.datafunc = lambda doc: doc.findAll("div", {'class': "detailcell"})
        self.url = "http://www.therapyjobs.com/Results.aspx?srch=%s&rpp=50"
    