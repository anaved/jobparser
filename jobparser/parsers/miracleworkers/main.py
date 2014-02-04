#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.find("a", {'class': "rslt"}).string if doc.find("a", {'class': "rslt"}) else ''
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.find("a", {'class': "jt"}).string
        self.fields["company_joburl"].func = lambda doc: doc.find("a", {'class': "jt"})["href"]
        self.fields["source_joburl"].func = lambda doc: doc.find("a", {'class': "jt"})["href"]
        self.fields["city"].func = lambda doc: doc.findAll("td", recursive=False)[2].string
        self.fields["city"].patterns = [r"-([^-]*)$"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.findAll("td", recursive=False)[2].string
        self.fields["state"].patterns = [r"^(\w\w)\W"]
        self.fields["state"].process = lambda t: t[0].strip()
#        self.fields["latitude"].func = lambda doc: doc.find("a", id=re.compile("MapJob"))["href"]
#        self.fields["latitude"].patterns = [r"lat=(.*?),"]
#        self.fields["latitude"].process = lambda t: float(t[0].strip())
#        self.fields["latitude"].depth = 2
#        self.fields["longitude"].func = lambda doc: doc.find("a", id=re.compile("MapJob"))["href"]
#        self.fields["longitude"].patterns = [r"lon=(.*?),"]
#        self.fields["longitude"].process = lambda t: float(t[0].strip())
#        self.fields["longitude"].depth = 2
        self.fields["source"].func = lambda doc: "miracleworkers.com"
        self.fields["posting_date"].func = lambda doc: doc.find("td", {'class': "jl_rslt_posted_cell"}).span["title"]
        self.fields["posting_date"].patterns = [r"(\w\w\w)-(\d\d?)"]
        self.fields["posting_date"].process = common.mmm_dd
        self.fields.update(kwargs)
        
        def nextpage(doc, page):
            links = doc.find("td", {'class': "nav_btm_cell"})
            if links is None or links.span.a is None:
                return None
            return links.span.a["href"]
        
        self.datafunc = lambda doc: doc.findAll("tr", {'class': re.compile(r"^jl_\w\w\w\w?_row$")}) if doc else None
        self.url = "http://www.miracleworkers.com/WM/JobSeeker/Jobs/JobResults.aspx?IPath=JRKCV&excrit=QID%3dA3853780526142%3bst%3dA%3buse%3dALL%3brawWords%3d%s%3bCID%3dUS%3bSID%3d%3f%3bTID%3d0%3bENR%3dNO%3bDTP%3dDRNS%3bYDI%3dYES%3bIND%3dALL%3bPDQ%3dAll%3bPDQ%3dAll%3bPAYL%3d0%3bPAYH%3dGT120%3bPOY%3dNO%3bETD%3dALL%3bRE%3dALL%3bMGT%3dDC%3bSUP%3dDC%3bFRE%3d30%3bCHL%3dWM%3bQS%3dSID_UNKNOWN%3bSS%3dNO%3bTITL%3d0%3bJQT%3dRAD%3bJDV%3dFalse%3bExpHigh%3dGT50%3bExpLow%3d0%3bMaxLowExp%3d-1&sc=3&ff=21&sd=2"
        self.nextlink = nextpage
    
    