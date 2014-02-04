#!/usr/bin/env python
from util import common
from core.JobsiteParser import JobsiteParser
from datetime import datetime
from parsers.regionalhelpwanted.conf import xdomains
import re
class Parser(JobsiteParser):
    def __init__(self, keyword, logger, ** kwargs):
        JobsiteParser.__init__(self, logger)
        self.keyword = keyword        
        self.fields["source"].func = lambda doc: 'regionalhelpwanted.com'
        self.fields["title"].func = lambda doc: doc.findAll('a')[0].string
        self.fields["company_joburl"].func = lambda doc: doc.findAll('a')[0]['href']
        self.fields["source_joburl"].func = self.fields["company_joburl"].func
        self.fields["company_name"].func = lambda doc: get_company(doc)
        self.fields["company_name"].depth = 2
        self.fields["company_id"].func =self.fields["company_name"].func
        self.fields["company_id"].depth = 2
        self.fields["city"].func = lambda doc: get_location(doc)[0]
        self.fields["city"].depth = 2
        self.fields["state"].func = lambda doc: get_location(doc)[1]
        self.fields["state"].depth = 2
        self.fields["posting_date"].func = lambda doc: get_posting_date(doc)
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yy
        self.fields["posting_date"].depth = 2
        self.fields.update(kwargs)         

        def get_company(doc):
           doc= get_tab(doc)            
           comp= doc.find('td',text=re.compile('Company Name:'))
           if comp:
               return comp.next.next.firstText().string
           return 'Unknown'

        def get_location(doc):
           doc= get_tab(doc)
           loc= doc.find('td',text=re.compile('Location:'))
           if loc:
               return [loc.next.next.string,'US']
           return [None,None]

        def get_posting_date(doc):
            doc= get_tab(doc)            
            d= doc.find('td',text=re.compile(r"(\d\d?)/(\d\d?)/(\d\d)"))
            return d.strip() if d else datetime.now().strftime('%m/%d/%y')            


        def get_tab(doc):
           if doc:
                tab= doc.findAll('table')
                return tab[1] if tab else ''
           return ''

        self.dev_mode = True
        self.datafunc = lambda doc: doc.findAll("div", {'class':'detailswhite'})#re.compile("^displayTableRow.*")})

        self.url = [e[0] for e in xdomains]