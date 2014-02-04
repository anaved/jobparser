import traceback
#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.findAll("td", {'class': None})[1].a.string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.findAll("td", {'class': None})[0].a.string
        self.fields["company_joburl"].func = lambda doc: "http://seeker.dice.com" + doc.findAll("td", {'class': None})[0].a["href"]
        self.fields["source_joburl"].func = lambda doc: "http://seeker.dice.com" + doc.findAll("td", {'class': None})[0].a["href"]
        self.fields["city"].func = lambda doc: doc.findAll("td", {'class': None})[2].string
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.findAll("td", {'class': None})[2].string
        self.fields["state"].patterns = [r", (\w\w)\W", r", (\w\w)$"]
        self.fields["state"].process = lambda t: t[0].strip()
        self.fields["source"].func = lambda doc: "dice.com"
        self.fields["posting_date"].func = lambda doc: doc.findAll("td", {'class': None})[3].string
        self.fields["posting_date"].patterns = [r"(\w\w\w)-(\d\d)"]
        self.fields["posting_date"].process = common.mmm_dd
        self.fields.update(kwargs)
        self.dev_mode=True
        def nextpage(doc, page):
            links=doc.find('div',{'class':'pageProg'})
            if links:
                  last_link=links.findAll('a')[-1]
                  return'http://seeker.dice.com'+last_link['href'] if last_link.string.startswith('Next') else None
        self.nextlink = nextpage
        self.datafunc = lambda doc: [elem for elem in doc.tbody.findAll("tr") if elem('td', {'class': "icon"})]
        self.url = "http://seeker.dice.com/jobsearch/servlet/JobSearch?QUICK=1&NUM_PER_PAGE=500&TRAVEL=0&FRMT=0&LOCATION_OPTION=2&Ntx=mode+matchall&DAYSBACK=30&RADIUS=64.37376&op=300&Hf=0&N=0&ZC_COUNTRY=0&FREE_TEXT=%s&Ntk=JobSearchRanking&TAXTERM=0&Ns=p_PostedAge|0&SORTDIR=7&SORTSPEC=0"
    