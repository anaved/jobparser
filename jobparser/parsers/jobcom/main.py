#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.findNext('h4').string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.a.string
        self.fields["company_joburl"].func = lambda doc: doc.a["href"]
        self.fields["source_joburl"].func = lambda doc: doc.a["href"]
        self.fields["city"].func = lambda doc: doc.findNext('div').string.split(',')[0]
        self.fields["city"].process = lambda t: t.strip()
        self.fields["state"].func = lambda doc: doc.findNext('div').string.split(',')[1]
        self.fields["state"].process = lambda t: t.strip()
        self.fields["source"].func = lambda doc: "job.com"
        self.fields["posting_date"].func = lambda doc: doc.find('ul',{'id':'jobSummary'}).findAll('li')[2]._lastRecursiveChild().strip()
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
        self.fields["posting_date"].depth = 2
        self.fields.update(kwargs)
        
        def nextpage(doc, page):
            links= doc.find('p',{'class':'resultsJumper'})
            if links is None or  links.findAll('a') is None:
                return None
            return links.findAll('a')[0]['href']
        
        self.datafunc = lambda doc: doc.findAll('h2',{'class':'jobTitle_results'})[2:]
        self.url = "http://www.job.com/my.job/search/page=results/pt=2/qs=2/kw=%s/kt=3/ns=1/f=60/rpp=10/&b=2"
        self.nextlink = nextpage
        self.cookie=False
    
    