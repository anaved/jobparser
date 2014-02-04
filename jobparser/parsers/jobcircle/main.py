#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        
        self.fields["company_name"].func = lambda doc: "".join(doc.findAll("td").pop().a.findAll(text=True))
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: "".join(doc.find("p", id="wrapJobTitle").a.findAll(text=True))
        self.fields["company_joburl"].func = lambda doc: "http://jobcircle.com" + doc.find("p", id="wrapJobTitle").a["href"]
        self.fields["source_joburl"].func = lambda doc: "http://jobcircle.com" + doc.find("p", id="wrapJobTitle").a["href"]
        self.fields["city"].func = lambda doc: doc.find("p", id="wrapJobTitle").findAll("br")[0].nextSibling
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.find("p", id="wrapJobTitle").findAll("br")[0].nextSibling
        self.fields["state"].patterns = [r", (\w\w)\W", r", (\w\w)$"]
        self.fields["state"].process = lambda t: t[0].strip()
        self.fields["source"].func = lambda doc: "jobcircle.com"
        self.fields["posting_date"].func = lambda doc: doc.find("p", id="wrapJobTitle").findAll("br")[1].nextSibling
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
        self.filterfields["zipcode"].func = lambda doc: "".join(doc.find("b", text=re.compile("ZIP Code:")).parent.parent.parent.findAll(text=True))
        self.filterfields["zipcode"].patterns = [r"(\d{5})"]
        self.filterfields["zipcode"].process = lambda t: t[0].strip()
        self.filterfields["zipcode"].depth = 2
        self.fields.update(kwargs)
        self.keyword = ['a']
        def nextpage(doc, page):
            if doc.find('a',text='[More]'):
               start=(page*50)+1
               return  'http://jobcircle.com/public/csearch.mpl?search_string=%s&search_method=and&search_radius=&search_zip_code=&industry_code=ALL&chk_search_radius=0&reward=&start=%d&len=50&job_length=&search_scope=1'%\
                      (self.query,start)
            return None
        
        self.nextlink = nextpage
        self.datafunc = lambda doc: [tr for tr in doc.findAll("tr") if len(tr.findAll("td", {'class': "tblrowcolored"}, recursive=False))+len(tr.findAll("td", {'class': "tblrowwhite"}, recursive=False)) > 1]
        self.url = "http://jobcircle.com/public/csearch.mpl?search_string=%s&search_method=and&search_radius=&search_zip_code=&industry_code=ALL&chk_search_radius=0&reward=&start=0&len=50&job_length=&search_scope=1"
    
    