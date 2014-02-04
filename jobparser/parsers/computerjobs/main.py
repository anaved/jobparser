#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.find("span", id=re.compile("spanCompanyName")).string
        self.fields["company_name"].depth = 2
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["company_id"].depth = 2
        self.fields["title"].func = lambda doc: doc.find("a", id=re.compile("lnkTitle")).string
        self.fields["company_joburl"].func = lambda doc: "http://computerjobs.com" + doc.find("a", id=re.compile("lnkTitle"))["href"]
        self.fields["source_joburl"].func = lambda doc: "http://computerjobs.com" + doc.find("a", id=re.compile("lnkTitle"))["href"]
        self.fields["company_joburl"].patterns = [r"^(.*?)&searchid"]
        self.fields["source_joburl"].patterns = [r"^(.*?)&searchid"]
        self.fields["company_joburl"].process = lambda t: t[0].strip()
        self.fields["source_joburl"].process = lambda t: t[0].strip()
        self.fields["city"].func = lambda doc: doc.find("span", id=re.compile("spanLocation")).string
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.find("span", id=re.compile("spanLocation")).string
        self.fields["state"].patterns = [r", (\w\w)\W", r", (\w\w)$"]
        self.fields["state"].process = lambda t: t[0].strip()
        self.fields["source"].func = lambda doc: "computerjobs.com"
        self.fields["posting_date"].func = lambda doc: doc.find("span", id=re.compile("spanPosted")).string
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
        self.fields["posting_date"].depth = 2
        self.fields.update(kwargs)
        
        def nextpage(doc, page):
            link = doc.find("a", id=re.compile(r"hlNextPage"))
            if link is None:
                return None
            return "http://computerjobs.com" + link["href"]
        
        self.datafunc = lambda doc: doc.findAll("table", id=re.compile(r"jobResults"))
        self.url = "http://computerjobs.com/jresults.aspx?s_kw=%s&s_sl=&s_excNonIT=off&s_excNatl=off"
        self.nextlink = nextpage
    
    