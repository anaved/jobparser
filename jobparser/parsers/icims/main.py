
#!/usr/bin/env python
from datetime import datetime
from util import common
from core.JobsiteParser import JobsiteParser
from parsers.icims.conf import xdomains
from urlparse import urlparse
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: get_company()
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.string.strip()
        self.fields["company_joburl"].func = lambda doc: doc['href']
        self.fields["source_joburl"].func = self.fields["company_joburl"].func
        self.fields["city"].func = lambda doc: find_location(doc)['city'] if find_location(doc).has_key('city') else None
        self.fields["city"].depth = 2
        self.fields["state"].func = lambda doc: find_location(doc)['state'] if find_location(doc).has_key('state') else None
        self.fields["state"].depth = 2
        self.fields["source"].func = lambda doc: get_company()#"icims.com"
        self.fields["posting_date"].func = lambda doc: find_date(doc)
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
        self.fields["posting_date"].depth = 2
        self.fields.update(kwargs)

        def find_location(doc):
                header = doc.findAll('th', attrs={'class':'iCIMS_JobHeaderField'})
                location = {}
                for e in header:
                    try:
                        txt = e.string.strip().lower()
                        if txt.startswith('location'):
                            data=unicode(e.findNext().string.strip().encode('ascii', 'ignore'))                            
                            loc=data.split("-")
                            location['city']=loc[-1]
                            location['state']=loc[-2]
                        if txt.startswith('city'):
                            data=unicode(e.findNext().string.strip().encode('ascii', 'ignore'))                            
                            location['city']=data
                        if txt.startswith('state'):
                            data=unicode(e.findNext().string.strip().encode('ascii', 'ignore'))                            
                            location['state']=data
                    except:pass                
                return location

        def find_date(doc):
                header = doc.findAll('th', attrs={'class':'iCIMS_JobHeaderField'})
                date=None
                for e in header:
                    try:
                        txt = e.string.strip().lower()                        
                        if 'date' in txt:
                            date=unicode(e.findNext().string.strip().encode('ascii', 'ignore'))
                    except:pass
                if not date:
                    date=datetime.now().strftime('%m/%d/%Y')                
                return date
              
        def get_company():
              dom= urlparse(self.url)
              dom="http://%s"%(dom.netloc,)
              return xdomains[dom][0]

        def nextpage(doc, page):
            x='http.*'+urlparse(self.url).netloc+'/jobs/search.*?pr='+str(page+1)            
            next_pat = re.compile(x)
            d= re.findall(next_pat, str(doc))           
            if len(d):
                return d[0]
            return None

        self.nextlink=nextpage        

        def get_data(doc):           
           pat = re.compile('.*icims.com/jobs/(\d+)/job')
           x= doc.find("table",{'class':'iCIMS_JobsTable'})
           if x:            
               urls = x.findAll('a', href=pat)
               return urls
           return []

        self.datafunc = lambda doc: get_data(doc)        
        self.url=[e+"/jobs/search?searchKeyword=%s" for e in xdomains.keys()]
