#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: ""
        self.fields["company_id"].func = lambda doc: ""
        self.fields["title"].func = lambda doc: doc.previousSibling.previousSibling.find("a",{'class':'tl'}).findChild().string
        self.fields["company_joburl"].func = lambda doc: "http://www.tiptopjob.com"+doc.previousSibling.previousSibling.find("a",{'class':'tl'})['href']
        self.fields["source_joburl"].func = self.fields["company_joburl"].func
        self.fields["city"].func = lambda doc: loc(doc).previous.split("(")[0]
        self.fields["state"].func = lambda doc: loc(doc).string
#        self.fields["state"].process = common.shorten
        self.fields["source"].func = lambda doc: "tiptopjob.com"
        self.fields["posting_date"].func = lambda doc: x(doc)
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d\d\d)"]
        self.fields["posting_date"].process = common.dd_mm_yyyy
        self.fields.update(kwargs)
        
        self.datafunc = lambda doc: doc.find("table",id='tbljobresults').findAll('tr',{'class':'cr'})        
        self.url="http://www.tiptopjob.com/search/tiptopresults.asp?qs=1&srchtype=1&jobtype=3&keyword=%s&searchby=1&country=USA&orderby=4&sortdirection=1&newsearch=1&PageNo=1"

        def x(doc):
             y=doc.find('table',{'class':'sjd'}).findAll('tr')[-1].findAll('td')[-1]
             print y
             return y
        def loc(doc):            
            return doc.find('table',{'class':'sjd'}).findAll('tr')[0].findAll('td')[1].a
            

        def nextpage(doc, page):
           x=doc.find('img',src='http://img.tiptopjob.com/jobs_images/next_arrow.png')
           if x.parent.name=='a':
                 return "http://www.tiptopjob.com/search/tiptopresults.asp?qs=1&srchtype=1&jobtype=3&keyword=%s&searchby=1&country=USA&orderby=4&sortdirection=1&newsearch=1&PageNo=%d"%(self.query,page+1,)
           return None
        self.dev_mode=True
        self.nextlink = nextpage
        self.clean_html=True