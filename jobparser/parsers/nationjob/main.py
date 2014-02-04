#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.findAll("td")[1].a.string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.findAll("td")[0].a.string
        self.fields["company_joburl"].func = lambda doc: "http://nationjob.com" + doc.findAll("td")[0].a["href"]
        self.fields["source_joburl"].func = lambda doc: "http://nationjob.com" + doc.findAll("td")[0].a["href"]
        self.fields["city"].func = lambda doc: doc.findAll("td")[2].a.string
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.findAll("td")[2].a.string
        self.fields["state"].patterns = [r", (\w\w)\W", r", (\w\w)$", r", ([^/]*)$"]
        self.fields["state"].process = common.shorten
        self.fields["source"].func = lambda doc: "nationjob.com"
        self.fields["posting_date"].func = datetime.datetime.now()
        self.fields.update(kwargs)
        
        self.cookie = False
        
        def getall(doc):
            x = doc.findAll("tr", {'class': "row1"})
            x.extend(doc.findAll("tr", {'class': "row2"}))
            return x
        
        self.datafunc = getall
        self.url = "http://nationjob.com/jobsearch/?keywords=%s&searchnow=1&pos=NA&STATE=&ZIP=zipcode&radius=25&go=Search+Jobs"
    