#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: "".join(doc.findAll("td")[-2].findAll(text=True))
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.findAll("td")[3].a.string
        self.fields["company_joburl"].func = lambda doc: "http://www.hcareers.com" + doc.findAll("td")[3].a["href"]
        self.fields["source_joburl"].func = lambda doc: "http://www.hcareers.com" + doc.findAll("td")[3].a["href"]
        self.fields["city"].func = lambda doc: doc.findAll("td")[2].string
        self.fields["city"].patterns = [r"-([^-]*)$"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.findAll("td")[2].string
        self.fields["state"].patterns = [r"\W(\w\w)\W"]
        self.fields["state"].process = lambda t: t[0].strip()
        self.fields["source"].func = lambda doc: "hcareers.com"
        self.fields["posting_date"].func = lambda doc: doc.findAll("td")[0].string
        self.fields["posting_date"].patterns = [r"(\w\w\w) (\d\d?), (\d\d\d\d)"]
        self.fields["posting_date"].process = common.mmm_dd_yyyy
        self.fields.update(kwargs)
        
        def nextpage(doc, page):
            link = doc.find("div", {'class': "search-results-nav"}).a
            if link is None:
                return None
            return "http://www.hcareers.com" + link["href"]
        
        self.datafunc = lambda doc: doc.find("table", id="table1").findAll("tr")[1:]
        self.url = "http://www.hcareers.com/seeker/search/advanced?jobDetectiveId=&booleanKeyWordSearch=%s&industryCodes=&management=&managementCheckbox=on&nonmanagementCheckbox=on&form.commit=Search&h_v=XG_20071127_1"
        self.nextlink = nextpage
        self.dev_mode=True