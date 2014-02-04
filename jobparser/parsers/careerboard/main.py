#!/usr/bin/env python

from util import common
from core.JobsiteParser import JobsiteParser
from util.html2content import get_desc

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.find("ul", {'class': "details"}).findAll("li")[1].string
        self.fields["company_name"].patterns = [r"^\s*(.*?)\s*$"]
        self.fields["company_name"].process = lambda doc: doc[0]
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["company_id"].patterns = self.fields["company_name"].patterns
        self.fields["company_id"].process = self.fields["company_name"].process
        self.fields["title"].func = lambda doc: doc.h3.a["title"]
        self.fields["company_joburl"].func = lambda doc: "http://www.careerboard.com" + doc.h3.a["href"]
        self.fields["source_joburl"].func = lambda doc: "http://www.careerboard.com" + doc.h3.a["href"]
        self.fields["city"].func = lambda doc: doc.find("ul", {'class': "details"}).findAll("li")[0].string
        self.fields["city"].patterns = [r".*?\|.*?\|([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.find("ul", {'class': "details"}).findAll("li")[0].string
        self.fields["state"].patterns = [r".*?\|.*?\|.*?, (\w\w)\W", r".*?\|.*?\|.*?, (\w\w)$"]
        self.fields["state"].process = lambda t: t[0].strip()
        self.fields["source"].func = lambda doc: "careerboard.com"
        self.fields["posting_date"].func = lambda doc: doc.find("p", {'class': "floatr small"}).string
        self.fields["posting_date"].patterns = [r"\s*(\d\d)/(\d\d)/(\d\d\d\d)\s*"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
        self.fields.update(kwargs)
        self.fields["all_text"].func = lambda doc: all_text(doc)

        def all_text(doc):
            doc= doc.find('div',{'class':'job-description'})
            doc.find('h2').extract() if doc.find('h2') else None
            return get_desc(doc,self.url)

        def nextpage(doc, page):                
                linkSet = doc.find("div", {'class': "pages"})                
                if linkSet.findAll()[-1].name!='span':
                   return 'http://www.careerboard.com'+linkSet.find('span').findNext('a')['href']
                return None
            
        
        self.datafunc = lambda doc: doc.findAll('div', {'class': " listing1  "})
        self.url = "http://www.careerboard.com/jobs/containing-any-of-%s"
        self.nextlink = nextpage