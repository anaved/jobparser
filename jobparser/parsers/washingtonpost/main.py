#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.find("td", {'class': "sh_company "}).a.string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: "".join(doc.h3.a.findAll(text=True))
        self.fields["company_joburl"].func = lambda doc: doc.h3.a["href"]
        self.fields["source_joburl"].func = lambda doc: doc.h3.a["href"]
        self.fields["city"].func = lambda doc: doc.find("td", {'class': "sh_location "}).string
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.find("td", {'class': "sh_location "}).string
        self.fields["state"].patterns = [r", (\w\w)\W", r", (\w\w)$"]
        self.fields["state"].process = lambda t: t[0].strip()
        self.fields["source"].func = lambda doc: "washingtonpost.com"
        self.fields["posting_date"].func = lambda doc: doc.find("td", {'class': "sh_posted "}).string
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)"]
        self.fields["posting_date"].process = common.mm_dd
        self.fields.update(kwargs)
        
        self.datafunc = lambda doc: doc.findAll("tr", {'class': "sh_listing"})[::2]
        self.url = "http://nationaljobs.washingtonpost.com/a/all-jobs/list/q-%s/sb-pd"
        self.nextlink = lambda doc, page: "http://nationaljobs.washingtonpost.com" + doc.find("span", {'class': "sh_current"}).nextSibling.nextSibling["href"]
        self.sleeptime = 2
    