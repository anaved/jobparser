#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: "".join(doc.find("td", id=re.compile(r"Company")).findAll(text=True))
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.find("a", {'class': "jt"}).string
        self.fields["company_joburl"].func = lambda doc: doc.find("a", {'class': "jt"})["href"]
        self.fields["source_joburl"].func = self.fields["company_joburl"].func
        self.fields["city"].func = lambda doc: doc.find("td", id=re.compile(r"Location")).string
        self.fields["city"].patterns = [r"-([^-]*)$"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.find("td", id=re.compile(r"Location")).string
        self.fields["state"].patterns = [r"^(\w\w)\W"]
        self.fields["state"].process = lambda t: t[0].strip()
        self.fields["source"].func = lambda doc: "jobpath.com"
        self.fields["posting_date"].func = lambda doc: doc.find("span", id=re.compile(r"Posted"))["title"]
        self.fields["posting_date"].patterns = [r"(\w\w\w)-(\d\d?)"]
        self.fields["posting_date"].process = common.mmm_dd 
        self.fields.update(kwargs)
        
        def nextpage(doc, page):
            links = doc.find("td", {'class': "nav_btm_cell"})
            if links :
                return links.a["href"] if links.find('a',text='Next Page') else None
            return None
        
        self.datafunc = lambda doc: doc.findAll("tr", {'class': re.compile(r"^jl_\w+_row$")})
        self.url = "http://www.jobpath.com/JobSeeker/Jobs/JobResults.aspx?IPath=QHKCV&excrit=QID%3dA6657255451511%3bst%3da%3buse%3dALL%3brawWords%3d%s%3bCID%3dUS%3bSID%3d%3f%3bTID%3d0%3bENR%3dNO%3bDTP%3dDRNS%3bYDI%3dYES%3bIND%3dALL%3bPDQ%3dAll%3bPDQ%3dAll%3bPAYL%3d0%3bPAYH%3dgt120%3bPOY%3dNO%3bETD%3dALL%3bRE%3dALL%3bMGT%3dDC%3bSUP%3dDC%3bFRE%3d30%3bQS%3dsid_unknown%3bSS%3dNO%3bTITL%3d0%3bJQT%3dRAD%3bJDV%3dFalse%3bExpHigh%3dgt50%3bExpLow%3d0%3bMaxLowExp%3d-1&sc=3&ff=21&sd=2"
        self.nextlink = nextpage
        self.dev_mode=True
    