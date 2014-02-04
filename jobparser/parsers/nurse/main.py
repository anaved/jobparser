#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.findAll("td")[3].strong.a.string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.findAll("td")[1].strong.a.string
        self.fields["company_joburl"].func = lambda doc: "http://www.nurse.com" + doc.findAll("td")[1].strong.a["href"]
        self.fields["source_joburl"].func = lambda doc: "http://www.nurse.com" + doc.findAll("td")[1].strong.a["href"]
        self.fields["city"].func = lambda doc: doc.findAll("td")[2].string
        self.fields["city"].patterns = [r"^.*?-(.*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.findAll("td")[2].string
        self.fields["state"].patterns = [r"^(\w\w)\W"]
        self.fields["state"].process = lambda t: t[0].strip()
        self.fields["source"].func = lambda doc: "nurse.com"
        self.fields["posting_date"].func = lambda doc: doc.findAll("td")[0].string
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yy
        self.fields.update(kwargs)
        
        self.cookie = False
        
        self.datafunc = lambda doc: doc.find("table", id="results").tbody.findAll("tr")
        self.url = "http://www.nurse.com/jobs/search_result.cfm?keywords=%s"
        
    
    