#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.find("span", {'class': "company"}).string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.find("a", {'class': "jobTitle"})["title"]
        self.fields["company_joburl"].func = lambda doc: doc.find("a", {'class': "jobTitle"})["href"]
        self.fields["source_joburl"].func = lambda doc: doc.find("a", {'class': "jobTitle"})["href"]
        self.fields["city"].func = lambda doc: "".join(doc.find("span", {'class': "jobplace"}).findAll(text=True))
        self.fields["city"].patterns = [r"^([^,]*),"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: "".join(doc.find("span", {'class': "jobplace"}).findAll(text=True))
        self.fields["state"].patterns = [r"\W(\w\w),", r"\W(\w\w)$"]
        self.fields["state"].process = lambda t: t[0].strip()
        self.fields["source"].func = lambda doc: "monster.com"
        self.fields["posting_date"].func = lambda doc: doc.find("span", {'class': "postingdate"}).string
        self.fields["posting_date"].patterns = [r"()today", r"(\d+)"]
        self.fields["posting_date"].process = common.daysago
        self.fields.update(kwargs)
        self.dev_mode=True
        def nextpage(doc, page):
            nav= doc.find('div',{'class':'navigationBar'})
            links= nav.findAll('a')
            if links[-1].has_key('href'):
                url='http://jobsearch.monster.com/PowerSearch.aspx?q=%s&rad=20&rad_units=miles&tm=60&dv=&pg=%d&pp=500&sort=dt.rv'%(self.query,page+1)                
                return url
            return None

        self.nextlink=nextpage
        self.datafunc = lambda doc: doc.findAll("div", {'class': "itemHeader"})
        self.url = "http://jobsearch.monster.com/PowerSearch.aspx?q=%s&rad=20&rad_units=miles&tm=60&dv=&pg=1&pp=500&sort=dt.rv"

