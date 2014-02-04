#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.find("div", id=re.compile("^companyname")).span.string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.h3.findAll("div")[0].a.string
        self.fields["company_joburl"].func = lambda doc: "http://www.healthcarejobsite.com" + doc.h3.findAll("div")[0].a["href"]
        self.fields["source_joburl"].func = lambda doc: "http://www.healthcarejobsite.com" + doc.h3.findAll("div")[0].a["href"]
        self.fields["city"].func = lambda doc: doc.find("div", id=re.compile("^companyname")).i.string
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.find("div", id=re.compile("^companyname")).i.string
        self.fields["state"].patterns = [r", (\w\w)\W", r", (\w\w)$"]
        self.fields["state"].process = lambda t: t[0].strip()
        self.fields["source"].func = lambda doc: "healthcarejobsite.com"
        self.fields["posting_date"].func = lambda doc: doc.h3.findAll("div")[1].i.string
        self.fields["posting_date"].patterns = [r"(\w\w\w) (\d\d?)"]
        self.fields["posting_date"].process = common.mmm_dd
        self.fields.update(kwargs)
        
        def nextpage(doc, page):
            x=doc.findAll("td", {'class': "paging"})[-1]
            links = doc.find("td", {'class': "paging"}).findAll("a")
            if links[-1].string=='Next':
                return "http://www.healthcarejobsite.com"+x.find('span',{'class':'currentPage'}).findNext()['href']
            return None           
        
        self.datafunc = lambda doc: doc.findAll("td", {'class': re.compile("^job_title")})
        self.url = "http://www.healthcarejobsite.com/jobs/job-search.asp?fkeywords=%s&forderby=M"
        self.nextlink = nextpage