#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.find("span", {'class': "Company"}).string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.h3.a.string
        self.fields["company_joburl"].func = lambda doc: "http://postjobfree.com/" + doc.h3.a["href"]
        self.fields["source_joburl"].func = lambda doc: "http://postjobfree.com/" + doc.h3.a["href"]
        self.fields["city"].func = lambda doc: doc.find("span", {'class': "Location"}).string
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.find("span", {'class': "Location"}).string
        self.fields["state"].patterns = [r", (\w\w)\W", r", (\w\w)$"]
        self.fields["state"].process = lambda t: t[0].strip()
        self.fields["source"].func = lambda doc: "postjobfree.com"
        self.fields["posting_date"].func = lambda doc: doc.find("span", {'class': "PostedDate"}).string
        self.fields["posting_date"].patterns = [r"(\w\w\w) (\d\d?)"]
        self.fields["posting_date"].process = common.mmm_dd
        self.filterfields["zipcode"].func = lambda doc: "".join(doc.find("td", text=re.compile("ZIP:")).parent.parent.findAll(text=True))
        self.filterfields["zipcode"].patterns = [r"(\d{5})"]
        self.filterfields["zipcode"].process = lambda t: t[0].strip()
        self.filterfields["zipcode"].depth = 2
        self.fields.update(kwargs)
        
        self.datafunc = lambda doc: doc.findAll("div", {'class': "JobRow"})
        self.url = "http://postjobfree.com/JobList.aspx?q=%s&n=&t=&c=&jt=&l=&radius=25&r=50&lat=&lng=&lct=&lc=&ls=&lz=&accuracy=&address="
    