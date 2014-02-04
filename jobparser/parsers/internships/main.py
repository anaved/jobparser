#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from datetime import datetime
class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)        
        self.fields["company_name"].func = lambda doc: doc.find('span',{'class':'company-name'}).next.split('&mdash;')[0]
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.find("h3", {'class': "title"}).a.string
        self.fields["company_joburl"].func = lambda doc: "http://www.internships.com" + doc.find("h3", {'class': "title"}).a['href']
        self.fields["source_joburl"].func = lambda doc: "http://www.internships.com" + doc.find("h3", {'class': "title"}).a['href']
        self.fields["city"].func = lambda doc : get_loc(doc)[0]
        self.fields["state"].func = lambda doc : get_loc(doc)[1]
        self.fields["source"].func = lambda doc: "internships.com"
        self.fields["posting_date"].func = lambda doc : datetime.now()
        self.fields.update(kwargs)
        self.keyword = ['the',]

        def get_loc(doc):
           x= doc.find('span',{'class':'internship-location'}).string.strip().split(',')
           if len(x)>1:
               return [x[0],x[1]]
           else:
               return [x[0],'']
           
        def nextpage(doc, page):
             x= 'http://www.internships.com/search/post/results?keywords=%s&start=%d&limit=100'%(self.query,page*10)
             return x
        
        self.datafunc = lambda doc: doc.findAll("div", {'class': 'search-result-item item-wrap '})       
        self.url =  'http://www.internships.com/search/post/results?keywords=%s&limit=100'
        self.nextlink = nextpage
        self.dev_mode=True