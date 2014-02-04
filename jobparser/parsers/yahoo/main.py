#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        
        self.fields["company_name"].func = lambda doc: doc.find("td", {'class': "c"}).a.string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.find("td", {'class': "t"}).a.string
        self.fields["company_joburl"].func = lambda doc: "http://hotjobs.yahoo.com" + doc.find("td", {'class': "t"}).a["href"].split(';')[0]
        self.fields["source_joburl"].func = lambda doc: "http://hotjobs.yahoo.com" + doc.find("td", {'class': "t"}).a["href"].split(';')[0]
        self.fields["source"].func = lambda doc: "hotjobs.yahoo.com"
        self.fields["posting_date"].func = lambda doc: doc.find("td", {'class': "d"}).string
        self.fields["posting_date"].patterns = [r"(\w\w\w) (\d\d)"]
        self.fields["posting_date"].process = common.mmm_dd
        self.fields.update(kwargs)
        
        self.datafunc = lambda doc: doc.findAll("tr", {'class': " top"})
        self.url = "http://hotjobs.yahoo.com/job-search?jobtype=PERM&jobtype=CONT&commitment=FT&commitment=PT&locations=&country=&industry=&kw=%s&sort[type]=date"
        
        def getexp(doc):
            for tr in doc.findAll("tr"):
                if tr.th.string == "Experience":
                    return tr.td.string or ""
        
        def getloc(doc):
            try:
                return doc.find("td", {'class': "l"}).string
            except:
                return doc.find("span", {'class': "first-of-type"}).string
        
        def nextpage(doc, page):
            linkSet=doc.find("div", {'class': "pageCtrl"})
            links = linkSet.findAll("a")
            if links[-1].findChild():
                return 'http://hotjobs.yahoo.com'+linkSet.find('a',{'class':'current'}).findNext()['href']
            return None
        
        self.fields["city"].func = getloc
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = getloc
        self.fields["state"].patterns = [r", (\w\w)\W", r", (\w\w)$"]
        self.fields["state"].process = lambda t: t[0].strip()
        
#        self.filterfields["experience"].func = getexp
#        self.filterfields["experience"].patterns = [r"(\d+)-(\d+)"]
#        self.filterfields["experience"].process = common.expminmax
#        self.filterfields["experience"].depth = 2
        self.nextlink = nextpage
        self.dev_mode=True